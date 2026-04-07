// ---------------------------------------------------------------------------
// Plan definitions
// ---------------------------------------------------------------------------

export type PlanId = "starter" | "pro" | "equipe";

export interface PlanLimits {
  maxDataSources: number | null; // null = unlimited
  maxRows: number | null;
  maxReportsPerMonth: number;
  maxAlerts: number;
  maxUsers: number;
  hasAiInsights: boolean;
  hasCustomReports: boolean;
  hasApiAccess: boolean;
  hasWhiteLabel: boolean;
  hasPrioritySupport: boolean;
}

export const PLAN_LIMITS: Record<PlanId, PlanLimits> = {
  starter: {
    maxDataSources: 1,
    maxRows: 1_000,
    maxReportsPerMonth: 1,
    maxAlerts: 1,
    maxUsers: 1,
    hasAiInsights: false,
    hasCustomReports: false,
    hasApiAccess: false,
    hasWhiteLabel: false,
    hasPrioritySupport: false,
  },
  pro: {
    maxDataSources: 3,
    maxRows: 20_000,
    maxReportsPerMonth: 5,
    maxAlerts: 5,
    maxUsers: 3,
    hasAiInsights: true,
    hasCustomReports: true,
    hasApiAccess: false,
    hasWhiteLabel: false,
    hasPrioritySupport: false,
  },
  equipe: {
    maxDataSources: null,
    maxRows: null,
    maxReportsPerMonth: 999,
    maxAlerts: 999,
    maxUsers: 20,
    hasAiInsights: true,
    hasCustomReports: true,
    hasApiAccess: true,
    hasWhiteLabel: true,
    hasPrioritySupport: true,
  },
};

export const PLAN_PRICES: Record<PlanId, { monthly: number; annual: number }> = {
  starter: { monthly: 0, annual: 0 },
  pro: { monthly: 99, annual: 990 },
  equipe: { monthly: 249, annual: 2490 },
};

export const PLAN_NAMES: Record<PlanId, string> = {
  starter: "Starter",
  pro: "Pro",
  equipe: "Equipe",
};

// ---------------------------------------------------------------------------
// KPI types
// ---------------------------------------------------------------------------

export type KpiType =
  | "revenue"
  | "net_margin"
  | "active_clients"
  | "critical_stock"
  | "expenses"
  | "profit"
  | "orders"
  | "avg_order_value"
  | "conversion_rate"
  | "growth_rate";

export const KPI_LABELS: Record<KpiType, string> = {
  revenue: "Chiffre d'affaires",
  net_margin: "Marge nette",
  active_clients: "Clients actifs",
  critical_stock: "Stock critique",
  expenses: "Depenses",
  profit: "Benefice net",
  orders: "Commandes",
  avg_order_value: "Panier moyen",
  conversion_rate: "Taux de conversion",
  growth_rate: "Croissance",
};

export const KPI_FORMATS: Record<KpiType, "currency" | "percent" | "number"> =
  {
    revenue: "currency",
    net_margin: "percent",
    active_clients: "number",
    critical_stock: "number",
    expenses: "currency",
    profit: "currency",
    orders: "number",
    avg_order_value: "currency",
    conversion_rate: "percent",
    growth_rate: "percent",
  };

// ---------------------------------------------------------------------------
// Data source types
// ---------------------------------------------------------------------------

export const DATA_SOURCE_TYPES = [
  { id: "excel", label: "Excel (.xlsx)", icon: "FileSpreadsheet" },
  { id: "csv", label: "CSV (.csv)", icon: "FileText" },
  { id: "google_sheets", label: "Google Sheets", icon: "Sheet" },
  { id: "odoo", label: "Odoo ERP", icon: "Database" },
  { id: "sage", label: "Sage Comptabilite", icon: "Calculator" },
] as const;

export type DataSourceTypeId = (typeof DATA_SOURCE_TYPES)[number]["id"];

// ---------------------------------------------------------------------------
// Sectors
// ---------------------------------------------------------------------------

export const SECTORS = [
  { id: "distribution", label: "Distribution & Commerce de Gros", icon: "Truck", description: "Grossistes, distributeurs FMCG, importateurs" },
  { id: "retail", label: "Retail & Chaines de Magasins", icon: "Store", description: "Chaines de magasins, franchises, multi-points de vente" },
  { id: "industrie", label: "Industrie & Fabrication", icon: "Factory", description: "Usines textile, agroalimentaire, plasturgie, BTP" },
  { id: "transport", label: "Transport & Logistique", icon: "Truck", description: "Flottes de camions, transitaires, messagerie" },
  { id: "restaurant", label: "Restaurants & F&B", icon: "UtensilsCrossed", description: "Restaurants, fast-food, dark kitchens, traiteurs" },
  { id: "ecommerce", label: "E-commerce", icon: "ShoppingCart", description: "Vente en ligne, Instagram, Shopify, Jumia" },
  { id: "clinique", label: "Cliniques & Sante", icon: "HeartPulse", description: "Cliniques privees, laboratoires, cabinets dentaires" },
  { id: "pharmacie", label: "Pharmacies & Parapharmacies", icon: "Pill", description: "Groupements de pharmacies, parapharmacies" },
  { id: "immobilier", label: "Immobilier & Promotion", icon: "Building2", description: "Promoteurs immobiliers, agences, lotisseurs" },
  { id: "hotel", label: "Hotels & Riads", icon: "Hotel", description: "Hotels, riads, maisons d'hotes, resorts" },
  { id: "services", label: "Services & Prestations B2B", icon: "Briefcase", description: "Cabinets conseil, agences, maintenance" },
  { id: "agriculture", label: "Agriculture & Cooperatives", icon: "Sprout", description: "Fermes modernes, cooperatives, export agricole" },
] as const;

export type SectorId = (typeof SECTORS)[number]["id"];

// ---------------------------------------------------------------------------
// Periods
// ---------------------------------------------------------------------------

export const PERIODS = [
  { id: "this_month", label: "Ce mois" },
  { id: "last_month", label: "Mois dernier" },
  { id: "last_3_months", label: "3 derniers mois" },
  { id: "this_year", label: "Cette annee" },
  { id: "custom", label: "Personnalise" },
] as const;

export type PeriodId = (typeof PERIODS)[number]["id"];

// ---------------------------------------------------------------------------
// Feature flags
// ---------------------------------------------------------------------------

export const FEATURES: Record<PlanId, string[]> = {
  starter: [
    "1 source de donnees",
    "Dashboard de base",
    "3 rapports / mois",
    "2 alertes",
  ],
  pro: [
    "3 sources de donnees",
    "Dashboard avance",
    "10 rapports / mois",
    "10 alertes",
    "Insights IA",
    "Rapports personnalises",
  ],
  equipe: [
    "Sources illimitees",
    "Dashboard premium",
    "Rapports illimites",
    "Alertes illimitees",
    "Insights IA avances",
    "Acces API",
    "Marque blanche",
    "Support prioritaire",
  ],
};

// ---------------------------------------------------------------------------
// Moroccan cities (common)
// ---------------------------------------------------------------------------

export const MOROCCAN_CITIES = [
  "Casablanca",
  "Rabat",
  "Marrakech",
  "Fes",
  "Tanger",
  "Agadir",
  "Meknes",
  "Oujda",
  "Kenitra",
  "Tetouan",
  "Safi",
  "El Jadida",
  "Nador",
  "Beni Mellal",
  "Khouribga",
  "Mohammedia",
  "Settat",
  "Taza",
  "Berrechid",
  "Khemisset",
] as const;
