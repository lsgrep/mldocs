import json
import re

import requests


# TODO automate this process


def prepare_base_keywords():
    base_file = '../data/base.json'
    with open(base_file, 'r') as f:
        data = json.load(f)
    return data


def prepare_sklearn_keywords():
    data = {}
    sklearn_index = 'https://scikit-learn.org/stable/modules/classes.html'
    sklearn_base = 'https://scikit-learn.org/stable/modules'
    resp = requests.get(sklearn_index)
    pattern = 'href="(generated/[a-zA-Z._/#]+)"'
    matches = re.findall(pattern, resp.text, re.DOTALL)
    for i in matches:
        if "." in i and "#" in i:
            _, k = i.split('#')
            k_url = f'{sklearn_base}/{i}'
            keyword_metadata = {'url': k_url}
            data[k] = keyword_metadata
    return data


def prepare_tf_keywords():
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


def prepare_torch_keywords():
    data = {}
    pytorch_index_url = 'https://pytorch.org/docs/master/genindex.html'
    pytorch_base_url = 'https://pytorch.org/docs/master'
    resp = requests.get(pytorch_index_url)
    pattern = 'href="([a-zA-Z0-9_./#]+)"'
    matches = re.findall(pattern, resp.text, re.DOTALL)

    for link in matches:
        if '.' in link and '#' in link:
            _, k = link.split('#')
            pytorch_doc_url = f'{pytorch_base_url}/{link}'
            keyword_metadata = {'url': pytorch_doc_url}  # TODO add docs
            data[k] = keyword_metadata
    return data


if __name__ == '__main__':
    data = prepare_base_keywords()
    data.update(prepare_tf_keywords())
    data.update(prepare_torch_keywords())
    data.update(prepare_sklearn_keywords())
    output_file = '../data/ml.json'
    print(data)
    with open(output_file, 'w') as f:
        json.dump(data, f)
