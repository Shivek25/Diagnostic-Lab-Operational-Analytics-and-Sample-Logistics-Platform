{{ config(materialized='table',
          alias='agg_lab_daily_performance')}}

-- This model aggregates lab performance metrics by lab_id and date.
with base as (
    select
        lab_id,
        date(sample_collected_at) as activity_date,
        sample_id,
        result_status,
        rejection_flag,
        sla_breach_flag,
        total_tat_minutes,
        test_processing_minutes,
        delivery_to_lab_minutes
    from {{ ref('fct_sample_journey') }}
)

select
    lab_id,
    activity_date,
    count(*) as total_samples,
    countif(result_status = 'Completed') as completed_samples,
    countif(result_status = 'Delayed') as delayed_samples,
    countif(result_status = 'Rejected') as rejected_samples,
    round(avg(total_tat_minutes), 2) as avg_total_tat_minutes,
    round(avg(test_processing_minutes), 2) as avg_test_processing_minutes,
    round(avg(delivery_to_lab_minutes), 2) as avg_delivery_to_lab_minutes,
    round(safe_divide(countif(sla_breach_flag = 1), count(*)) * 100, 2) as sla_breach_rate_pct,
    round(safe_divide(countif(rejection_flag = 1), count(*)) * 100, 2) as rejection_rate_pct
from base
group by lab_id, activity_date