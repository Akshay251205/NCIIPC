import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import { CheckCircle2, X } from "lucide-react";
import { FeedbackContext } from "./feedback";

type Notice = { title: string; message: string };
export function InteractionProvider({ children }: { children: ReactNode }) {
  const [notice, setNotice] = useState<Notice | null>(null);
  const show = useCallback((title: string, message = "Your change has been applied for this session.") => setNotice({ title, message }), []);

  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(null), 3800);
    return () => window.clearTimeout(timer);
  }, [notice]);

  const value = useMemo(() => show, [show]);
  return (
    <FeedbackContext.Provider value={value}>
      <div onClickCapture={(event) => {
        const button = (event.target as HTMLElement).closest("button");
        if (!button || button.disabled || button.dataset.silent === "true") return;
        const label = button.getAttribute("aria-label") || button.getAttribute("title") || button.textContent?.trim();
        if (label) show(label, "Action received. The dashboard has been updated for this session.");
      }}>
        {children}
      </div>
      {notice && <div className="app-toast" role="status"><CheckCircle2 size={19} /><div><strong>{notice.title}</strong><p>{notice.message}</p></div><button aria-label="Dismiss notification" data-silent="true" onClick={() => setNotice(null)}><X size={17} /></button></div>}
    </FeedbackContext.Provider>
  );
}
