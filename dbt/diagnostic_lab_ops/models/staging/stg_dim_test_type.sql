{{ config(materialized='view',
          alias='stg_dim_test_type')}}

select 
    test_type_id,
    test_name,
    test_category,
    sample_type,
    expected_tat_hours,
    cost,
    is_critical_test,
    created_at,
    CURRENT_TIMESTAMP() as dbt_loaded_at 

from {{ source('lab_ops_raw', 'dim_test_type') }}

