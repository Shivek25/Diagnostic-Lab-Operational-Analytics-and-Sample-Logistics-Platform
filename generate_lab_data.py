import os
import uuid
import random
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

# -----------------------------
# Config
# -----------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("en_IN")
Faker.seed(SEED)

BASE_DIR = Path("Diagnostic Lab Operational Analytics Sample Logistics Project")
RAW_DIR = BASE_DIR / "data" / "raw"
REFERENCE_DIR = BASE_DIR / "data" / "reference"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

for p in [RAW_DIR, REFERENCE_DIR, PROCESSED_DIR]:
    p.mkdir(parents=True, exist_ok=True)

NOW = datetime.now().replace(microsecond=0)

# -----------------------------
# Helper functions
# -----------------------------
def make_id(prefix: str, num: int, width: int = 3) -> str:
    return f"{prefix}{str(num).zfill(width)}"

def random_dt(start_dt: datetime, end_dt: datetime) -> datetime:
    delta_seconds = int((end_dt - start_dt).total_seconds())
    if delta_seconds <= 0:
        return start_dt
    return start_dt + timedelta(seconds=random.randint(0, delta_seconds))

def hash_patient_id() -> str:
    raw = str(uuid.uuid4()).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]

def rand_choice_weighted(items, weights):
    return random.choices(items, weights=weights, k=1)[0]

# -----------------------------
# Reference data
# -----------------------------
zones = [
    {
        "zone_id": "Z001",
        "zone_name": "Noida East",
        "city": "Noida",
        "region_type": "urban",
        "traffic_level": "high",
        "priority_level": 1,
    },
    {
        "zone_id": "Z002",
        "zone_name": "Noida West",
        "city": "Noida",
        "region_type": "urban",
        "traffic_level": "medium",
        "priority_level": 2,
    },
    {
        "zone_id": "Z003",
        "zone_name": "Delhi Central",
        "city": "Delhi",
        "region_type": "urban",
        "traffic_level": "high",
        "priority_level": 1,
    },
    {
        "zone_id": "Z004",
        "zone_name": "Gurugram North",
        "city": "Gurugram",
        "region_type": "urban",
        "traffic_level": "medium",
        "priority_level": 2,
    },
]

labs = [
    {
        "lab_id": "LAB001",
        "lab_name": "Noida Central Lab",
        "lab_type": "processing_lab",
        "city": "Noida",
        "zone_id": "Z001",
        "capacity_per_day": 1200,
        "is_24x7": True,
        "lab_status": "active",
    },
    {
        "lab_id": "LAB002",
        "lab_name": "Delhi Reference Lab",
        "lab_type": "hub_lab",
        "city": "Delhi",
        "zone_id": "Z003",
        "capacity_per_day": 1800,
        "is_24x7": True,
        "lab_status": "active",
    },
    {
        "lab_id": "LAB003",
        "lab_name": "Gurugram Diagnostic Center",
        "lab_type": "processing_lab",
        "city": "Gurugram",
        "zone_id": "Z004",
        "capacity_per_day": 900,
        "is_24x7": False,
        "lab_status": "active",
    },
    {
        "lab_id": "LAB004",
        "lab_name": "Noida Collection Hub",
        "lab_type": "collection_center",
        "city": "Noida",
        "zone_id": "Z002",
        "capacity_per_day": 500,
        "is_24x7": False,
        "lab_status": "active",
    },
]

couriers = [
    {
        "courier_id": "C001",
        "courier_name": "NCR Express Logistics",
        "courier_type": "third_party",
        "service_area": "Delhi NCR",
        "avg_delivery_time_hours": 2.5,
        "cost_per_km": 18.0,
        "sla_hours": 4.0,
        "contact_type": "phone",
        "active_status": "active",
    },
    {
        "courier_id": "C002",
        "courier_name": "HealthMove Couriers",
        "courier_type": "third_party",
        "service_area": "Delhi NCR",
        "avg_delivery_time_hours": 3.0,
        "cost_per_km": 20.0,
        "sla_hours": 5.0,
        "contact_type": "whatsapp",
        "active_status": "active",
    },
    {
        "courier_id": "C003",
        "courier_name": "Metro Sample Transport",
        "courier_type": "inhouse",
        "service_area": "Noida",
        "avg_delivery_time_hours": 1.8,
        "cost_per_km": 15.0,
        "sla_hours": 3.0,
        "contact_type": "phone",
        "active_status": "active",
    },
    {
        "courier_id": "C004",
        "courier_name": "QuickPath Medical Logistics",
        "courier_type": "third_party",
        "service_area": "Delhi NCR",
        "avg_delivery_time_hours": 2.2,
        "cost_per_km": 22.0,
        "sla_hours": 4.0,
        "contact_type": "email",
        "active_status": "active",
    },
    {
        "courier_id": "C005",
        "courier_name": "CityCare Courier",
        "courier_type": "third_party",
        "service_area": "Gurugram",
        "avg_delivery_time_hours": 2.9,
        "cost_per_km": 19.0,
        "sla_hours": 5.0,
        "contact_type": "phone",
        "active_status": "active",
    },
]

