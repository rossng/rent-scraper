import json
from jinja2 import Template, Environment, PackageLoader

jinja_env = Environment(loader=PackageLoader('rent_scraper', package_path='templates'))

properties = []

for agent in ['abode', 'ubu', 'absolute', 'gough', 'tlg']:
    file = open('rent_scraper/properties_' + agent + '.json')
    properties += json.load(file)
    file.close()

property_template = jinja_env.get_template('template.html')

html = property_template.render({ 'properties' : properties })

output_file = open('results.html', 'w')
output_file.write(html.encode("UTF-8"))
output_file.close()