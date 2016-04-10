import json

config = {
    'baseurl': 'http://www.gumtree.com',
    'urls': [],
}

config.update(json.load(open('config.json', 'r')))