test_types = [
    {
        "test_type_id": "T001",
        "test_name": "CBC",
        "test_category": "Hematology",
        "sample_type": "Blood",
        "expected_tat_hours": 6,
        "cost": 350.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T002",
        "test_name": "Blood Sugar Fasting",
        "test_category": "Biochemistry",
        "sample_type": "Blood",
        "expected_tat_hours": 4,
        "cost": 180.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T003",
        "test_name": "Liver Function Test",
        "test_category": "Biochemistry",
        "sample_type": "Blood",
        "expected_tat_hours": 8,
        "cost": 750.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T004",
        "test_name": "Kidney Function Test",
        "test_category": "Biochemistry",
        "sample_type": "Blood",
        "expected_tat_hours": 8,
        "cost": 700.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T005",
        "test_name": "Thyroid Profile",
        "test_category": "Hormone",
        "sample_type": "Blood",
        "expected_tat_hours": 10,
        "cost": 900.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T006",
        "test_name": "HbA1c",
        "test_category": "Biochemistry",
        "sample_type": "Blood",
        "expected_tat_hours": 12,
        "cost": 600.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T007",
        "test_name": "Vitamin D",
        "test_category": "Vitamin",
        "sample_type": "Blood",
        "expected_tat_hours": 24,
        "cost": 1200.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T008",
        "test_name": "Urine Routine",
        "test_category": "Pathology",
        "sample_type": "Urine",
        "expected_tat_hours": 6,
        "cost": 250.00,
        "is_critical_test": False,
    },
    {
        "test_type_id": "T009",
        "test_name": "Dengue NS1",
        "test_category": "Serology",
        "sample_type": "Blood",
        "expected_tat_hours": 8,
        "cost": 850.00,
        "is_critical_test": True,
    },
    {
        "test_type_id": "T010",
        "test_name": "PCR Test",
        "test_category": "Molecular",
        "sample_type": "Swab",
        "expected_tat_hours": 18,
        "cost": 1500.00,
        "is_critical_test": True,
    },
]

# -----------------------------
# Build dimension tables
# -----------------------------
dim_zone_df = pd.DataFrame(zones)
dim_zone_df["created_at"] = [random_dt(NOW - timedelta(days=180), NOW - timedelta(days=1)) for _ in range(len(dim_zone_df))]

dim_lab_df = pd.DataFrame(labs)
dim_lab_df["created_at"] = [random_dt(NOW - timedelta(days=180), NOW - timedelta(days=1)) for _ in range(len(dim_lab_df))]

dim_courier_df = pd.DataFrame(couriers)
dim_courier_df["created_at"] = [random_dt(NOW - timedelta(days=180), NOW - timedelta(days=1)) for _ in range(len(dim_courier_df))]

dim_test_type_df = pd.DataFrame(test_types)
dim_test_type_df["created_at"] = [random_dt(NOW - timedelta(days=180), NOW - timedelta(days=1)) for _ in range(len(dim_test_type_df))]

