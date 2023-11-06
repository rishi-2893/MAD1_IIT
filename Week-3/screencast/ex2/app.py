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


def main():
    template_file = open('template.html', 'r')
    TEMPLATE = template_file.read()
    
    template = Template(TEMPLATE)
    content = template.render(jnanpith_data = jnanpith_data)

    html_doc = open('jnanipith.html', 'w')
    html_doc.write(content)
    html_doc.close()

    

if __name__ == '__main__':
	main()