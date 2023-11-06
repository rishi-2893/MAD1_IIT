from jinja2 import Environment, FileSystemLoader
import random


template_dir = "./templates"
env = Environment(loader=FileSystemLoader(template_dir))


# BASE
base_template = env.get_template("base.html")

base_content = base_template.render()
base_html = open('outputs/base.html', 'w')
base_html.write(base_content)


# HOME
home_template = env.get_template("home.html")

home_content = home_template.render(randomNumber=random.randint(1, 100))
home_html = open('outputs/home.html', 'w')
home_html.write(home_content)



# CONTACT
contact_template = env.get_template("contact.html")

contact_content = contact_template.render(phoneNumber = 9978624042)
contact_html = open('outputs/contact.html', 'w')
contact_html.write(contact_content)