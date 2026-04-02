{{ config(materialized='table',
          alias='agg_courier_sla')}}

-- This model aggregates courier performance metrics by courier_id and date.
with base as (
    select
        courier_id,
        date(pickup_time) as activity_date,
        sample_id,
        transit_minutes,
        distance_km,
        courier_delay_flag,
        result_status
    from {{ ref('fct_sample_journey') }}
    where courier_id is not null
)

select
    courier_id,
    activity_date,
    count(*) as total_deliveries,
    round(avg(transit_minutes), 2) as avg_transit_minutes,
    round(avg(distance_km), 2) as avg_distance_km,
    countif(courier_delay_flag = 1) as delayed_deliveries,
    round(safe_divide(countif(courier_delay_flag = 1), count(*)) * 100, 2) as delay_rate_pct,
    round(safe_divide(countif(result_status = 'Completed'), count(*)) * 100, 2) as completion_rate_pct
from base
group by courier_id, activity_date