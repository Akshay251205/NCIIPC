export interface DashboardStat {
  title: string;
  value: string;
  change: string;
  description: string;
  type:
    | "organization"
    | "users"
    | "analysts"
    | "alerts"
    | "investigations"
    | "assets";
}

export interface AlertTrend {
  day: string;
  alerts: number;
}

export interface SeverityItem {
  name: string;
  value: number;
}

export interface SectorItem {
  sector: string;
  organizations: number;
}

export interface ActivityItem {
  time: string;
  user: string;
  action: string;
  detail: string;
  status: string;
}

export const dashboardStats: DashboardStat[] = [
  {
    title: "Organizations",
    value: "52",
    change: "+5.2%",
    description: "vs last month",
    type: "organization",
  },
  {
    title: "Users",
    value: "438",
    change: "+8.4%",
    description: "vs last month",
    type: "users",
  },
  {
    title: "Analysts",
    value: "326",
    change: "+4.8%",
    description: "vs last month",
    type: "analysts",
  },
  {
    title: "Total Alerts",
    value: "125.4K",
    change: "+12.1%",
    description: "vs last month",
    type: "alerts",
  },
  {
    title: "Investigations",
    value: "24.3K",
    change: "+6.7%",
    description: "vs last month",
    type: "investigations",
  },
  {
    title: "Assets",
    value: "8,920",
    change: "+3.9%",
    description: "vs last month",
    type: "assets",
  },
];

export const alertTrendData: AlertTrend[] = [
  { day: "Sep 09", alerts: 14500 },
  { day: "Sep 10", alerts: 19800 },
  { day: "Sep 11", alerts: 15600 },
  { day: "Sep 12", alerts: 18100 },
  { day: "Sep 13", alerts: 21900 },
  { day: "Sep 14", alerts: 28400 },
  { day: "Sep 15", alerts: 24100 },
  { day: "Sep 16", alerts: 26700 },
];

export const severityData: SeverityItem[] = [
  {
    name: "Critical",
    value: 12540,
  },
  {
    name: "High",
    value: 28320,
  },
  {
    name: "Medium",
    value: 52110,
  },
  {
    name: "Low",
    value: 32450,
  },
];

export const sectorData: SectorItem[] = [
  { sector: "Banking", organizations: 12 },
  { sector: "Power", organizations: 8 },
  { sector: "Telecom", organizations: 7 },
  { sector: "Oil & Gas", organizations: 6 },
  { sector: "Transport", organizations: 6 },
  { sector: "Healthcare", organizations: 5 },
  { sector: "Others", organizations: 8 },
];

export const recentActivity: ActivityItem[] = [
  {
    time: "14:32",
    user: "Admin",
    action: "Uploaded dataset",
    detail: "alerts.csv",
    status: "Success",
  },
  {
    time: "13:45",
    user: "Admin",
    action: "Created new analyst",
    detail: "AN-00328",
    status: "Success",
  },
  {
    time: "12:18",
    user: "System",
    action: "AI model loaded",
    detail: "Investigation NLP v1.2",
    status: "Success",
  },
  {
    time: "11:03",
    user: "Admin",
    action: "Updated rule threshold",
    detail: "Speed Demon Detector",
    status: "Success",
  },
  {
    time: "10:27",
    user: "Admin",
    action: "Added organization",
    detail: "CSE-052",
    status: "Success",
  },
];