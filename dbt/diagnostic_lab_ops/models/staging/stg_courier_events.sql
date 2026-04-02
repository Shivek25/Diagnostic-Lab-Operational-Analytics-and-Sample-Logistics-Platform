{{ config(materialized='view',
          alias='stg_courier_events')}}


select 
    event_id, 
    courier_id, 
    sample_id, 
    event_type, 
    event_time, 
    source_location, 
    destination_location, 
    status, 
    distance_km, 
    transit_minutes,
    CURRENT_TIMESTAMP() as dbt_loaded_at    

from {{ source('lab_ops_raw', 'courier_events') }}
