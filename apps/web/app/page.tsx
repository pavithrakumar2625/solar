"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  Bell,
  Bot,
  CalendarDays,
  ChevronDown,
  CircleDollarSign,
  ClipboardList,
  Cpu,
  Gauge,
  LayoutDashboard,
  MapPin,
  Search,
  Settings,
  ShieldAlert,
  Sparkles,
  Sun,
  Upload,
  Wrench,
  Zap,
} from "./ui/icons";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const navItems = [
  [LayoutDashboard, "Overview"],
  [MapPin, "Sites"],
  [Cpu, "Assets"],
  [Activity, "Digital Twin"],
  [Gauge, "Analytics"],
  [AlertTriangle, "Anomalies"],
  [CircleDollarSign, "Loss Analysis"],
  [Sparkles, "Recovery Simulator"],
  [Wrench, "Maintenance"],
  [ClipboardList, "Technician Mode"],
  [Bot, "AI Copilot"],
  [ClipboardList, "Reports"],
  [Settings, "Settings"],
] as const;

type DashboardMetric = {
  label: string;
  value: string;
  detail: string;
  tone: "green" | "blue" | "orange" | "red" | "muted";
};

type PlantPerformance = {
  id: number;
  name: string;
  capacity_mw: number;
  current_generation_mw: number | null;
  expected_generation_mw: number | null;
  performance_pct: number | null;
};

type DashboardSummary = {
  generated_at: string;
  data_status: "empty" | "ready";
  message: string;
  metrics: DashboardMetric[];
  plants: PlantPerformance[];
  health: {
    healthy: number;
    warning: number;
    critical: number;
  };
  anomalies: string[];
  loss_breakdown: string[];
};

type LoadState = "loading" | "ready" | "error";

function MetricCard({ metric, index }: { metric: DashboardMetric; index: number }) {
  const icons = [Sun, Zap, Gauge, Activity, AlertTriangle, ShieldAlert, Wrench];
  const Icon = icons[index] ?? Activity;

  return (
    <article className="metric-card">
      <span className={`metric-icon ${metric.tone}`}>
        <Icon />
      </span>
      <div>
        <p>{metric.label}</p>
        <strong>{metric.value}</strong>
        <small className={metric.tone === "red" || metric.tone === "orange" ? "danger" : "positive"}>
          {metric.detail}
        </small>
      </div>
    </article>
  );
}

function EmptyPanel({ title, message }: { title: string; message: string }) {
  return (
    <div className="empty-state">
      <b>{title}</b>
      <p>{message}</p>
    </div>
  );
}