# -----------------------------
# Generate sample manifest
# -----------------------------
NUM_SAMPLES = 1000
sample_rows = []
for i in range(1, NUM_SAMPLES + 1):
    sample_id = make_id("SMP", i, 6)
    patient_id_hash = hash_patient_id()

    test = random.choice(test_types)
    zone = random.choice(zones)
    lab_candidates = [l for l in labs if l["city"] == zone["city"]]
    if not lab_candidates:
        lab_candidates = labs
    lab = random.choice(lab_candidates)

    # Collection time in last 21 days
    collected_at = random_dt(NOW - timedelta(days=21), NOW - timedelta(hours=6))

    # Promised TAT is a business SLA, so keep it as a decimal duration
    promised_tat_hours = round(float(test["expected_tat_hours"]) + random.uniform(0.0, 3.5), 2)

    priority_flag = rand_choice_weighted(
        ["Low", "Normal", "High"],
        [0.15, 0.7, 0.15],
    )

    sample_rows.append({
        "sample_id": sample_id,
        "patient_id_hash": patient_id_hash,
        "test_type_id": test["test_type_id"],
        "lab_id": lab["lab_id"],
        "city": zone["city"],
        "zone_id": zone["zone_id"],
        "sample_collected_at": collected_at,
        "promised_tat_hours": promised_tat_hours,
        "priority_flag": priority_flag,
    })

sample_manifest_df = pd.DataFrame(sample_rows)

# -----------------------------
# Generate courier events
# -----------------------------
event_rows = []
event_counter = 1

courier_map = {c["courier_id"]: c for c in couriers}
zone_map = {z["zone_id"]: z for z in zones}
lab_map = {l["lab_id"]: l for l in labs}

rejection_reasons = [
    "Damaged sample",
    "Insufficient sample quantity",
    "Incorrect label",
    "Delayed arrival",
    "Clotted sample",
]

for _, row in sample_manifest_df.iterrows():
    sample_id = row["sample_id"]
    courier = random.choice(couriers)
    lab = lab_map[row["lab_id"]]
    zone = zone_map[row["zone_id"]]

    pickup_delay_minutes = random.randint(10, 120)
    pickup_time = row["sample_collected_at"] + timedelta(minutes=pickup_delay_minutes)

    # Transit time in minutes, based on courier average
    base_transit = courier["avg_delivery_time_hours"] * 60
    transit_minutes = max(10, int(random.gauss(base_transit, base_transit * 0.25)))
    distance_km = round(max(1.0, transit_minutes / 12 * random.uniform(0.7, 1.5)), 2)

    delivered_time = pickup_time + timedelta(minutes=transit_minutes)

    sla_minutes = courier["sla_hours"] * 60
    courier_status = "Delayed" if transit_minutes > sla_minutes else "Completed"

    event_rows.append({
        "event_id": make_id("EVT", event_counter, 7),
        "courier_id": courier["courier_id"],
        "sample_id": sample_id,
        "event_type": "PickedUp",
        "event_time": pickup_time,
        "source_location": f"Collection Center - {zone['zone_name']}",
        "destination_location": f"{lab['lab_name']}",
        "status": "Completed",
        "distance_km": round(distance_km * 0.35, 2),
        "transit_minutes": round(float(pickup_delay_minutes), 2),
    })
    event_counter += 1

    event_rows.append({
        "event_id": make_id("EVT", event_counter, 7),
        "courier_id": courier["courier_id"],
        "sample_id": sample_id,
        "event_type": "Delivered",
        "event_time": delivered_time,
        "source_location": f"Collection Center - {zone['zone_name']}",
        "destination_location": f"{lab['lab_name']}",
        "status": courier_status,
        "distance_km": distance_km,
        "transit_minutes": round(float(transit_minutes), 2),
    })
    event_counter += 1

courier_events_df = pd.DataFrame(event_rows)

# -----------------------------
# Generate lab processing data
# -----------------------------
processing_rows = []
for _, row in sample_manifest_df.iterrows():
    sample_id = row["sample_id"]
    lab = lab_map[row["lab_id"]]
    courier_event_delivered = courier_events_df[
        (courier_events_df["sample_id"] == sample_id) &
        (courier_events_df["event_type"] == "Delivered")
    ].iloc[0]

    lab_received_at = courier_event_delivered["event_time"] + timedelta(minutes=random.randint(10, 60))

    # Some rejected samples
    is_rejected = random.random() < 0.08

    if is_rejected:
        processing_rows.append({
            "lab_id": row["lab_id"],
            "sample_id": sample_id,
            "lab_received_at": lab_received_at,
            "test_started_at": None,
            "test_completed_at": None,
            "report_released_at": None,
            "result_status": "Rejected",
            "rejection_reason": random.choice(rejection_reasons),
        })
        continue

    test_started_at = lab_received_at + timedelta(minutes=random.randint(5, 90))

    # Actual processing duration linked to expected TAT
    test_info = dim_test_type_df[dim_test_type_df["test_type_id"] == row["test_type_id"]].iloc[0]
    expected_hours = float(test_info["expected_tat_hours"])

    # Make actual processing a little realistic
    test_duration_minutes = max(20, int((expected_hours * 60) * random.uniform(0.35, 0.8)))
    test_completed_at = test_started_at + timedelta(minutes=test_duration_minutes)

    report_released_at = test_completed_at + timedelta(minutes=random.randint(10, 45))

    # Some delayed but completed samples
    actual_total_hours = (report_released_at - row["sample_collected_at"]).total_seconds() / 3600
    promised = float(row["promised_tat_hours"])
    result_status = "Delayed" if actual_total_hours > promised else "Completed"

    processing_rows.append({
        "lab_id": row["lab_id"],
        "sample_id": sample_id,
        "lab_received_at": lab_received_at,
        "test_started_at": test_started_at,
        "test_completed_at": test_completed_at,
        "report_released_at": report_released_at,
        "result_status": result_status,
        "rejection_reason": None,
    })

