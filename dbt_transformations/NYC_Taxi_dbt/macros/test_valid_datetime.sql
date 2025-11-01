{% test valid_datetime(model, column_name) %}
SELECT *
FROM {{ model }}
WHERE {{ column_name }} <= '2000-01-01'
{% endtest %}