export default function Dashboard() {
  const [period, setPeriod] = useState("Today");
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loadState, setLoadState] = useState<LoadState>("loading");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadDashboard() {
      setLoadState("loading");
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/dashboard/summary`, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`Dashboard API returned ${response.status}`);
        }

        const data = (await response.json()) as DashboardSummary;
        setSummary(data);
        setLoadState("ready");
      } catch (fetchError) {
        if (fetchError instanceof DOMException && fetchError.name === "AbortError") {
          return;
        }

        setLoadState("error");
        setError(fetchError instanceof Error ? fetchError.message : "Dashboard API request failed");
      }
    }

    void loadDashboard();

    return () => controller.abort();
  }, []);

  const lastUpdated = useMemo(() => {
    if (!summary) {
      return "Waiting for API";
    }

    return new Intl.DateTimeFormat(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(summary.generated_at));
  }, [summary]);

  const healthTotal = summary
    ? summary.health.healthy + summary.health.warning + summary.health.critical
    : 0;

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span>
            <Sun />
          </span>
          <div>
            <b>SolarRecover AI</b>
            <small>Recover More. Power Tomorrow.</small>
          </div>
        </div>
        <nav>
          {navItems.map(([Icon, name]) => (
            <button className={name === "Overview" ? "active" : ""} disabled={name !== "Overview"} key={name}>
              <Icon />
              <span>{name}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span>SR</span>
          <p>
            Clean Energy
            <br />
            Brighter Future
          </p>
        </div>
      </aside>

      <section className="workspace">
        <header>
          <label className="search">
            <Search />
            <input disabled placeholder="Search is available after asset APIs are implemented" />
          </label>
          <div className="top-actions">
            <button className="notification" disabled aria-label="Notifications are not implemented yet">
              <Bell />
              <i>0</i>
            </button>
            <div className="profile">
              <span>SK</span>
              <p>
                <b>Sathish Kumar</b>
                <small>Admin</small>
              </p>
              <ChevronDown />
            </div>
          </div>
        </header>

        <div className="content">
          <div className="page-title">
            <div>
              <h1>Solar Operations Overview</h1>
              <p>Live foundation view backed by FastAPI and PostgreSQL.</p>
            </div>
            <button className="date-button" disabled>
              <CalendarDays /> {lastUpdated} <ChevronDown />
            </button>
          </div>

          {loadState === "error" ? (
            <div className="state-banner error">
              <AlertTriangle />
              <span>{error}. Check that the FastAPI server, PostgreSQL, and migrations are running.</span>
            </div>
          ) : null}

          {loadState === "loading" ? (
            <div className="state-banner">
              <Activity />
              <span>Loading dashboard data from the backend API...</span>
            </div>
          ) : null}

          {summary ? (
            <div className="state-banner">
              <ShieldAlert />
              <span>{summary.message}</span>
            </div>
          ) : null}

          <section className="metrics">
            {summary?.metrics.map((metric, i) => (
              <MetricCard key={metric.label} metric={metric} index={i} />
            ))}
            {loadState === "loading"
              ? Array.from({ length: 7 }, (_, i) => <article className="metric-card skeleton" key={i} />)
              : null}
          </section>

          <section className="dashboard-grid">
            <article className="panel generation">
              <div className="panel-heading">
                <h2>Generation Overview</h2>
                <select value={period} onChange={(event) => setPeriod(event.target.value)}>
                  <option>Today</option>
                  <option>This Week</option>
                  <option>This Month</option>
                </select>
              </div>
              <EmptyPanel
                title="Telemetry timeline not connected"
                message="The database schema is ready. A time-series API is still needed before this chart can render real generation curves."
              />
            </article>

            <article className="panel health">
              <h2>Plant Health Distribution</h2>
              {healthTotal > 0 ? (
                <div className="donut-layout">
                  <div className="donut">
                    <div>
                      <strong>{healthTotal}</strong>
                      <small>Plants</small>
                    </div>
                  </div>
                  <ul>
                    <li>
                      <i className="healthy" /> Healthy <b>{summary?.health.healthy}</b>
                    </li>
                    <li>
                      <i className="warning" /> Warning <b>{summary?.health.warning}</b>
                    </li>
                    <li>
                      <i className="critical" /> Critical <b>{summary?.health.critical}</b>
                    </li>
                  </ul>
                </div>
              ) : (
                <EmptyPanel
                  title="No health distribution yet"
                  message="Health bands will calculate after plants have expected and actual telemetry readings."
                />
              )}
            </article>

            <article className="panel anomalies">
              <div className="panel-heading">
                <h2>Recent Anomalies</h2>
                <button disabled>View All</button>
              </div>
              <EmptyPanel
                title="Anomaly module pending"
                message="No anomaly records are stored yet. This panel will populate after the anomaly detection phase."
              />
            </article>

            <article className="panel plants">
              <div className="panel-heading">
                <h2>Top Plants by Performance</h2>
                <button disabled>View All</button>
              </div>
              {summary?.plants.length ? (
                <div className="plant-table">
                  <div className="table-head">
                    <span>Plant</span>
                    <span>Capacity</span>
                    <span>Current Gen</span>
                    <span>Performance</span>
                  </div>
                  {summary.plants.map((plant) => (
                    <div className="plant-row" key={plant.id}>
                      <b>{plant.name}</b>
                      <span>{plant.capacity_mw.toFixed(1)} MW</span>
                      <span>
                        {plant.current_generation_mw === null
                          ? "No telemetry"
                          : `${plant.current_generation_mw.toFixed(1)} MW`}
                      </span>
                      <span className="performance">
                        <em className={plant.performance_pct !== null && plant.performance_pct < 82 ? "amber" : ""}>
                          {plant.performance_pct === null ? "N/A" : `${plant.performance_pct.toFixed(1)}%`}
                        </em>
                        <i>
                          <u style={{ width: `${Math.min(plant.performance_pct ?? 0, 100)}%` }} />
                        </i>
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyPanel
                  title="No plants in PostgreSQL"
                  message="Create organization, site, and plant records to make this a populated operational dashboard."
                />
              )}
            </article>

            <article className="panel loss">
              <h2>
                Loss Breakdown <small>(not yet attributed)</small>
              </h2>
              <EmptyPanel
                title="Loss attribution pending"
                message="The foundation reports generation gap only. Root-cause loss categories require the analytics phase."
              />
            </article>

            <article className="panel quick">
              <h2>Quick Actions</h2>
              <div className="quick-grid">
                <button disabled>
                  <Upload /> Upload Plant Data
                </button>
                <button disabled>
                  <Sparkles /> Run AI Analysis
                </button>
                <button disabled>
                  <Wrench /> Create Maintenance
                </button>
                <button disabled>
                  <Bot /> Open AI Copilot
                </button>
              </div>
            </article>

            <article className="promo">
              <div>
                <b>
                  AI-Powered
                  <br />
                  Solar Operations
                </b>
                <p>Detect. Diagnose. Recover.</p>
                <small>Maximize Every Ray.</small>
              </div>
            </article>
          </section>
        </div>
      </section>
      <footer className="loop">
        <span>Observe</span>
        <b>-</b>
        <span>Model</span>
        <b>-</b>
        <span>Detect</span>
        <b>-</b>
        <span>Explain</span>
        <b>-</b>
        <span>Quantify</span>
        <b>-</b>
        <span>Simulate</span>
        <b>-</b>
        <span>Act</span>
        <b>-</b>
        <span>Measure</span>
        <b>-</b>
        <span>Learn</span>
      </footer>
    </main>
  );
}
