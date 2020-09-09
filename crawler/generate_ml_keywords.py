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


def parse_tf_docs(tf_doc_url=None, prefix='tf'):
    data = {}
    base_url = tf_doc_url.split('?')[0]
    content = requests.get(tf_doc_url).text
    pattern = f"({base_url}/{prefix}/[a-zA-Z0-9_./#]+)"
    matches = re.findall(pattern, content, re.DOTALL)
    for link in matches:
        keyword_i = len(base_url) + 1
        kw = link[keyword_i:]
        kw = kw.replace('/', '.')
        kw_metadata = {'url': link}
        data[kw] = kw_metadata
    return data


def parse_tf_docs_local():
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
    seed_file = 'seed.yaml'
    seed = load_seed_file(seed_file)
    for tensorflow_doc in seed['tensorflow']:
        print(f'processing: {tensorflow_doc["name"]}')
        crawled = parse_tf_docs(tensorflow_doc['url'], tensorflow_doc['prefix'])
        data.update(crawled)
    for api_doc in seed['generated']:
        print(f'processing: {api_doc["name"]}')
        doc_url = api_doc['url']
        data.update(parse_generated_docs(doc_url))

    doc_file = '../data/ml.json'
    with open(doc_file, 'w') as f:
        json.dump(data, f)
