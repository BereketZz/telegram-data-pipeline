with raw as (
    select
        id,
        channel_name,
        message_date,
        raw_data
    from raw.telegram_messages
)

select
    id,
    channel_name,
    message_date::timestamp as message_timestamp,
    raw_data->>'text' as message_text,
    (raw_data->>'has_photo')::boolean as has_photo,
    length(raw_data->>'text') as message_length
from raw
