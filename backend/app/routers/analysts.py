from sqlalchemy import case, func
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Analyst
from app.models import Alert
from app.models import Investigation
from app.schemas import AnalystResponse, AnalystUpdate
from app.services.pagination import paginate


router = APIRouter(
    prefix="/api/v1/analysts",
    tags=["Analysts"],
)


@router.get("")
def list_analysts(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    organization_id: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Analyst)

    if organization_id:
        query = query.filter(
            Analyst.organization_id == organization_id
        )

    if status:
        query = query.filter(
            Analyst.status == status
        )

    result = paginate(
        query.order_by(Analyst.analyst_id),
        page,
        limit,
    )

    return {
        "success": True,
        **result,
    }


@router.get("/suspicious")
def suspicious_analysts(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Lightweight suspicious-analyst endpoint.

    The full analyst intelligence remains in
    analyst_metrics.py and will be connected more deeply
    during the integration pass.
    """

    analysts = (
        db.query(Analyst)
        .join(
            Alert,
            Alert.analyst_id == Analyst.analyst_id,
        )
        .filter(
            Alert.closure_time_minutes <= 10
        )
        .group_by(Analyst.analyst_id)
        .limit(limit)
        .all()
    )

    return {
        "success": True,
        "count": len(analysts),
        "data": analysts,
    }


@router.get("/performance")
def analyst_performance(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return page-scoped operational metrics without running full AI analysis."""
    investigation_counts = (
        db.query(
            Investigation.analyst_id.label("analyst_id"),
            func.count(Investigation.investigation_id).label("total"),
        )
        .group_by(Investigation.analyst_id)
        .subquery()
    )
    alert_total = func.count(Alert.alert_id)
    closed = func.coalesce(func.sum(case((Alert.status == "Closed", 1), else_=0)), 0)
    evidence = func.coalesce(func.sum(case((Alert.evidence_reviewed.is_(True), 1), else_=0)), 0)
    escalated = func.coalesce(func.sum(case((Alert.escalated.is_(True), 1), else_=0)), 0)
    rows = (
        db.query(
            Analyst,
            alert_total.label("alert_total"),
            closed.label("closed"),
            evidence.label("evidence"),
            escalated.label("escalated"),
            func.avg(Alert.closure_time_minutes).label("average_closure"),
            func.coalesce(investigation_counts.c.total, 0).label("investigation_total"),
        )
        .outerjoin(Alert, Alert.analyst_id == Analyst.analyst_id)
        .outerjoin(investigation_counts, investigation_counts.c.analyst_id == Analyst.analyst_id)
        .group_by(Analyst, investigation_counts.c.total)
        .order_by(Analyst.analyst_id)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    def percent(value, total):
        return round(value / total * 100, 2) if total else 0.0

    def as_row(row):
        analyst, total, closed_count, evidence_count, escalated_count, average_closure, investigation_total = row
        return {
            "analyst_id": analyst.analyst_id,
            "name": analyst.name,
            "organization_id": analyst.organization_id,
            "status": analyst.status,
            "closure_rate": percent(closed_count, total),
            "evidence_review_rate": percent(evidence_count, total),
            "escalation_rate": percent(escalated_count, total),
            "investigation_completion": investigation_total,
            "avg_closure_time_minutes": round(average_closure, 2) if average_closure is not None else None,
        }

    return {"success": True, "total": db.query(func.count(Analyst.analyst_id)).scalar(), "page": page, "limit": limit, "data": [as_row(row) for row in rows]}


@router.get("/{analyst_id}", response_model=AnalystResponse)
def get_analyst(
    analyst_id: str,
    db: Session = Depends(get_db),
):
    analyst = (
        db.query(Analyst)
        .filter(
            Analyst.analyst_id == analyst_id
        )
        .first()
    )

    if not analyst:
        raise HTTPException(
            status_code=404,
            detail="Analyst not found",
        )

    return analyst


@router.patch("/{analyst_id}", response_model=AnalystResponse)
def update_analyst(
    analyst_id: str,
    payload: AnalystUpdate,
    db: Session = Depends(get_db),
):
    """Persist changes made through the administrative analyst profile."""
    analyst = db.query(Analyst).filter(Analyst.analyst_id == analyst_id).first()
    if not analyst:
        raise HTTPException(status_code=404, detail="Analyst not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(analyst, field, value)

    db.commit()
    db.refresh(analyst)
    return analyst
