{% test column_gte_column(model, left_column, right_column) %}

select *
from {{ model }}
where {{ left_column }} is not null
  and {{ right_column }} is not null
  and {{ left_column }} < {{ right_column }}

{% endtest %}