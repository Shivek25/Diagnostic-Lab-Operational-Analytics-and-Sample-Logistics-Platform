{{ config(materialized='view',
          alias='stg_sample_manifest')}}

select 
    sample_id,
    patient_id_hash,
    test_type_id,
    lab_id,
    city,
    zone_id,
    sample_collected_at,
    promised_tat_hours,
    priority_flag,
    CURRENT_TIMESTAMP() as dbt_loaded_at 

from {{ source('lab_ops_raw', 'sample_manifest') }}

