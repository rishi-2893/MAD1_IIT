from jinja2 import Template

# Define query variables
variables = {
  "column": "value",
  "min_date": "2022-01-01",
  "max_date": "2022-12-31"
}

# Create a Jinja template for the query
template = Template("""
SELECT * FROM table
WHERE column = '{{ column }}'
AND date BETWEEN '{{ min_date }}' AND '{{ max_date }}'
""")

# Render the template along with the variables
query = template.render(variables)

# Print the results
print(query)