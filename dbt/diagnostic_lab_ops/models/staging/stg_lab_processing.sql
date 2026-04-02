{{ config(materialized='view',
          alias='stg_lab_processing')}}

select 
    sample_id,
    lab_id,
    lab_received_at,
    test_started_at,
    test_completed_at,
    report_released_at,
    result_status,
    rejection_reason,
    CURRENT_TIMESTAMP() as dbt_loaded_at 

from {{ source('lab_ops_raw', 'lab_processing') }}

