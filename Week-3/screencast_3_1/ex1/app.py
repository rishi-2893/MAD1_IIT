from jinja2 import Template

jnanpith_data = [
	{
		"year": 1965,
		"awardees": "G. Sankara Kurup",
		"language": "Malayalam"
	},
	{
		"year": 1966,
		"awardees": "Tarashankar Bandopadhyaya",
		"language": "Bengali"
	},
	{
		"year": 1967,
		"awardees": "Kuppali Venkatappagowda Puttappa",
		"language": "Kannada"
	}
]


TEMPLATE = """
<!DOCTYPE html>
<hmtl>
	<head>
		<meta charset="UTF-8" />
		<title>Jnanpith</title>
		<meta name="description" content="This page lists Jnanpith Awardees">
	</head>
	<body>
		<h1>Awardees</h1>
		<table>
			<thead>
				<tr>
					<th>Year</th>
					<th>Awardees</th>
					<th>Language</th>
				</tr>
			</thead>
			<tbody>
				{% for jnanpith in jnanpith_data %}
                <tr>
                    <td>{{ jnanpith['year'] }}</td>
                    <td>{{ jnanpith['awardees'] }}</td>
                    <td>{{ jnanpith['language'] }}</td>
				</tr>
				{% endfor %}
			</tbody>
		</table>
	</body>
</html>
"""


def main():
    # Sending string to Jinja Template class
    template = Template(TEMPLATE)
    content = template.render(jnanpith_data = jnanpith_data)

    # Saving html to a file
    html_doc = open('jnanipith.html', 'w')
    html_doc.write(content)
    html_doc.close()


if __name__ == '__main__':
	# Execute only if run as a script
	main()