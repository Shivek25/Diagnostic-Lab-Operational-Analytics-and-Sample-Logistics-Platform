{{ config(materialized='view',
          alias='stg_dim_zone')}}

select 
    zone_id,
    zone_name,
    city,
    region_type,
    traffic_level,
    priority_level,
    created_at,
    CURRENT_TIMESTAMP() as dbt_loaded_at 

from {{ source('lab_ops_raw', 'dim_zone') }}

