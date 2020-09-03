import json
import re

import requests
import yaml


# TODO automate this process
def prepare_base_keywords():
    base_file = '../data/base.json'
    with open(base_file, 'r') as f:
        data = json.load(f)
    return data


def parse_tf_docs():
    data = {}
    input_file = '/tmp/out/index.md'
    pattern = '<code>([a-zA-Z_.0-9]+)</code>'
    f = open(input_file, 'r')
    content = f.read()
    f.close()
    matches = re.findall(pattern, content, re.DOTALL)
    tf_base_url = 'https://www.tensorflow.org/api_docs/python'

    for i in matches:
        print(f"{tf_base_url}/{i.replace('.', '/')}")

    for k in matches:
        tf_doc_url = f"{tf_base_url}/{k.replace('.', '/')}"
        keyword_metadata = {'url': tf_doc_url}  # TODO add docs
        data[k] = keyword_metadata
    return data


def load_seed_file(file_name):
    with open(file_name, 'r') as stream:
        seed = yaml.safe_load(stream)
    return seed


def parse_generated_docs(link, pattern=None):
    data = {}
    base_url = link[:link.rfind('/')]
    resp = requests.get(link)
    if pattern is None:
        pattern = 'href="([a-zA-Z0-9_./#]+)"'
    matches = re.findall(pattern, resp.text, re.DOTALL)
    for href in matches:
        # generated urls tend to have package name and '#' mark included.
        # intentionally excluded __ functions
        if '.' in href and '#' in href and '__' not in href:
            _, k = href.split('#')
            if '.' in k:  # keyword is a package name
                doc_url = f'{base_url}/{href}'
                metadata = {'url': doc_url}
                data[k] = metadata

    return data


if __name__ == '__main__':
    data = prepare_base_keywords()
    data.update(parse_tf_docs())
    seed_file = 'seed.yaml'
    seed = load_seed_file(seed_file)
    for api_doc in seed['generated']:
        print(f'processing: {api_doc["name"]}')
        doc_url = api_doc['url']
        data.update(parse_generated_docs(doc_url))

    doc_file = '../data/ml.json'
    with open(doc_file, 'w') as f:
        json.dump(data, f)
