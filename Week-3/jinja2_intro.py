from jinja2 import Template

t = Template("Hello {{ something }}")
print(t.render(something = "World"))


t = Template("First 5 numbers: {% for i in range(1, 6) %}{{i}} {% endfor %}")
print(t.render())
