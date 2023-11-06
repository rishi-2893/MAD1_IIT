from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("jinjaTemplates/"))

rishi_template = env.get_template("rishi.txt")

rishi_content = rishi_template.render()

print(rishi_content)