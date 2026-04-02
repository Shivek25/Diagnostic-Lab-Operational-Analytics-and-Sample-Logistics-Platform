{{ config(materialized='table',
          alias='fct_sample_journey')}}

-- This model joins the raw journey data into one row per sample_id. This is the core operational journey. 
with manifest as (
    select
        sample_id,
        patient_id_hash,
        test_type_id,
        lab_id as manifest_lab_id,
        city,
        zone_id,
        sample_collected_at,
        promised_tat_hours,
        priority_flag
    from {{ ref('stg_sample_manifest') }}
),

courier_pickup as (
    select
        sample_id,
        courier_id,
        min(case when event_type = 'PickedUp' then event_time end) as pickup_time,
        min(case when event_type = 'Delivered' then event_time end) as delivery_time,
        max(distance_km) as distance_km,
        max(transit_minutes) as transit_minutes
    from {{ ref('stg_courier_events') }}
    group by sample_id, courier_id
),

lab_process as (
    select
        sample_id,
        lab_id as process_lab_id,
        lab_received_at,
        test_started_at,
        test_completed_at,
        report_released_at,
        result_status,
        rejection_reason
    from {{ ref('stg_lab_processing') }}
),

test_dim as (
    select
        test_type_id,
        test_name,
        test_category,
        sample_type,
        expected_tat_hours,
        cost,
        is_critical_test
    from {{ ref('stg_dim_test_type') }}
)

select
    m.sample_id,
    m.patient_id_hash,
    m.test_type_id,
    t.test_name,
    t.test_category,
    t.sample_type,
    t.expected_tat_hours,
    t.cost,
    t.is_critical_test,

    m.manifest_lab_id as lab_id,
    m.city,
    m.zone_id,
    m.sample_collected_at,
    m.promised_tat_hours,
    m.priority_flag,

    c.courier_id,
    c.pickup_time,
    c.delivery_time,
    c.distance_km,
    c.transit_minutes,

    l.lab_received_at,
    l.test_started_at,
    l.test_completed_at,
    l.report_released_at,
    l.result_status,
    l.rejection_reason,

    case
        when c.pickup_time is not null and c.pickup_time > m.sample_collected_at then 1
        else 0
    end as pickup_delay_flag,

    case
        when c.delivery_time is not null and c.delivery_time > timestamp_add(c.pickup_time, interval cast(t.expected_tat_hours as int64) hour) then 1
        else 0
    end as courier_delay_flag,

    case
        when l.report_released_at is not null
         and timestamp_diff(l.report_released_at, m.sample_collected_at, minute) > cast(m.promised_tat_hours * 60 as int64)
        then 1
        else 0
    end as sla_breach_flag,

    case
        when l.result_status = 'Rejected' then 1
        else 0
    end as rejection_flag,

    case
        when l.report_released_at is not null
        then timestamp_diff(l.report_released_at, m.sample_collected_at, minute)
        else null
    end as total_tat_minutes,

    case
        when l.lab_received_at is not null and c.delivery_time is not null
        then timestamp_diff(l.lab_received_at, c.delivery_time, minute)
        else null
    end as delivery_to_lab_minutes,

    case
        when l.test_completed_at is not null and l.test_started_at is not null
        then timestamp_diff(l.test_completed_at, l.test_started_at, minute)
        else null
    end as test_processing_minutes

from manifest m
left join courier_pickup c
    on m.sample_id = c.sample_id
left join lab_process l
    on m.sample_id = l.sample_id
left join test_dim t
    on m.test_type_id = t.test_type_id