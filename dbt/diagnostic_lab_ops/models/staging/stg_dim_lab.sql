{{ config(materialized='view',
          alias='stg_dim_lab')}}

select 
    lab_id,
    lab_name,
    lab_type,
    city,
    zone_id,
    capacity_per_day,
    is_24x7,
    lab_status,
    created_at,
    CURRENT_TIMESTAMP() as dbt_loaded_at 

from {{ source('lab_ops_raw', 'dim_lab') }}

