# 🧪 Developer Run Checklist — Diagnostic Lab Dashboard

A quick checklist to get the dashboard running locally from scratch.

---

## Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

> Requires Python 3.9+. Activate a virtual environment (`.venv`) first if preferred.

---

## Step 2 — Generate Synthetic Data (only needed once)

Run this from the project root:

```bash
python generate_lab_data.py
```

This will create all CSV source files under:
```
Diagnostic Lab Operational Analytics Sample Logistics Project/
  data/
    raw/        → sample_manifest.csv, courier_events.csv, lab_processing.csv
    reference/  → dim_lab.csv, dim_courier.csv, dim_test_type.csv, dim_zone.csv
```

> If the files already exist, skip this step. The dashboard auto-detects and regenerates if they are missing.

---

## Step 3 — Launch the Dashboard

```bash
streamlit run app.py
```

The browser will open automatically at `http://localhost:8501`.

---

## Step 4 — Verify the Dashboard

- [ ] All 5 tabs load without errors:
  - 📊 Executive Overview
  - 🏥 Lab Performance
  - 🚚 Courier Performance
  - 🔬 Test Type Analytics
  - 🗺 Sample Journey
- [ ] KPI cards show non-zero values at the top
- [ ] Charts render in the Overview and Lab/Courier/Test tabs
- [ ] Sidebar filters (date, city, lab, courier, test type, status) update the data
- [ ] Sample Journey table is searchable by Sample ID (e.g. `SMP000042`)
- [ ] No Python errors in the terminal

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` |
| Charts are empty | Check that CSV files exist in the `data/raw` and `data/reference` folders |
| App fails to start | Make sure you run `streamlit run app.py` from the project root directory |
| Data looks stale | Delete the CSVs and re-run `python generate_lab_data.py` |
