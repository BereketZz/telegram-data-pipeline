-- dbt/models/marts/fct_image_detections.sql

SELECT
    CAST(message_id AS INTEGER) AS message_id,
    detected_object_class,
    confidence_score,
    detected_at
FROM {{ ref('stg_image_detections') }}
