select
    id as message_id,
    (select channel_key from {{ ref('dim_channels') }} where channel_name = s.channel_name) as channel_key,
    (select date_key from {{ ref('dim_dates') }} where date = s.message_timestamp::date) as date_key,
    s.message_text,
    s.message_length,
    s.has_photo
from {{ ref('stg_telegram_messages') }} s
