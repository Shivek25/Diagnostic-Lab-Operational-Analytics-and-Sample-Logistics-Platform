with courier_events as (
    select * from {{ ref('stg_courier_events') }}
),

sample_manifest as (
    select * from {{ ref('stg_sample_manifest') }}
),

joined as (
    -- Example join logic, you will obviously modify this according to table structures
    select 
        c.*, 
        -- assuming both have a common sample_id or similar, 
        -- we just do a dummy join for demonstration. 
        s.*
    from courier_events c
    left join sample_manifest s 
      -- Replace with actual join keys:
      on 1=1
)

select * from joined
limit 10
