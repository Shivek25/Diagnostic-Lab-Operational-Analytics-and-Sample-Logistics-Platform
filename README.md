# 🏥 Diagnostic Lab Operational Analytics & Sample Logistics Platform

An end-to-end data engineering and analytics solution designed for private diagnostic lab chains. This platform tracks the full lifecycle of medical samples; from collection and courier movement to lab processing and final report release. 

By unifying fragmented operational data, this project provides a single consolidated view to monitor delays, identify bottlenecks, measure turnaround times, and improve overall operational reliability.

---

## 🚀 Project Overview

In a typical diagnostic lab environment, tracking sample movement and operational performance is often managed through disconnected tools or manual registers. This results in poor visibility into where delays occur or which parts of the process are failing.

This project solves this by building a centralized analytics pipeline that answers critical business questions:
- How long does each sample take from collection to report release?
- Which labs are performing well, and which are creating delays?
- Which couriers are causing transport delays?
- Which test types are slower, more resource-intensive, or prone to rejection?
- Where are the rejection and SLA breach patterns?

---

## 💡 Problem Statement

Private diagnostic labs generally face several recurring operational challenges:
- Sample movement is tracked manually across fragmented systems.
- Courier delay information is not connected to lab processing data.
- **TAT (Turnaround Time)** is not measured consistently across different labs or test types.
- Rejected samples are not analyzed adequately to determine root causes.
- Management lacks a single consolidated view of sample flow and operational performance.

**The Solution:** A structured data platform with proper ingestion, modeling, quality checks, and reporting, delivering actionable business intelligence.

---

## 🛠️ Architecture & Tech Stack

The solution is built as a modern data warehouse pipeline consisting of four major layers:

1. **Synthetic Data Generation (Python, Pandas, Faker):** 
   Since real patient-level data is sensitive, realistic de-identified operational data was generated (including realistic delays, priority-based samples, and SLA breaches).
2. **Raw Data Layer (Google BigQuery):** 
   Generated data is loaded into BigQuery staging tables representing the raw operational systems (manifests, courier events, lab intake).
3. **Transformation Layer (dbt - data build tool):** 
   Data is cleaned, standardized, and modeled using dbt. This includes staging models, an intermediate sample journey model, and final aggregated mart tables.
4. **Analytics & Reporting Layer (Power BI):** 
   A comprehensive dashboard providing interactive drill-down capabilities for executive overviews, lab performance, and courier tracking.

---

## 📊 Data Model Design

The project employs a robust **Star Schema** designed for analytical workloads:

### **Dimension Tables** (Business Context)
- `dim_lab`: Lab master data (capacity, type, 24x7 availability, zone).
- `dim_courier`: Courier vendor details (service area, average delivery time, SLA hours).
- `dim_test_type`: Test catalog information (category, expected TAT, critical status).
- `dim_zone`: Regional information (traffic levels, priority).

### **Fact & Operational Tables** (Business Process)
- `sample_manifest`: Order and collection records.
- `courier_events`: Courier pickup and delivery behavior.
- `lab_processing`: Lab intake, testing, and report release timestamps.

### **Analytical Data Marts** (Reporting Tables)
- `fct_sample_journey`: The main fact table stitching the entire sample lifecycle, including flags and durations.
- `agg_lab_daily_performance`: Daily lab productivity and quality summaries.
- `agg_courier_sla`: Courier operational performance tracking.
- `agg_test_tat`: Test-level turnaround and rejection metrics.

---

## 📈 Key Business Logic & Metrics

- **TAT (Turnaround Time):** The total time taken from sample collection to the final report release.
- **SLA (Service Level Agreement) Monitoring:** A sample is flagged as "breached" if the actual TAT exceeds the expected/promised TAT.
- **Delay Attribution:** The pipeline separately tracks *Pickup Delays* and *Courier Delays* so the business knows exactly whether transport or lab processing is at fault.
- **Rejection Tracking:** Rejected samples are flagged, allowing labs to review rejection patterns by test type, courier, or zone.

---

## 📈 Power BI Dashboard Highlights

The final Power BI report acts as a real-time operations control system, divided into key areas:
1. **Executive Overview:** Top-level metrics on total samples, completion rates, SLA breach rates, and overall TAT trends.
2. **Lab Performance:** Focuses on lab efficiency, highlighting overloaded labs, rejection rates, and average processing times.
3. **Courier Performance:** Tracks vendor efficiency, average transit times, and delivery completion rates.
4. **Test Analytics:** Identifies operationally heavy tests, critical test volume, and expected vs. actual TAT.
5. **Sample Journey Detail:** A drill-through view detailing the exact lifecycle and timestamp trace of individual samples.

---

## 💼 Value Proposition for Clients

This platform serves as a strong foundation for any diagnostic business looking to modernize its operations:
- **Operational Visibility:** Get a single pane of glass over sample logistics.
- **Root Cause Analysis:** Instantly identify whether a bottleneck is due to a specific courier route, a slow lab, or a specific test category.
- **Vendor & Lab Accountability:** Accurately track courier SLA adherence and individual lab productivity.
- **Process Improvement:** Spot rejection patterns caused by poor sample handling or route delays and take corrective action.

---

*This project was built to demonstrate an end-to-end data engineering lifecycle, combining data modeling, warehouse design, pipeline orchestration, and business interpretation into a production-grade analytics platform.*
