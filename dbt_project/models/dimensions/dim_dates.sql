with dates as (
    select distinct message_timestamp::date as date from {{ ref('stg_telegram_messages') }}
)
select
    date as date_key,
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    extract(week from date) as week
from dates
