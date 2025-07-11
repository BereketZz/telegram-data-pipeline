select
    distinct channel_name as channel_key,
    channel_name as channel_name
from {{ ref('stg_telegram_messages') }}
