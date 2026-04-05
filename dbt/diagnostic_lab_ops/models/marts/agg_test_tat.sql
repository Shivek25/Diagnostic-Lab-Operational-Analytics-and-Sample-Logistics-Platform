{{ config(materialized='table',
          alias='agg_test_tat')}}

-- This model aggregates test performance metrics by test type_id and date.
with base as (
    select
        test_type_id,
        test_name,
        test_category,
        date(sample_collected_at) as activity_date,
        sample_id,
        total_tat_minutes,
        expected_tat_hours,
        rejection_flag,
        sla_breach_flag,
        result_status
    from {{ ref('fct_sample_journey') }}
)

select
    test_type_id,
    test_name,
    test_category,
    activity_date,
    count(*) as total_samples,
    round(avg(total_tat_minutes), 2) as avg_total_tat_minutes,
    round(avg(expected_tat_hours * 60), 2) as avg_expected_tat_minutes,
    countif(rejection_flag = 1) as rejected_samples,
    round(safe_divide(countif(rejection_flag = 1), count(*)), 2) as rejection_rate,
    countif(sla_breach_flag = 1) as sla_breaches,
    round(safe_divide(countif(sla_breach_flag = 1), count(*)), 2) as sla_breach_rate
from base
group by test_type_id, test_name, test_category, activity_date