lab_processing_df = pd.DataFrame(processing_rows)

# -----------------------------
# Clean datetime columns for CSV
# -----------------------------
def normalize_datetime_cols(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    datetime_cols = [
        "sample_collected_at",
        "event_time",
        "lab_received_at",
        "test_started_at",
        "test_completed_at",
        "report_released_at",
        "created_at"
    ]

    for col in datetime_cols:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")

    return out

dim_zone_df = normalize_datetime_cols(dim_zone_df)
dim_lab_df = normalize_datetime_cols(dim_lab_df)
dim_courier_df = normalize_datetime_cols(dim_courier_df)
dim_test_type_df = normalize_datetime_cols(dim_test_type_df)
sample_manifest_df = normalize_datetime_cols(sample_manifest_df)
courier_events_df = normalize_datetime_cols(courier_events_df)
lab_processing_df = normalize_datetime_cols(lab_processing_df)

print(sample_manifest_df.head())
print(lab_processing_df.head())
# -----------------------------
# Save CSVs
# -----------------------------
dim_zone_df.to_csv(REFERENCE_DIR / "dim_zone.csv", index=False)
dim_lab_df.to_csv(REFERENCE_DIR / "dim_lab.csv", index=False)
dim_courier_df.to_csv(REFERENCE_DIR / "dim_courier.csv", index=False)
dim_test_type_df.to_csv(REFERENCE_DIR / "dim_test_type.csv", index=False)

sample_manifest_df.to_csv(RAW_DIR / "sample_manifest.csv", index=False)
courier_events_df.to_csv(RAW_DIR / "courier_events.csv", index=False)
lab_processing_df.to_csv(RAW_DIR / "lab_processing.csv", index=False)

# Optional processed folder copies
sample_manifest_df.to_csv(PROCESSED_DIR / "sample_manifest_clean.csv", index=False)
courier_events_df.to_csv(PROCESSED_DIR / "courier_events_clean.csv", index=False)
lab_processing_df.to_csv(PROCESSED_DIR / "lab_processing_clean.csv", index=False)

# -----------------------------
# Basic validation
# -----------------------------
print("Files created successfully.\n")
print("Reference tables:")
print(f" - {REFERENCE_DIR / 'dim_zone.csv'}")
print(f" - {REFERENCE_DIR / 'dim_lab.csv'}")
print(f" - {REFERENCE_DIR / 'dim_courier.csv'}")
print(f" - {REFERENCE_DIR / 'dim_test_type.csv'}")

print("\nRaw tables:")
print(f" - {RAW_DIR / 'sample_manifest.csv'}")
print(f" - {RAW_DIR / 'courier_events.csv'}")
print(f" - {RAW_DIR / 'lab_processing.csv'}")

print("\nRow counts:")
print(f"dim_zone: {len(dim_zone_df)}")
print(f"dim_lab: {len(dim_lab_df)}")
print(f"dim_courier: {len(dim_courier_df)}")
print(f"dim_test_type: {len(dim_test_type_df)}")
print(f"sample_manifest: {len(sample_manifest_df)}")
print(f"courier_events: {len(courier_events_df)}")
print(f"lab_processing: {len(lab_processing_df)}")

print("\nNull check summary:")
print(sample_manifest_df.isna().sum())
print(lab_processing_df.isna().sum())
print(sample_manifest_df["patient_id_hash"].isna().sum())
print(lab_processing_df["result_status"].isna().sum())