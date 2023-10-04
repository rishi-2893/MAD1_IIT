from string import Template

t = Template('$name is the $job of the $company')
s = t.substitute(name='Tim Cook', job='CEO', company='Apple Inc.')
print(s)