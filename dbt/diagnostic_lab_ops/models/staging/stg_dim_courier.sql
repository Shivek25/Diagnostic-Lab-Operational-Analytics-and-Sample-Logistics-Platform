{{ config(materialized='view',
          alias='stg_dim_courier')}}

select 
    courier_id,
    courier_name,
    courier_type,
    service_area,
    avg_delivery_time_hours,
    cost_per_km,
    sla_hours,
    contact_type,
    active_status,
    created_at,
    CURRENT_TIMESTAMP() as dbt_loaded_at    

from {{ source('lab_ops_raw', 'dim_courier') }}

