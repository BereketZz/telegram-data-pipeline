-- dbt/models/staging/stg_image_detections.sql

SELECT
    message_id,
    detected_object_class,
    confidence_score,
    detected_at
FROM {{ source('raw', 'raw_image_detections') }}
