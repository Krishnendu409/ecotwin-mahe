#!/usr/bin/env python3
"""
Builds the self-contained, zero-broken-dependency Flagship Web Application
`index.html` for EcoTwin-MAHE with embedded simulation data from
`data/mit_manipal_digital_twin_data.json`.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "mit_manipal_digital_twin_data.json"
OUT_HTML = BASE_DIR / "index.html"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    twin_data = json.load(f)

json_payload = json.dumps(twin_data)

html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EcoTwin-MAHE | AI, CFD-Surrogate & GIS Digital Twin — MIT Manipal (CHEMIGNITE 2026)</title>
  <!-- Leaflet GIS CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg-primary: #070B14;
      --bg-card: #0F172A;
      --bg-card-alt: #1E293B;
      --border-col: #334155;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --accent-teal: #10B981;
      --accent-cyan: #06B6D4;
      --accent-blue: #3B82F6;
      --accent-amber: #F59E0B;
      --accent-rose: #F43F5E;
      --accent-purple: #A855F7;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: radial-gradient(circle at 15% 15%, #0F172A 0%, #070B14 70%);
      color: var(--text-main);
      min-height: 100vh;
      overflow-x: hidden;
    }
    /* Top Header */
    .top-banner {
      background: linear-gradient(90deg, rgba(16,185,129,0.14) 0%, rgba(6,182,212,0.14) 50%, rgba(168,85,247,0.14) 100%);
      border-bottom: 1px solid var(--border-col);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .brand-logo {
      width: 44px;
      height: 44px;
      border-radius: 11px;
      background: linear-gradient(135deg, #10B981, #06B6D4);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 18px;
      color: #070B14;
      box-shadow: 0 0 20px rgba(16,185,129,0.4);
    }
    .brand-title h1 {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.3px;
      background: linear-gradient(90deg, #F8FAFC, #38BDF8, #34D399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-title p {
      font-size: 12px;
      color: var(--text-muted);
    }
    .badge-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }
    .pill-badge {
      font-size: 11px;
      font-weight: 600;
      padding: 5px 10px;
      border-radius: 999px;
      background: rgba(30,41,59,0.85);
      border: 1px solid var(--border-col);
      color: #E2E8F0;
    }
    .pill-badge.emerald { border-color: #10B981; color: #6EE7B7; background: rgba(16,185,129,0.12); }
    .pill-badge.cyan { border-color: #06B6D4; color: #67E8F9; background: rgba(6,182,212,0.12); }
    .pill-badge.amber { border-color: #F59E0B; color: #FCD34D; background: rgba(245,158,11,0.12); }

    /* Campus KPI Strip */
    .kpi-strip {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 12px;
      padding: 14px 24px;
      background: rgba(15,23,42,0.65);
      border-bottom: 1px solid rgba(51,65,85,0.6);
    }
    @media (max-width: 1200px) {
      .kpi-strip { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 700px) {
      .kpi-strip { grid-template-columns: repeat(2, 1fr); }
    }
    .kpi-box {
      background: rgba(30,41,59,0.55);
      border: 1px solid rgba(71,85,105,0.45);
      border-radius: 10px;
      padding: 10px 14px;
      position: relative;
      overflow: hidden;
    }
    .kpi-box::before {
      content: "";
      position: absolute;
      left: 0; top: 0; bottom: 0;
      width: 4px;
      background: var(--accent-teal);
    }
    .kpi-box.cyan::before { background: var(--accent-cyan); }
    .kpi-box.amber::before { background: var(--accent-amber); }
    .kpi-box.purple::before { background: var(--accent-purple); }
    .kpi-box.blue::before { background: var(--accent-blue); }
    .kpi-box.rose::before { background: var(--accent-rose); }
    .kpi-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      font-weight: 600;
    }
    .kpi-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 20px;
      font-weight: 700;
      color: #F8FAFC;
      margin-top: 3px;
    }
    .kpi-sub {
      font-size: 11px;
      color: #34D399;
      margin-top: 2px;
      font-weight: 500;
    }

    /* Navigation Tabs */
    .nav-tabs {
      display: flex;
      gap: 8px;
      padding: 12px 24px 0 24px;
      border-bottom: 1px solid var(--border-col);
      background: #0B1120;
      overflow-x: auto;
    }
    .tab-btn {
      background: rgba(30,41,59,0.5);
      color: var(--text-muted);
      border: 1px solid var(--border-col);
      border-bottom: none;
      padding: 11px 18px;
      border-radius: 10px 10px 0 0;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tab-btn:hover {
      color: #F8FAFC;
      background: rgba(51,65,85,0.5);
    }
    .tab-btn.active {
      background: var(--bg-card);
      color: #38BDF8;
      border-color: #38BDF8;
      box-shadow: 0 -3px 12px rgba(56,189,248,0.15);
    }
    .tab-num {
      background: rgba(56,189,248,0.18);
      color: #38BDF8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 5px;
    }

    /* Main Content Panels */
    .tab-panel {
      display: none;
      padding: 20px 24px 40px 24px;
      max-width: 1650px;
      margin: 0 auto;
    }
    .tab-panel.active {
      display: block;
    }
    .grid-2col {
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 18px;
    }
    .grid-3col {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }
    @media (max-width: 1150px) {
      .grid-2col, .grid-3col { grid-template-columns: 1fr; }
    }
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-col);
      border-radius: 12px;
      padding: 16px 18px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 1px solid rgba(51,65,85,0.6);
      flex-wrap: wrap;
      gap: 8px;
    }
    .card-title {
      font-size: 14.5px;
      font-weight: 700;
      color: #F8FAFC;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .card-subtitle {
      font-size: 11.5px;
      color: var(--text-muted);
    }

    /* Building Selector Pills */
    .building-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 14px;
    }
    .b-pill {
      padding: 6px 11px;
      font-size: 11.5px;
      font-weight: 600;
      border-radius: 8px;
      background: var(--bg-card-alt);
      border: 1px solid var(--border-col);
      color: #CBD5E1;
      cursor: pointer;
      transition: all 0.15s;
    }
    .b-pill:hover {
      border-color: #38BDF8;
      color: #F8FAFC;
    }
    .b-pill.active {
      background: linear-gradient(135deg, rgba(16,185,129,0.25), rgba(6,182,212,0.28));
      border-color: #10B981;
      color: #6EE7B7;
      box-shadow: 0 0 12px rgba(16,185,129,0.25);
    }

    /* Map & 3D Isometric Twin Container */
    .twin-viewport-grid {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 14px;
    }
    @media (max-width: 900px) {
      .twin-viewport-grid { grid-template-columns: 1fr; }
    }
    #manipal-map {
      width: 100%;
      height: 410px;
      border-radius: 10px;
      border: 1px solid var(--border-col);
      z-index: 2;
    }
    #iso-building-canvas {
      width: 100%;
      height: 410px;
      background: radial-gradient(circle at 50% 35%, #1E293B 0%, #090D16 100%);
      border-radius: 10px;
      border: 1px solid var(--border-col);
      display: block;
    }

    /* Retrofit Checkboxes */
    .retrofit-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 8px;
    }
    .retrofit-item {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
      padding: 10px 12px;
      border-radius: 9px;
      background: rgba(30,41,59,0.65);
      border: 1px solid rgba(71,85,105,0.5);
      cursor: pointer;
      transition: all 0.15s;
    }
    .retrofit-item.checked {
      background: rgba(16,185,129,0.12);
      border-color: #10B981;
    }
    .retrofit-left {
      display: flex;
      align-items: flex-start;
      gap: 10px;
    }
    .retrofit-left input[type="checkbox"] {
      margin-top: 3px;
      width: 16px;
      height: 16px;
      accent-color: #10B981;
      cursor: pointer;
    }
    .r-title {
      font-size: 12.5px;
      font-weight: 700;
      color: #F8FAFC;
    }
    .r-desc {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .r-mentor {
      font-size: 10.5px;
      color: #38BDF8;
      margin-top: 2px;
      font-weight: 600;
    }
    .r-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 7px;
      border-radius: 6px;
      background: rgba(15,23,42,0.8);
      color: #34D399;
      white-space: nowrap;
    }

    /* Metrics Mini Grid */
    .metric-mini-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin: 12px 0;
    }
    @media (max-width: 650px) {
      .metric-mini-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .m-card {
      background: rgba(15,23,42,0.85);
      border: 1px solid rgba(71,85,105,0.5);
      padding: 10px;
      border-radius: 8px;
    }
    .m-card .lbl { font-size: 10.5px; color: var(--text-muted); font-weight: 600; }
    .m-card .val { font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: #F8FAFC; margin-top: 3px; }
    .m-card .delta { font-size: 10.5px; color: #34D399; margin-top: 2px; }

    /* Sliders */
    .slider-group {
      margin-bottom: 14px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 12.5px;
      font-weight: 600;
      margin-bottom: 5px;
      color: #E2E8F0;
    }
    .slider-val {
      font-family: 'JetBrains Mono', monospace;
      color: #38BDF8;
      font-weight: 700;
    }
    input[type="range"] {
      width: 100%;
      accent-color: #06B6D4;
      cursor: pointer;
    }

    /* CFD Canvas */
    #cfd-streamline-canvas {
      width: 100%;
      height: 360px;
      background: #070B14;
      border-radius: 10px;
      border: 1px solid var(--border-col);
      display: block;
    }

    /* Tables */
    .table-wrap {
      overflow-x: auto;
      margin-top: 10px;
    }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    table.data-table th, table.data-table td {
      padding: 9px 10px;
      text-align: left;
      border-bottom: 1px solid rgba(51,65,85,0.5);
    }
    table.data-table th {
      background: rgba(30,41,59,0.9);
      color: #94A3B8;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 10.5px;
      letter-spacing: 0.4px;
    }
    table.data-table tr:hover {
      background: rgba(56,189,248,0.06);
    }
    .lvl-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      display: inline-block;
    }
    .lvl-0 { background: rgba(100,116,139,0.25); color: #94A3B8; }
    .lvl-1 { background: rgba(56,189,248,0.2); color: #7DD3FC; }
    .lvl-2 { background: rgba(20,184,166,0.22); color: #5EEAD4; }
    .lvl-3 { background: rgba(16,185,129,0.25); color: #6EE7B7; }
    .lvl-4 { background: rgba(168,85,247,0.25); color: #D8B4FE; }
    .lvl-5 { background: linear-gradient(90deg, rgba(16,185,129,0.35), rgba(6,182,212,0.35)); color: #A7F3D0; border: 1px solid #10B981; }

    .btn-action {
      background: linear-gradient(135deg, #10B981, #06B6D4);
      color: #070B14;
      border: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: opacity 0.15s;
    }
    .btn-action:hover { opacity: 0.9; }
    .btn-secondary {
      background: rgba(30,41,59,0.9);
      color: #E2E8F0;
      border: 1px solid var(--border-col);
      padding: 7px 12px;
      border-radius: 8px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
    }
    .btn-secondary:hover { border-color: #38BDF8; color: #38BDF8; }

    .chart-box {
      position: relative;
      height: 270px;
      width: 100%;
    }
  </style>
</head>
<body>

  <!-- TOP HEADER BANNER -->
  <header class="top-banner">
    <div class="brand-wrap">
      <div class="brand-logo">ET</div>
      <div class="brand-title">
        <h1>EcoTwin-MAHE : AI, CFD-Surrogate &amp; GIS Campus Digital Twin</h1>
        <p>Low-Carbon Geopolymer Retrofits, Rooftop Solar-H₂ Microgrids &amp; Monsoon Rainwater Circularity at MIT Manipal</p>
      </div>
    </div>
    <div class="badge-row">
      <span class="pill-badge emerald">CHEMIGNITE 2026 — ASPIRE Hackathon</span>
      <span class="pill-badge cyan">Innovation Centre MAHE &amp; SCCE MIT Manipal</span>
      <span class="pill-badge amber">12 Campus Buildings Live Twin</span>
    </div>
  </header>

  <!-- CAMPUS-WIDE KPI STRIP -->
  <section class="kpi-strip">
    <div class="kpi-box">
      <div class="kpi-label">Cooling Energy Saved</div>
      <div class="kpi-val" id="kpi-cooling-saved">10,121.9 MWh/yr</div>
      <div class="kpi-sub" id="kpi-cooling-pct">-75.5% Campus HVAC Reduction</div>
    </div>
    <div class="kpi-box cyan">
      <div class="kpi-label">Geopolymer Embodied CO₂</div>
      <div class="kpi-val" id="kpi-embodied-co2">3,101.3 tCO₂e</div>
      <div class="kpi-sub">Fly-Ash/GGBFS + E-Waste vs OPC</div>
    </div>
    <div class="kpi-box purple">
      <div class="kpi-label">Operational Carbon Abated</div>
      <div class="kpi-val" id="kpi-op-co2">11,141.1 tCO₂e/yr</div>
      <div class="kpi-sub">225,923 tCO₂e over 20-Yr Horizon</div>
    </div>
    <div class="kpi-box blue">
      <div class="kpi-label">Monsoon RWH + Greywater</div>
      <div class="kpi-val" id="kpi-water-suff">75.9% Self-Suff.</div>
      <div class="kpi-sub">164,421 m³ RWH + 66,769 m³ Recharge</div>
    </div>
    <div class="kpi-box amber">
      <div class="kpi-label">Solar BIPV + PEM H₂ Buffer</div>
      <div class="kpi-val" id="kpi-solar-kwp">3,040.2 kWp</div>
      <div class="kpi-sub">4,826.8 MWh/yr + 6,565 kg Green H₂</div>
    </div>
    <div class="kpi-box rose">
      <div class="kpi-label">20-Yr Campus Masterplan NPV</div>
      <div class="kpi-val" id="kpi-npv">+₹13.19 Cr</div>
      <div class="kpi-sub">CAPEX ₹4.79 Cr | Payback 2.72 Yrs</div>
    </div>
  </section>

  <!-- NAVIGATION TABS -->
  <nav class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab(1)" id="tab-btn-1">
      <span class="tab-num">01</span> 3D Campus Digital Twin &amp; Building Inspector
    </button>
    <button class="tab-btn" onclick="switchTab(2)" id="tab-btn-2">
      <span class="tab-num">02</span> CFD Airflow &amp; Geopolymer Envelope Lab
    </button>
    <button class="tab-btn" onclick="switchTab(3)" id="tab-btn-3">
      <span class="tab-num">03</span> GIS Monsoon Rainwater &amp; Greywater Network
    </button>
    <button class="tab-btn" onclick="switchTab(4)" id="tab-btn-4">
      <span class="tab-num">04</span> AI NSGA-II Budget Pareto Optimizer &amp; ROI
    </button>
  </nav>

  <!-- ==================================================================== -->
  <!-- TAB 1: 3D CAMPUS DIGITAL TWIN & BUILDING INSPECTOR                   -->
  <!-- ==================================================================== -->
  <main class="tab-panel active" id="tab-panel-1">
    <div class="building-pills" id="building-selector-bar"></div>

    <div class="grid-2col">
      <!-- Left Column: Geospatial Map + 3D Isometric Building Renderer -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">MIT Manipal Geospatial GIS &amp; 3D Isometric Building Digital Twin</div>
            <div class="card-subtitle">Click any building polygon on the map or inspect the live 3D thermal/solar/RWH digital twin</div>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="btn-secondary" onclick="selectAllRetrofits(true)">Enable All 5 Retrofits</button>
            <button class="btn-secondary" onclick="selectAllRetrofits(false)">Reset to Baseline</button>
          </div>
        </div>

        <div class="twin-viewport-grid">
          <div id="manipal-map"></div>
          <div style="position:relative;">
            <canvas id="iso-building-canvas" width="520" height="410"></canvas>
            <div style="position:absolute; top:10px; left:12px; background:rgba(15,23,42,0.85); border:1px solid #334155; padding:6px 10px; border-radius:8px; font-size:11px;">
              <div style="color:#38BDF8; font-weight:700;" id="iso-b-name">AB-2 (Sir M.V. Hall)</div>
              <div style="color:#94A3B8;" id="iso-b-tag">CHEMIGNITE Main Conference Venue</div>
            </div>
          </div>
        </div>

        <!-- Monthly Cooling vs Solar Generation Chart for Selected Building -->
        <div style="margin-top:16px;">
          <div class="card-header" style="margin-bottom:8px; padding-bottom:6px;">
            <div class="card-title" style="font-size:13px;">12-Month Cooling Demand (Baseline vs. Active Retrofits) &amp; Rooftop Solar PV Yield</div>
            <span class="pill-badge emerald" id="b-Venue-Badge">Coordinates: 13.3526° N, 74.7928° E</span>
          </div>
          <div class="chart-box" style="height:230px;">
            <canvas id="chart-b-monthly-energy"></canvas>
          </div>
        </div>
      </div>

      <!-- Right Column: Building Inspector & Live Passive Solar / Geopolymer Retrofit Toggles -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title" id="inspector-title">Academic Block 2 (AB-2 — Sir M.V. Seminar Hall)</div>
            <div class="card-subtitle" id="inspector-meta">GFA: 18,200 m² | Roof: 4,850 m² | Floors: 4 | Occupancy: 2,400</div>
          </div>
          <span class="pill-badge cyan" id="inspector-category">Academic &amp; Conference</span>
        </div>

        <!-- 8 Live Building Metrics -->
        <div class="metric-mini-grid">
          <div class="m-card">
            <div class="lbl">Annual Cooling Load</div>
            <div class="val" id="insp-cooling-mwh">288.4 MWh</div>
            <div class="delta" id="insp-cooling-delta">-75.7% vs Base</div>
          </div>
          <div class="m-card">
            <div class="lbl">Peak Cooling Demand</div>
            <div class="val" id="insp-peak-kwe">148.2 kWe</div>
            <div class="delta" id="insp-peak-delta">-398.5 kWe Clipped</div>
          </div>
          <div class="m-card">
            <div class="lbl">ASHRAE-55 Comfort</div>
            <div class="val" id="insp-pmv">PMV -0.01</div>
            <div class="delta" id="insp-ppd">PPD 5.0% (Compliant)</div>
          </div>
          <div class="m-card">
            <div class="lbl">Roof Sol-Air Peak</div>
            <div class="val" id="insp-sol-air">35.0 °C</div>
            <div class="delta" id="insp-sol-air-delta">-18.9 °C Roof Cool</div>
          </div>
          <div class="m-card">
            <div class="lbl">Embodied CO₂ Saved</div>
            <div class="val" id="insp-emb-co2">295.4 tCO₂</div>
            <div class="delta">Geopolymer vs OPC</div>
          </div>
          <div class="m-card">
            <div class="lbl">Monsoon RWH Harvest</div>
            <div class="val" id="insp-rwh-m3">15,791 m³</div>
            <div class="delta" id="insp-water-ss">72.0% Water Self-Suff.</div>
          </div>
          <div class="m-card">
            <div class="lbl">Rooftop Bifacial PV</div>
            <div class="val" id="insp-solar-kwp">292.0 kWp</div>
            <div class="delta" id="insp-solar-mwh">463.5 MWh/yr</div>
          </div>
          <div class="m-card">
            <div class="lbl">Active Package CAPEX</div>
            <div class="val" id="insp-capex">₹43.8 L</div>
            <div class="delta" id="insp-payback">Payback: 2.65 Yrs</div>
          </div>
        </div>

        <div style="font-size:12.5px; font-weight:700; color:#38BDF8; margin: 10px 0 6px 0;">
          Module 1 Interactive Retrofit Toggles (Prof. Rajiv Gupta &amp; Dr. Shreelaxmi Prashanth Alignment):
        </div>

        <div class="retrofit-list" id="retrofit-toggles-container"></div>
      </div>
    </div>
  </main>

  <!-- ==================================================================== -->
  <!-- TAB 2: CFD AIRFLOW & GEOPOLYMER ENVELOPE LAB                         -->
  <!-- ==================================================================== -->
  <main class="tab-panel" id="tab-panel-2">
    <div class="grid-2col">
      <!-- Left: Live Animated PINN-CFD Indoor Velocity & Temperature Field -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Module 2: PINN-CFD Surrogate Indoor Airflow &amp; Thermal Comfort Visualizer</div>
            <div class="card-subtitle"> Strategic Alignment: Dr. Mohammad Zuber (Chief Innovation Officer, Innovation Centre MAHE)</div>
          </div>
          <span class="pill-badge emerald" id="cfd-compliance-badge">ASHRAE-55 Class A Comfort</span>
        </div>

        <canvas id="cfd-streamline-canvas" width="760" height="360"></canvas>

        <div class="metric-mini-grid" style="margin-top:14px;">
          <div class="m-card">
            <div class="lbl">Mean Indoor Air Speed</div>
            <div class="val" id="cfd-vel-val">0.76 m/s</div>
            <div class="delta">Coastal Sea-Breeze Jet</div>
          </div>
          <div class="m-card">
            <div class="lbl">Air Changes / Hour</div>
            <div class="val" id="cfd-ach-val">11.4 ACH</div>
            <div class="delta">Hybrid Cross-Ventilation</div>
          </div>
          <div class="m-card">
            <div class="lbl">Operative Temp (T_op)</div>
            <div class="val" id="cfd-top-val">26.76 °C</div>
            <div class="delta" id="cfd-mrt-val">T_mrt: 26.80 °C</div>
          </div>
          <div class="m-card">
            <div class="lbl">Fanger PMV / PPD</div>
            <div class="val" id="cfd-pmv-val">-0.01</div>
            <div class="delta" id="cfd-ppd-val">PPD: 5.0% Dissatisfied</div>
          </div>
        </div>
      </div>

      <!-- Right: Parametric Boundary Conditions & Geopolymer Low-Carbon Material Lab -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Coastal Microclimate &amp; Alkali-Activated Geopolymer Lab</div>
            <div class="card-subtitle">Dr. Shreelaxmi Prashanth, Dr. Amit Kumar &amp; Prof. Rajiv Gupta Alignment</div>
          </div>
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Arabian Sea Breeze Wind Speed (W-SW 10m)</span>
            <span class="slider-val" id="lbl-wind-speed">3.8 m/s</span>
          </div>
          <input type="range" id="sld-wind-speed" min="1.0" max="6.5" step="0.2" value="3.8" oninput="updateCfdParametric()" />
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Manipal Outdoor Daytime Temperature (T_amb)</span>
            <span class="slider-val" id="lbl-amb-temp">32.2 °C</span>
          </div>
          <input type="range" id="sld-amb-temp" min="26.0" max="37.0" step="0.2" value="32.2" oninput="updateCfdParametric()" />
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Coastal Relative Humidity (RH %)</span>
            <span class="slider-val" id="lbl-amb-rh">74 %</span>
          </div>
          <input type="range" id="sld-amb-rh" min="50" max="95" step="1" value="74" oninput="updateCfdParametric()" />
        </div>

        <div class="slider-group">
          <div class="slider-header">
            <span>Geopolymer Binder Replacement (UPCL Fly Ash + GGBFS + E-Waste %)</span>
            <span class="slider-val" id="lbl-geo-blend">85 % OPC Replaced</span>
          </div>
          <input type="range" id="sld-geo-blend" min="40" max="95" step="5" value="85" oninput="updateCfdParametric()" />
        </div>

        <div class="chart-box" style="height:225px; margin-top:10px;">
          <canvas id="chart-cfd-pmv-comparison"></canvas>
        </div>
      </div>
    </div>
  </main>

  <!-- ==================================================================== -->
  <!-- TAB 3: GIS MONSOON RAINWATER & GREYWATER NETWORK                     -->
  <!-- ==================================================================== -->
  <main class="tab-panel" id="tab-panel-3">
    <div class="grid-2col">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Module 3: Udupi/Manipal Monsoon Hydrology (3,954 mm/yr) &amp; Laterite Aquifer Recharge</div>
            <div class="card-subtitle">Strategic Alignment: Prof. Rajiv Gupta (GIS RWH) &amp; Dr. K. Balakrishna (Coastal Hydrogeochemistry)</div>
          </div>
          <span class="pill-badge cyan">164,421 m³/yr Roof Runoff Harvested</span>
        </div>
        <div class="chart-box" style="height:300px;">
          <canvas id="chart-monsoon-hydrology"></canvas>
        </div>
        <div class="metric-mini-grid" style="margin-top:14px;">
          <div class="m-card">
            <div class="lbl">Annual Monsoon Rain</div>
            <div class="val">3,954 mm</div>
            <div class="delta">Jun–Sep 89% Concentrated</div>
          </div>
          <div class="m-card">
            <div class="lbl">Roof RWH Harvested</div>
            <div class="val">164,421 m³</div>
            <div class="delta">50,500 m² Catchment</div>
          </div>
          <div class="m-card">
            <div class="lbl">Laterite Recharge Pits</div>
            <div class="val">66,769 m³</div>
            <div class="delta">K_sat = 1.85 m/day Vadose</div>
          </div>
          <div class="m-card">
            <div class="lbl">Biochar Wetland Reuse</div>
            <div class="val">275,037 m³</div>
            <div class="delta">91% BOD/COD Removal</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Building-Wise RWH Cisterns, Laterite Pits &amp; Hostel/Mess Circularity</div>
            <div class="card-subtitle">Includes Hostel Blocks 16/17 &amp; 10 Greywater + Food Court 1 &amp; 2 Anaerobic Biogas</div>
          </div>
        </div>
        <div class="chart-box" style="height:260px;">
          <canvas id="chart-building-water"></canvas>
        </div>
        <div class="table-wrap" style="max-height:195px; overflow-y:auto;">
          <table class="data-table" id="water-building-table">
            <thead>
              <tr>
                <th>Building</th>
                <th>Roof (m²)</th>
                <th>RWH Yield (m³/yr)</th>
                <th>Cistern (m³)</th>
                <th>Greywater Reuse (m³/yr)</th>
                <th>Self-Suff. (%)</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>
  </main>

  <!-- ==================================================================== -->
  <!-- TAB 4: AI NSGA-II BUDGET PARETO OPTIMIZER & ROI                      -->
  <!-- ==================================================================== -->
  <main class="tab-panel" id="tab-panel-4">
    <div class="grid-2col">
      <!-- Left: Interactive Budget Slider + NSGA-II Pareto Front Chart -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">Module 4: AI NSGA-II Multi-Objective Campus Budget Pareto Optimizer</div>
            <div class="card-subtitle">Strategic Alignment: Prof. Kishalay Mitra (Multi-Objective Pareto Optimization under Uncertainty)</div>
          </div>
          <button class="btn-action" onclick="exportMasterplanJSON()">Download Optimal Masterplan JSON</button>
        </div>

        <div class="slider-group" style="background:rgba(30,41,59,0.7); padding:12px 14px; border-radius:10px; border:1px solid #38BDF8;">
          <div class="slider-header" style="font-size:14px;">
            <span>Select Campus Sustainability Capital Budget Constraint:</span>
            <span class="slider-val" id="lbl-budget-slider" style="font-size:17px; color:#34D399;">₹2.50 Crores (₹250 Lakhs)</span>
          </div>
          <input type="range" id="sld-campus-budget" min="25" max="500" step="25" value="250" oninput="updateNsga2BudgetOptimizer()" />
          <div style="display:flex; justify-content:space-between; font-size:10.5px; color:#94A3B8; margin-top:4px;">
            <span>₹0.25 Cr (Seed Pilot)</span>
            <span>₹1.50 Cr (Phase 1)</span>
            <span>₹2.50 Cr (Pareto Knee)</span>
            <span>₹3.75 Cr (Phase 2)</span>
            <span>₹5.00 Cr (Full Net-Zero)</span>
          </div>
        </div>

        <div class="metric-mini-grid">
          <div class="m-card">
            <div class="lbl">Optimal CAPEX Used</div>
            <div class="val" id="opt-capex-used">₹2.48 Cr</div>
            <div class="delta" id="opt-payback">Payback: 2.58 Yrs</div>
          </div>
          <div class="m-card">
            <div class="lbl">Carbon Abatement</div>
            <div class="val" id="opt-co2-abated">7,217 t/yr</div>
            <div class="delta" id="opt-emb-co2">+2,140 t Embodied</div>
          </div>
          <div class="m-card">
            <div class="lbl">Water Circularity</div>
            <div class="val" id="opt-water-pct">72.4 %</div>
            <div class="delta" id="opt-water-m3">328,400 m³/yr</div>
          </div>
          <div class="m-card">
            <div class="lbl">20-Yr Net Present Value</div>
            <div class="val" id="opt-npv-cr">+₹8.46 Cr</div>
            <div class="delta" id="opt-ann-sav">Savings: ₹1.07 Cr/yr</div>
          </div>
        </div>

        <div class="chart-box" style="height:265px;">
          <canvas id="chart-nsga2-pareto"></canvas>
        </div>
      </div>

      <!-- Right: Building-by-Building NSGA-II Optimal Allocation Table -->
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">NSGA-II Optimal Building-by-Building Intervention Schedule</div>
            <div class="card-subtitle">Chromosome Decision Allocation across all 12 MIT Manipal Buildings for Selected Budget</div>
          </div>
          <span class="pill-badge emerald" id="opt-mean-pmv-badge">Campus Mean PMV: +0.08</span>
        </div>

        <div class="table-wrap" style="max-height:495px; overflow-y:auto;">
          <table class="data-table" id="nsga2-allocation-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>MIT Manipal Building</th>
                <th>Assigned Tier</th>
                <th>Intervention Package</th>
                <th>CAPEX (₹ L)</th>
                <th>Savings (₹ L/yr)</th>
                <th>CO₂ Abated (t/yr)</th>
                <th>PMV</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>
  </main>

  <!-- EMBEDDED SIMULATION DATASET -->
  <script id="ecotwin-data" type="application/json">__JSON_PAYLOAD__</script>

  <script>
    // Parse embedded dataset
    const TWIN_DATA = JSON.parse(document.getElementById('ecotwin-data').textContent);
    const BUILDINGS = TWIN_DATA.buildings;
    const RETROFITS = TWIN_DATA.retrofit_packages;
    const CLIMATE = TWIN_DATA.climate_monthly;
    const NSGA2 = TWIN_DATA.nsga2_optimization;

    // Application State
    let selectedBuildingIdx = 0;
    let activeRetrofits = new Set(Object.keys(RETROFITS)); // Start with all 5 active to showcase full impact
    let mapInstance = null;
    let mapPolygons = [];
    let chartMonthlyEnergy = null;
    let chartCfdPmv = null;
    let chartMonsoon = null;
    let chartBuildingWater = null;
    let chartPareto = null;

    // Tab Switching
    function switchTab(tabNum) {
      document.querySelectorAll('.tab-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', (idx + 1) === tabNum);
      });
      document.querySelectorAll('.tab-panel').forEach((panel, idx) => {
        panel.classList.toggle('active', (idx + 1) === tabNum);
      });
      if (tabNum === 1 && mapInstance) {
        setTimeout(() => mapInstance.invalidateSize(), 150);
      }
      if (tabNum === 2) {
        updateCfdParametric();
      }
      if (tabNum === 3) {
        renderWaterCharts();
      }
      if (tabNum === 4) {
        updateNsga2BudgetOptimizer();
      }
    }

    // Initialize Building Pills
    function initBuildingPills() {
      const bar = document.getElementById('building-selector-bar');
      bar.innerHTML = '';
      BUILDINGS.forEach((b, idx) => {
        const btn = document.createElement('button');
        btn.className = 'b-pill' + (idx === selectedBuildingIdx ? ' active' : '');
        btn.textContent = `${b.id}: ${b.short_name}`;
        btn.onclick = () => selectBuilding(idx);
        bar.appendChild(btn);
      });
    }

    function selectBuilding(idx) {
      selectedBuildingIdx = idx;
      document.querySelectorAll('.b-pill').forEach((el, i) => {
        el.classList.toggle('active', i === idx);
      });
      const b = BUILDINGS[idx];
      if (mapInstance) {
        mapInstance.panTo([b.lat, b.lon], { animate: true });
      }
      highlightMapPolygon(idx);
      updateBuildingInspector();
      drawIsometricBuilding();
      if (document.getElementById('tab-panel-2').classList.contains('active')) {
        updateCfdParametric();
      }
    }

    // Initialize Leaflet Map of MIT Manipal
    function initManipalMap() {
      mapInstance = L.map('manipal-map', {
        center: [13.3518, 74.7924],
        zoom: 16,
        zoomControl: true
      });

      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO | EcoTwin-MAHE MIT Manipal',
        maxZoom: 19
      }).addTo(mapInstance);

      mapPolygons = [];
      BUILDINGS.forEach((b, idx) => {
        const coords = b.polygon_offset.map(off => [b.lat + off[0], b.lon + off[1]]);
        const isSelected = idx === selectedBuildingIdx;
        const poly = L.polygon(coords, {
          color: isSelected ? '#10B981' : '#38BDF8',
          weight: isSelected ? 3 : 1.8,
          fillColor: isSelected ? '#10B981' : '#0284C7',
          fillOpacity: isSelected ? 0.55 : 0.32
        }).addTo(mapInstance);

        poly.bindTooltip(
          `<b>${b.short_name}</b><br/>${b.highlight_tag}<br/>Cooling Drop: -${b.cooling_saved_pct}% | RWH: ${b.water_circularity.annual_rwh_harvested_m3.toLocaleString()} m³/yr`,
          { sticky: true }
        );
        poly.on('click', () => selectBuilding(idx));
        mapPolygons.push(poly);
      });
    }

    function highlightMapPolygon(selectedIdx) {
      mapPolygons.forEach((poly, i) => {
        const isSel = i === selectedIdx;
        poly.setStyle({
          color: isSel ? '#10B981' : '#38BDF8',
          weight: isSel ? 3 : 1.8,
          fillColor: isSel ? '#10B981' : '#0284C7',
          fillOpacity: isSel ? 0.55 : 0.32
        });
      });
    }

    // Initialize Retrofit Checkboxes
    function initRetrofitToggles() {
      const container = document.getElementById('retrofit-toggles-container');
      container.innerHTML = '';
      Object.entries(RETROFITS).forEach(([key, pkg]) => {
        const isChecked = activeRetrofits.has(key);
        const item = document.createElement('div');
        item.className = 'retrofit-item' + (isChecked ? ' checked' : '');
        item.onclick = (e) => {
          if (e.target.tagName !== 'INPUT') {
            const cb = item.querySelector('input');
            cb.checked = !cb.checked;
          }
          toggleRetrofitKey(key, item.querySelector('input').checked);
        };
        item.innerHTML = `
          <div class="retrofit-left">
            <input type="checkbox" ${isChecked ? 'checked' : ''} />
            <div>
              <div class="r-title">${pkg.code}: ${pkg.name}</div>
              <div class="r-desc">${pkg.description}</div>
              <div class="r-mentor">★ ${pkg.mentor_alignment}</div>
            </div>
          </div>
          <div class="r-tag" id="r-impact-${key}">Active</div>
        `;
        container.appendChild(item);
      });
    }

    function toggleRetrofitKey(key, enabled) {
      if (enabled) activeRetrofits.add(key);
      else activeRetrofits.delete(key);
      initRetrofitToggles();
      updateBuildingInspector();
      drawIsometricBuilding();
    }

    function selectAllRetrofits(enableAll) {
      if (enableAll) {
        activeRetrofits = new Set(Object.keys(RETROFITS));
      } else {
        activeRetrofits.clear();
      }
      initRetrofitToggles();
      updateBuildingInspector();
      drawIsometricBuilding();
    }

    // Dynamic Building Physics Interpolation from Precomputed Individual + Full Retrofits
    function computeActiveBuildingState(b) {
      const baseE = b.baseline_energy;
      const fullE = b.retrofitted_energy;
      const allKeys = Object.keys(RETROFITS);
      const count = activeRetrofits.size;

      if (count === 0) {
        return {
          annual_cooling_mwh: baseE.annual_cooling_mwh,
          peak_cooling_kwe: baseE.peak_cooling_kwe,
          monthly_cooling_mwh: baseE.monthly_cooling_mwh.slice(),
          peak_sol_air_c: baseE.peak_sol_air_roof_c,
          embodied_co2_t: 0.0,
          capex_lakhs: 0.0,
          pmv: b.baseline_cfd.pmv,
          ppd_pct: b.baseline_cfd.ppd_pct,
          t_op_c: b.baseline_cfd.t_operative_c,
          vel_ms: b.baseline_cfd.mean_velocity_ms,
          ach: b.baseline_cfd.ach
        };
      }
      if (count === allKeys.length) {
        return {
          annual_cooling_mwh: fullE.annual_cooling_mwh,
          peak_cooling_kwe: fullE.peak_cooling_kwe,
          monthly_cooling_mwh: fullE.monthly_cooling_mwh.slice(),
          peak_sol_air_c: fullE.peak_sol_air_roof_c,
          embodied_co2_t: fullE.embodied_co2_saved_t,
          capex_lakhs: b.financials_full_package.total_capex_lakhs,
          pmv: b.retrofitted_cfd.pmv,
          ppd_pct: b.retrofitted_cfd.ppd_pct,
          t_op_c: b.retrofitted_cfd.t_operative_c,
          vel_ms: b.retrofitted_cfd.mean_velocity_ms,
          ach: b.retrofitted_cfd.ach
        };
      }

      // Sum individual contributions normalized by synergy factor
      let sumIndivSaved = 0;
      let sumAllIndivSaved = 0;
      let sumIndivPeak = 0;
      let sumAllIndivPeak = 0;
      let embCo2 = 0;
      let capex = 0;

      allKeys.forEach(k => {
        const ind = b.individual_retrofits[k];
        sumAllIndivSaved += ind.cooling_saved_mwh;
        sumAllIndivPeak += ind.peak_saved_kwe;
        if (activeRetrofits.has(k)) {
          sumIndivSaved += ind.cooling_saved_mwh;
          sumIndivPeak += ind.peak_saved_kwe;
          embCo2 += ind.embodied_co2_saved_t;
          capex += ind.capex_lakhs;
        }
      });

      const fracEnergy = sumAllIndivSaved > 0 ? (sumIndivSaved / sumAllIndivSaved) : (count / 5.0);
      const fracPeak = sumAllIndivPeak > 0 ? (sumIndivPeak / sumAllIndivPeak) : (count / 5.0);

      const totalSavedMwh = (baseE.annual_cooling_mwh - fullE.annual_cooling_mwh) * fracEnergy;
      const totalSavedPeak = (baseE.peak_cooling_kwe - fullE.peak_cooling_kwe) * fracPeak;
      const curCoolingMwh = +(baseE.annual_cooling_mwh - totalSavedMwh).toFixed(1);
      const curPeakKwe = +(baseE.peak_cooling_kwe - totalSavedPeak).toFixed(1);

      const monthly = baseE.monthly_cooling_mwh.map((baseVal, m) => {
        const fullVal = fullE.monthly_cooling_mwh[m];
        return +(baseVal - (baseVal - fullVal) * fracEnergy).toFixed(2);
      });

      const solAir = activeRetrofits.has('R1_cool_roof') ? fullE.peak_sol_air_roof_c : baseE.peak_sol_air_roof_c;
      const pmv = +(b.baseline_cfd.pmv - (b.baseline_cfd.pmv - b.retrofitted_cfd.pmv) * fracEnergy).toFixed(2);
      const ppd = +(100.0 - 95.0 * Math.exp(-0.03353 * Math.pow(pmv, 4) - 0.2179 * Math.pow(pmv, 2))).toFixed(1);
      const tOp = +(b.baseline_cfd.t_operative_c - (b.baseline_cfd.t_operative_c - b.retrofitted_cfd.t_operative_c) * fracEnergy).toFixed(2);
      const vel = +(b.baseline_cfd.mean_velocity_ms + (b.retrofitted_cfd.mean_velocity_ms - b.baseline_cfd.mean_velocity_ms) * fracEnergy).toFixed(2);
      const ach = +(b.baseline_cfd.ach + (b.retrofitted_cfd.ach - b.baseline_cfd.ach) * fracEnergy).toFixed(1);

      return {
        annual_cooling_mwh: curCoolingMwh,
        peak_cooling_kwe: curPeakKwe,
        monthly_cooling_mwh: monthly,
        peak_sol_air_c: solAir,
        embodied_co2_t: +embCo2.toFixed(1),
        capex_lakhs: +(capex + b.water_circularity.total_water_capex_lakhs + b.solar_h2_microgrid.solar_capex_lakhs).toFixed(2),
        pmv: pmv,
        ppd_pct: ppd,
        t_op_c: tOp,
        vel_ms: vel,
        ach: ach
      };
    }

    function updateBuildingInspector() {
      const b = BUILDINGS[selectedBuildingIdx];
      const st = computeActiveBuildingState(b);
      const baseMwh = b.baseline_energy.annual_cooling_mwh;
      const dropPct = +(((baseMwh - st.annual_cooling_mwh) / baseMwh) * 100.0).toFixed(1);
      const peakClip = +(b.baseline_energy.peak_cooling_kwe - st.peak_cooling_kwe).toFixed(1);

      document.getElementById('inspector-title').textContent = b.name;
      document.getElementById('inspector-meta').textContent =
        `GFA: ${b.gross_floor_area_m2.toLocaleString()} m² | Roof: ${b.roof_area_m2.toLocaleString()} m² | Floors: ${b.floors} | Occupancy: ${b.occupancy.toLocaleString()}`;
      document.getElementById('inspector-category').textContent = b.category;
      document.getElementById('b-Venue-Badge').textContent = `${b.highlight_tag} (${b.lat}° N, ${b.lon}° E)`;
      document.getElementById('iso-b-name').textContent = `${b.id}: ${b.short_name}`;
      document.getElementById('iso-b-tag').textContent = b.highlight_tag;

      document.getElementById('insp-cooling-mwh').textContent = `${st.annual_cooling_mwh.toLocaleString()} MWh`;
      document.getElementById('insp-cooling-delta').textContent = `-${dropPct}% vs Base (${baseMwh} MWh)`;
      document.getElementById('insp-peak-kwe').textContent = `${st.peak_cooling_kwe} kWe`;
      document.getElementById('insp-peak-delta').textContent = `-${peakClip} kWe Clipped`;
      document.getElementById('insp-pmv').textContent = `PMV ${st.pmv >= 0 ? '+' : ''}${st.pmv}`;
      document.getElementById('insp-ppd').textContent = `PPD ${st.ppd_pct}% (${Math.abs(st.pmv) <= 0.5 ? 'ASHRAE Compliant' : 'Warm'})`;
      document.getElementById('insp-sol-air').textContent = `${st.peak_sol_air_c} °C`;
      document.getElementById('insp-sol-air-delta').textContent =
        activeRetrofits.has('R1_cool_roof') ? `-18.9 °C Cool Roof Drop` : `Uninsulated RCC Roof`;
      document.getElementById('insp-emb-co2').textContent = `${st.embodied_co2_t} tCO₂e`;
      document.getElementById('insp-rwh-m3').textContent = `${b.water_circularity.annual_rwh_harvested_m3.toLocaleString()} m³`;
      document.getElementById('insp-water-ss').textContent = `${b.water_circularity.water_self_sufficiency_pct}% Water Self-Suff.`;
      document.getElementById('insp-solar-kwp').textContent = `${b.solar_h2_microgrid.installed_solar_kwp} kWp`;
      document.getElementById('insp-solar-mwh').textContent = `${b.solar_h2_microgrid.annual_solar_generation_mwh} MWh/yr`;
      document.getElementById('insp-capex').textContent = `₹${st.capex_lakhs} L`;
      document.getElementById('insp-payback').textContent = `Payback: ${b.financials_full_package.simple_payback_years} Yrs`;

      // Update individual retrofit badge labels
      Object.keys(RETROFITS).forEach(k => {
        const badge = document.getElementById(`r-impact-${k}`);
        if (badge) {
          const ind = b.individual_retrofits[k];
          badge.textContent = `-${ind.cooling_saved_mwh} MWh | ₹${ind.capex_lakhs}L`;
        }
      });

      renderMonthlyEnergyChart(b, st);
    }

    function renderMonthlyEnergyChart(b, st) {
      const ctx = document.getElementById('chart-b-monthly-energy').getContext('2d');
      if (chartMonthlyEnergy) chartMonthlyEnergy.destroy();
      chartMonthlyEnergy = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: CLIMATE.months,
          datasets: [
            {
              label: 'Baseline Cooling (MWh)',
              data: b.baseline_energy.monthly_cooling_mwh,
              backgroundColor: 'rgba(249, 115, 22, 0.75)',
              borderRadius: 4
            },
            {
              label: 'Active Retrofit Cooling (MWh)',
              data: st.monthly_cooling_mwh,
              backgroundColor: 'rgba(16, 185, 129, 0.85)',
              borderRadius: 4
            },
            {
              label: 'Rooftop Bifacial Solar PV (MWh)',
              data: b.solar_h2_microgrid.monthly_solar_mwh,
              type: 'line',
              borderColor: '#38BDF8',
              backgroundColor: 'rgba(56, 189, 248, 0.2)',
              borderWidth: 2.5,
              tension: 0.35,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#CBD5E1', font: { size: 11 } } }
          },
          scales: {
            x: { ticks: { color: '#94A3B8' }, grid: { display: false } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(148,163,184,0.12)' }, title: { display: true, text: 'MWh / month', color: '#94A3B8' } }
          }
        }
      });
    }

    // =========================================================================
    // 3D ISOMETRIC BUILDING DIGITAL TWIN CANVAS RENDERER
    // =========================================================================
    function drawIsometricBuilding() {
      const canvas = document.getElementById('iso-building-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      ctx.clearRect(0, 0, W, H);

      const b = BUILDINGS[selectedBuildingIdx];
      const hasCoolRoof = activeRetrofits.has('R1_cool_roof');
      const hasGeoWall = activeRetrofits.has('R2_geopolymer_wall');
      const hasLouvers = activeRetrofits.has('R3_solar_louvers');
      const hasPcm = activeRetrofits.has('R4_pcm_ceiling');
      const hasSmartHvac = activeRetrofits.has('R5_smart_hvac_cfd');

      // Draw ground laterite & RWH recharge grid
      const cx = W * 0.5, cy = H * 0.68;
      const bw = 135, bd = 110;
      const floors = Math.min(7, Math.max(2, b.floors));
      const fh = 24;
      const totalH = floors * fh;

      // Isometric projection helper
      function iso(x, y, z) {
        return {
          x: cx + (x - y) * 0.866,
          y: cy + (x + y) * 0.5 - z
        };
      }

      // Ground pad (Coastal Laterite Aquifer Zone)
      const g0 = iso(-bw * 0.8, -bd * 0.8, 0);
      const g1 = iso(bw * 0.8, -bd * 0.8, 0);
      const g2 = iso(bw * 0.8, bd * 0.8, 0);
      const g3 = iso(-bw * 0.8, bd * 0.8, 0);
      ctx.beginPath();
      ctx.moveTo(g0.x, g0.y); ctx.lineTo(g1.x, g1.y); ctx.lineTo(g2.x, g2.y); ctx.lineTo(g3.x, g3.y);
      ctx.closePath();
      ctx.fillStyle = 'rgba(16, 185, 129, 0.10)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.35)';
      ctx.lineWidth = 1;
      ctx.stroke();

      // Left Wall (South-West Solar Exposed Facade)
      const p00 = iso(-bw/2, bd/2, 0);
      const p10 = iso(bw/2, bd/2, 0);
      const p11 = iso(bw/2, bd/2, totalH);
      const p01 = iso(-bw/2, bd/2, totalH);

      ctx.beginPath();
      ctx.moveTo(p00.x, p00.y); ctx.lineTo(p10.x, p10.y); ctx.lineTo(p11.x, p11.y); ctx.lineTo(p01.x, p01.y);
      ctx.closePath();
      ctx.fillStyle = hasGeoWall ? '#1E3A5F' : '#475569';
      ctx.fill();
      ctx.strokeStyle = hasGeoWall ? '#38BDF8' : '#64748B';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Right Wall (South-East Facade)
      const r00 = iso(bw/2, bd/2, 0);
      const r10 = iso(bw/2, -bd/2, 0);
      const r11 = iso(bw/2, -bd/2, totalH);
      const r01 = iso(bw/2, bd/2, totalH);

      ctx.beginPath();
      ctx.moveTo(r00.x, r00.y); ctx.lineTo(r10.x, r10.y); ctx.lineTo(r11.x, r11.y); ctx.lineTo(r01.x, r01.y);
      ctx.closePath();
      ctx.fillStyle = hasGeoWall ? '#0F2942' : '#334155';
      ctx.fill();
      ctx.strokeStyle = hasGeoWall ? '#38BDF8' : '#64748B';
      ctx.stroke();

      // Draw Floors, Windows & Passive Solar Louvers (R3)
      for (let f = 0; f < floors; f++) {
        const zBot = f * fh + 5;
        const zTop = (f + 1) * fh - 4;
        for (let w = 0; w < 4; w++) {
          const frac0 = -0.4 + w * 0.22;
          const frac1 = frac0 + 0.14;
          const w0 = iso(bw * frac0, bd/2, zBot);
          const w1 = iso(bw * frac1, bd/2, zBot);
          const w2 = iso(bw * frac1, bd/2, zTop);
          const w3 = iso(bw * frac0, bd/2, zTop);
          ctx.beginPath();
          ctx.moveTo(w0.x, w0.y); ctx.lineTo(w1.x, w1.y); ctx.lineTo(w2.x, w2.y); ctx.lineTo(w3.x, w3.y);
          ctx.closePath();
          ctx.fillStyle = hasSmartHvac ? 'rgba(56, 189, 248, 0.55)' : 'rgba(251, 191, 36, 0.45)';
          ctx.fill();

          if (hasLouvers) {
            // Draw overhang shading fin above window
            const l0 = iso(bw * frac0, bd/2 + 7, zTop);
            const l1 = iso(bw * frac1, bd/2 + 7, zTop);
            ctx.beginPath();
            ctx.moveTo(w3.x, w3.y); ctx.lineTo(w2.x, w2.y); ctx.lineTo(l1.x, l1.y); ctx.lineTo(l0.x, l0.y);
            ctx.closePath();
            ctx.fillStyle = '#10B981';
            ctx.fill();
          }
        }
      }

      // Roof Slab (R1 Cool Roof + Aerogel Coating vs Dark RCC Roof)
      const t0 = iso(-bw/2, -bd/2, totalH);
      const t1 = iso(bw/2, -bd/2, totalH);
      const t2 = iso(bw/2, bd/2, totalH);
      const t3 = iso(-bw/2, bd/2, totalH);

      ctx.beginPath();
      ctx.moveTo(t0.x, t0.y); ctx.lineTo(t1.x, t1.y); ctx.lineTo(t2.x, t2.y); ctx.lineTo(t3.x, t3.y);
      ctx.closePath();
      ctx.fillStyle = hasCoolRoof ? '#E0F2FE' : '#334155';
      ctx.fill();
      ctx.strokeStyle = hasCoolRoof ? '#38BDF8' : '#94A3B8';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Draw Bifacial Rooftop Solar PV Array on Roof
      for (let r = -1; r <= 1; r++) {
        const yOff = r * 26;
        const s0 = iso(-bw * 0.34, yOff - 8, totalH + 4);
        const s1 = iso(bw * 0.34, yOff - 8, totalH + 4);
        const s2 = iso(bw * 0.34, yOff + 8, totalH + 9);
        const s3 = iso(-bw * 0.34, yOff + 8, totalH + 9);
        ctx.beginPath();
        ctx.moveTo(s0.x, s0.y); ctx.lineTo(s1.x, s1.y); ctx.lineTo(s2.x, s2.y); ctx.lineTo(s3.x, s3.y);
        ctx.closePath();
        ctx.fillStyle = '#0284C7';
        ctx.fill();
        ctx.strokeStyle = '#7DD3FC';
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // RWH Cistern & Laterite Recharge Tank Indicator at Base
      const cPos = iso(-bw * 0.62, bd * 0.45, 0);
      ctx.fillStyle = 'rgba(6, 182, 212, 0.28)';
      ctx.strokeStyle = '#06B6D4';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(cPos.x, cPos.y, 20, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.fillStyle = '#67E8F9';
      ctx.font = 'bold 10px Inter';
      ctx.fillText(`RWH ${b.water_circularity.cistern_capacity_m3}m³`, cPos.x - 28, cPos.y + 32);

      // Legend Overlay at Bottom Right
      ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
      ctx.fillRect(W - 205, H - 92, 195, 82);
      ctx.strokeStyle = '#334155';
      ctx.strokeRect(W - 205, H - 92, 195, 82);

      ctx.font = '600 10.5px Inter';
      ctx.fillStyle = hasCoolRoof ? '#38BDF8' : '#F97316';
      ctx.fillText(`● Roof: ${hasCoolRoof ? 'Cool Roof SRI 108 (35°C)' : 'Dark RCC (53.9°C)'}`, W - 195, H - 72);
      ctx.fillStyle = hasGeoWall ? '#34D399' : '#94A3B8';
      ctx.fillText(`● Wall: ${hasGeoWall ? 'Geopolymer Fly-Ash Cavity' : 'Uninsulated Laterite/OPC'}`, W - 195, H - 54);
      ctx.fillStyle = hasLouvers ? '#10B981' : '#94A3B8';
      ctx.fillText(`● Shading: ${hasLouvers ? 'Active Solar Louvers' : 'No Overhang Fins'}`, W - 195, H - 36);
      ctx.fillStyle = '#A855F7';
      ctx.fillText(`● Solar PV: ${b.solar_h2_microgrid.installed_solar_kwp} kWp Bifacial`, W - 195, H - 18);
    }

    // =========================================================================
    // TAB 2: CFD AIRFLOW & THERMAL COMFORT PARAMETRIC LAB
    // =========================================================================
    let cfdAnimFrame = null;
    let cfdParticles = [];
    for (let i = 0; i < 85; i++) {
      cfdParticles.push({
        x: Math.random(),
        y: 0.12 + Math.random() * 0.78,
        speed: 0.003 + Math.random() * 0.004
      });
    }

    function updateCfdParametric() {
      const wind = parseFloat(document.getElementById('sld-wind-speed').value);
      const tAmb = parseFloat(document.getElementById('sld-amb-temp').value);
      const rhAmb = parseFloat(document.getElementById('sld-amb-rh').value);
      const geoBlend = parseFloat(document.getElementById('sld-geo-blend').value);

      document.getElementById('lbl-wind-speed').textContent = `${wind.toFixed(1)} m/s`;
      document.getElementById('lbl-amb-temp').textContent = `${tAmb.toFixed(1)} °C`;
      document.getElementById('lbl-amb-rh').textContent = `${rhAmb} %`;
      document.getElementById('lbl-geo-blend').textContent = `${geoBlend} % OPC Replaced`;

      const b = BUILDINGS[selectedBuildingIdx];
      // Compute indoor velocity, ACH, T_op, and Fanger PMV dynamically from sliders
      const vIndoor = +(0.22 + 0.14 * wind).toFixed(2);
      const ach = +(3.4 + 2.1 * wind).toFixed(1);
      const geoInsulCredit = (geoBlend / 85.0) * 1.45;
      const tMrt = +(25.4 + (tAmb - 30.0) * 0.35 - geoInsulCredit * 0.4).toFixed(2);
      const tAir = +(24.8 + (tAmb - 30.0) * 0.28).toFixed(2);
      const tOp = +(0.65 * tAir + 0.35 * tMrt).toFixed(2);
      const rhIn = Math.max(48, Math.round(rhAmb - 16));

      // Approximate Fanger PMV response around tropical comfort point
      const pmv = +((tOp - 26.6) * 0.34 - (vIndoor - 0.55) * 0.42 + (rhIn - 58) * 0.012).toFixed(2);
      const ppd = +(100.0 - 95.0 * Math.exp(-0.03353 * Math.pow(pmv, 4) - 0.2179 * Math.pow(pmv, 2))).toFixed(1);

      document.getElementById('cfd-vel-val').textContent = `${vIndoor} m/s`;
      document.getElementById('cfd-ach-val').textContent = `${ach} ACH`;
      document.getElementById('cfd-top-val').textContent = `${tOp} °C`;
      document.getElementById('cfd-mrt-val').textContent = `T_mrt: ${tMrt} °C`;
      document.getElementById('cfd-pmv-val').textContent = `${pmv >= 0 ? '+' : ''}${pmv}`;
      document.getElementById('cfd-ppd-val').textContent = `PPD: ${ppd}% Dissatisfied`;

      const badge = document.getElementById('cfd-compliance-badge');
      if (Math.abs(pmv) <= 0.5) {
        badge.className = 'pill-badge emerald';
        badge.textContent = `ASHRAE-55 Compliant (|PMV| ≤ 0.5)`;
      } else {
        badge.className = 'pill-badge amber';
        badge.textContent = `Slightly Warm (PMV ${pmv >= 0 ? '+' : ''}${pmv})`;
      }

      drawCfdStreamlines(vIndoor, tOp, tMrt, pmv);
      renderCfdComparisonChart();
    }

    function drawCfdStreamlines(vIndoor, tOp, tMrt, pmv) {
      const canvas = document.getElementById('cfd-streamline-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;

      // Background thermal gradient (ceiling boundary vs breathing zone)
      const grad = ctx.createLinearGradient(0, 0, 0, H);
      grad.addColorStop(0, '#1E1B4B');
      grad.addColorStop(0.35, '#0F172A');
      grad.addColorStop(0.75, '#064E3B');
      grad.addColorStop(1, '#0F172A');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, W, H);

      // Draw Cool Roof + Geopolymer Wall boundaries
      ctx.fillStyle = '#38BDF8';
      ctx.fillRect(0, 0, W, 10);
      ctx.fillStyle = '#E2E8F0';
      ctx.font = 'bold 11px Inter';
      ctx.fillText('R1: High-Albedo Cool Roof + Nano-Silica Aerogel Slab + R4: Coconut Bio-PCM Ceiling Tiles (T_melt = 25.5°C)', 16, 26);

      // Windward Louver Inlet (Left) & Leeward Exhaust (Right)
      ctx.fillStyle = '#10B981';
      ctx.fillRect(0, H * 0.35, 10, H * 0.35);
      ctx.fillRect(W - 10, H * 0.25, 10, H * 0.35);

      // Draw Streamline Curves
      for (let s = 0; s < 9; s++) {
        const yBase = H * (0.18 + s * 0.085);
        ctx.beginPath();
        for (let x = 12; x < W - 12; x += 10) {
          const nx = x / W;
          const wave = Math.sin(nx * Math.PI * 2.0 + s * 0.4) * 16 * (1 - nx * 0.3);
          const y = yBase + wave;
          if (x === 12) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.32)';
        ctx.lineWidth = 1.6;
        ctx.stroke();
      }

      // Draw Velocity Vector Arrows along grid
      for (let gx = 65; gx < W - 50; gx += 75) {
        for (let gy = 55; gy < H - 40; gy += 52) {
          const nx = gx / W, ny = gy / H;
          const vy = Math.cos(nx * Math.PI * 2) * 5;
          const vx = 22 * (0.6 + 0.6 * Math.exp(-Math.pow(ny - 0.52, 2) / 0.08));
          ctx.beginPath();
          ctx.moveTo(gx, gy);
          ctx.lineTo(gx + vx, gy + vy);
          ctx.strokeStyle = '#34D399';
          ctx.lineWidth = 1.8;
          ctx.stroke();

          // Arrowhead
          ctx.beginPath();
          ctx.arc(gx + vx, gy + vy, 2.5, 0, Math.PI * 2);
          ctx.fillStyle = '#6EE7B7';
          ctx.fill();
        }
      }

      // Overlay Info Box
      ctx.fillStyle = 'rgba(15, 23, 42, 0.86)';
      ctx.fillRect(16, H - 54, 495, 40);
      ctx.strokeStyle = '#38BDF8';
      ctx.strokeRect(16, H - 54, 495, 40);
      ctx.fillStyle = '#F8FAFC';
      ctx.font = '600 11.5px JetBrains Mono';
      ctx.fillText(`CFD Breathing Zone (1.1m): v = ${vIndoor} m/s | T_op = ${tOp}°C | PMV = ${pmv >= 0 ? '+' : ''}${pmv}`, 26, H - 30);
    }

    function renderCfdComparisonChart() {
      const ctx = document.getElementById('chart-cfd-pmv-comparison').getContext('2d');
      if (chartCfdPmv) chartCfdPmv.destroy();
      chartCfdPmv = new Chart(ctx, {
        type: 'line',
        data: {
          labels: BUILDINGS.map(b => b.short_name),
          datasets: [
            {
              label: 'Baseline Afternoon Peak PMV (Discomfort)',
              data: BUILDINGS.map(b => b.baseline_cfd.pmv),
              borderColor: '#F43F5E',
              backgroundColor: 'rgba(244,63,94,0.15)',
              borderWidth: 2.2,
              pointRadius: 4
            },
            {
              label: 'EcoTwin Retrofitted PMV (ASHRAE-55 Neutral)',
              data: BUILDINGS.map(b => b.retrofitted_cfd.pmv),
              borderColor: '#10B981',
              backgroundColor: 'rgba(16,185,129,0.18)',
              borderWidth: 2.4,
              pointRadius: 4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#CBD5E1', font: { size: 11 } } }
          },
          scales: {
            x: { ticks: { color: '#94A3B8', font: { size: 10 }, maxRotation: 28 }, grid: { display: false } },
            y: { min: -0.6, max: 2.2, ticks: { color: '#94A3B8' }, grid: { color: 'rgba(148,163,184,0.12)' }, title: { display: true, text: 'ASHRAE-55 PMV', color: '#94A3B8' } }
          }
        }
      });
    }

    // =========================================================================
    // TAB 3: GIS MONSOON RAINWATER & GREYWATER NETWORK
    // =========================================================================
    function renderWaterCharts() {
      const ctx1 = document.getElementById('chart-monsoon-hydrology').getContext('2d');
      if (chartMonsoon) chartMonsoon.destroy();

      // Sum monthly RWH & Greywater across all 12 buildings
      const mRwh = new Array(12).fill(0);
      const mRech = new Array(12).fill(0);
      const mGw = new Array(12).fill(0);
      BUILDINGS.forEach(b => {
        for (let m = 0; m < 12; m++) {
          mRwh[m] += b.water_circularity.monthly_series.rwh_potential_m3[m];
          mRech[m] += b.water_circularity.monthly_series.aquifer_recharge_m3[m];
          mGw[m] += b.water_circularity.monthly_series.greywater_reclaimed_m3[m];
        }
      });

      chartMonsoon = new Chart(ctx1, {
        type: 'bar',
        data: {
          labels: CLIMATE.months,
          datasets: [
            {
              label: 'Roof RWH Harvested (m³/mo)',
              data: mRwh.map(v => Math.round(v)),
              backgroundColor: 'rgba(56, 189, 248, 0.8)'
            },
            {
              label: 'Laterite Aquifer Recharge (m³/mo)',
              data: mRech.map(v => Math.round(v)),
              backgroundColor: 'rgba(20, 184, 166, 0.85)'
            },
            {
              label: 'Biochar Wetland Greywater Reuse (m³/mo)',
              data: mGw.map(v => Math.round(v)),
              backgroundColor: 'rgba(168, 85, 247, 0.8)'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#CBD5E1', font: { size: 11 } } } },
          scales: {
            x: { ticks: { color: '#94A3B8' }, grid: { display: false } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(148,163,184,0.12)' }, title: { display: true, text: 'Volume (m³ / month)', color: '#94A3B8' } }
          }
        }
      });

      const ctx2 = document.getElementById('chart-building-water').getContext('2d');
      if (chartBuildingWater) chartBuildingWater.destroy();
      chartBuildingWater = new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: BUILDINGS.map(b => b.short_name),
          datasets: [
            {
              label: 'Roof Rainwater Harvested (m³/yr)',
              data: BUILDINGS.map(b => b.water_circularity.annual_rwh_harvested_m3),
              backgroundColor: '#38BDF8'
            },
            {
              label: 'Greywater Reclaimed (m³/yr)',
              data: BUILDINGS.map(b => b.water_circularity.annual_greywater_reclaimed_m3),
              backgroundColor: '#C084FC'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#CBD5E1', font: { size: 11 } } } },
          scales: {
            x: { ticks: { color: '#94A3B8', font: { size: 10 }, maxRotation: 25 }, grid: { display: false } },
            y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(148,163,184,0.12)' } }
          }
        }
      });

      // Populate table
      const tbody = document.querySelector('#water-building-table tbody');
      tbody.innerHTML = '';
      BUILDINGS.forEach(b => {
        const w = b.water_circularity;
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-weight:600; color:#F8FAFC;">${b.short_name}</td>
          <td>${b.roof_area_m2.toLocaleString()}</td>
          <td style="color:#38BDF8; font-weight:600;">${w.annual_rwh_harvested_m3.toLocaleString()}</td>
          <td>${w.cistern_capacity_m3}</td>
          <td style="color:#C084FC; font-weight:600;">${w.annual_greywater_reclaimed_m3.toLocaleString()}</td>
          <td><span class="lvl-badge lvl-3">${w.water_self_sufficiency_pct}%</span></td>
        `;
        tbody.appendChild(tr);
      });
    }

    // =========================================================================
    // TAB 4: AI NSGA-II BUDGET PARETO OPTIMIZER & ROI
    // =========================================================================
    function updateNsga2BudgetOptimizer() {
      const budgetL = parseInt(document.getElementById('sld-campus-budget').value, 10);
      const budgetCr = (budgetL / 100.0).toFixed(2);
      document.getElementById('lbl-budget-slider').textContent = `₹${budgetCr} Crores (₹${budgetL} Lakhs)`;

      const plan = NSGA2.budget_tiers_lakhs[String(budgetL)];
      if (!plan) return;
      const s = plan.summary;

      document.getElementById('opt-capex-used').textContent = `₹${s.capex_crores.toFixed(2)} Cr`;
      document.getElementById('opt-payback').textContent = `Payback: ${s.payback_years} Yrs`;
      document.getElementById('opt-co2-abated').textContent = `${s.annual_co2_abated_t.toLocaleString()} t/yr`;
      document.getElementById('opt-emb-co2').textContent = `+${s.embodied_co2_saved_t.toLocaleString()} t Embodied`;
      document.getElementById('opt-water-pct').textContent = `${s.water_self_sufficiency_pct} %`;
      document.getElementById('opt-water-m3').textContent = `${s.water_reclaimed_m3.toLocaleString()} m³/yr`;
      document.getElementById('opt-npv-cr').textContent = `+₹${s.npv_crores.toFixed(2)} Cr`;
      document.getElementById('opt-ann-sav').textContent = `Savings: ₹${(s.annual_savings_lakhs / 100.0).toFixed(2)} Cr/yr`;
      document.getElementById('opt-mean-pmv-badge').textContent = `Campus Mean PMV: ${s.campus_mean_pmv >= 0 ? '+' : ''}${s.campus_mean_pmv}`;

      // Populate Allocation Table
      const tbody = document.querySelector('#nsga2-allocation-table tbody');
      tbody.innerHTML = '';
      plan.building_allocations.forEach(al => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td style="font-family:'JetBrains Mono',monospace; color:#94A3B8;">${al.building_id}</td>
          <td style="font-weight:700; color:#F8FAFC;">${al.short_name}</td>
          <td><span class="lvl-badge lvl-${al.level}">Level ${al.level}</span></td>
          <td style="color:#CBD5E1;">${al.package_label}</td>
          <td style="font-family:'JetBrains Mono',monospace;">₹${al.capex_lakhs.toFixed(1)} L</td>
          <td style="font-family:'JetBrains Mono',monospace; color:#34D399;">₹${al.annual_savings_lakhs.toFixed(1)} L</td>
          <td style="font-family:'JetBrains Mono',monospace; color:#38BDF8;">${al.annual_co2_abated_t.toFixed(1)}</td>
          <td style="font-family:'JetBrains Mono',monospace;">${al.pmv >= 0 ? '+' : ''}${al.pmv}</td>
        `;
        tbody.appendChild(tr);
      });

      renderParetoChart(s);
    }

    function renderParetoChart(selectedSummary) {
      const ctx = document.getElementById('chart-nsga2-pareto').getContext('2d');
      if (chartPareto) chartPareto.destroy();

      const paretoPts = NSGA2.pareto_front.map(p => ({
        x: p.capex_crores,
        y: p.annual_co2_abated_t,
        r: Math.max(5, p.water_self_sufficiency_pct * 0.14)
      }));

      chartPareto = new Chart(ctx, {
        type: 'bubble',
        data: {
          datasets: [
            {
              label: 'Active Budget Selected Solution',
              data: [{
                x: selectedSummary.capex_crores,
                y: selectedSummary.annual_co2_abated_t,
                r: 13
              }],
              backgroundColor: '#10B981',
              borderColor: '#F8FAFC',
              borderWidth: 2.5
            },
            {
              label: 'NSGA-II Non-Dominated Pareto Frontier',
              data: paretoPts,
              backgroundColor: 'rgba(56, 189, 248, 0.55)',
              borderColor: '#38BDF8',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#CBD5E1', font: { size: 11 } } }
          },
          scales: {
            x: {
              title: { display: true, text: 'Campus Capital Budget Outlay (₹ Crores)', color: '#94A3B8' },
              ticks: { color: '#94A3B8' },
              grid: { color: 'rgba(148,163,184,0.12)' }
            },
            y: {
              title: { display: true, text: 'Annual Carbon Abatement (t CO₂e / yr)', color: '#94A3B8' },
              ticks: { color: '#94A3B8' },
              grid: { color: 'rgba(148,163,184,0.12)' }
            }
          }
        }
      });
    }

    function exportMasterplanJSON() {
      const budgetL = document.getElementById('sld-campus-budget').value;
      const plan = NSGA2.budget_tiers_lakhs[String(budgetL)];
      const blob = new Blob([JSON.stringify(plan, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `EcoTwin_MAHE_Masterplan_Rs${budgetL}Lakhs.json`;
      a.click();
      URL.revokeObjectURL(url);
    }

    // Boot Application on DOM Load
    window.addEventListener('DOMContentLoaded', () => {
      initBuildingPills();
      initRetrofitToggles();
      initManipalMap();
      updateBuildingInspector();
      drawIsometricBuilding();
      updateNsga2BudgetOptimizer();
    });
  </script>
</body>
</html>
"""

final_html = html_template.replace("__JSON_PAYLOAD__", json_payload)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Successfully generated {OUT_HTML} ({len(final_html):,} bytes)")
