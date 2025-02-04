import json
import re
from pathlib import Path
from typing import Dict, Any

import requests
import yaml
from bs4 import BeautifulSoup

data_dir = f'{str(Path(__file__).resolve().parent.parent)}/data'


# TODO automate this process
def prepare_base_keywords():
    base_file = f'{data_dir}/base.json'
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


def parse_huggingface_main_classes() -> Dict[str, Any]:
    """Parse Hugging Face Transformers main API classes documentation.
    
    Returns:
        Dictionary mapping class names to their documentation URLs
    """
    data = {}
    base_domain = 'https://huggingface.co'
    
    # Get main class pages from the API reference page
    print('\nFetching main classes from API reference...')
    resp = requests.get(f'{base_domain}/docs/transformers/main_classes/configuration')
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Find the sidebar navigation
    main_class_pages = []
    for link in soup.select('a'):
        href = link.get('href', '')
        if '/main_classes/' in href:
            page_name = href.split('/')[-1]
            if page_name and page_name not in main_class_pages:
                main_class_pages.append(page_name)
    
    # Remove duplicates and sort
    main_class_pages = sorted(set(main_class_pages))
    
    print(f'\nFound main class pages: {main_class_pages}')
    print(f'Processing {len(main_class_pages)} main class pages...')
    
    # Process each main class page
    for page in main_class_pages:
        page_url = f'{base_domain}/docs/transformers/main_classes/{page}'
        
        try:
            resp = requests.get(page_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find all class sections (h2 and h3 headers)
            class_sections = soup.find_all(['h2', 'h3'])
            current_class = None
            
            # Track links for summary
            page_links = set()
            page_classes = set()
            
            # Process all links first
            for a in soup.find_all('a'):
                href = a.get('href', '')
                if href and '#transformers.' in href:
                    page_links.add(href)
            
            # Process class sections
            for section in class_sections:
                # Look for class name in the text
                class_match = re.search(r'class transformers\.(\w+)', section.text)
                if class_match:
                    current_class = class_match.group(1)
                    class_key = f'transformers.{current_class}'
                    page_classes.add(class_key)
                    
                    data[class_key] = {
                        'url': f'{page_url}#transformers.{current_class}'
                    }
                    continue
                
                section_id = section.get('id', '')
                if not section_id or section_id.startswith('_') or section_id.endswith('_'):
                    continue
                
                # If we're in a class context, this might be a method
                if current_class:
                    method_key = f'transformers.{current_class}.{section_id}'
                    data[method_key] = {
                        'url': f'{page_url}#transformers.{current_class}.{section_id}'
                    }
            
            # Print summary for this page
            print(f'\n{page.upper()}:')
            if page_classes:
                print(f'  Classes ({len(page_classes)}): {sorted(page_classes)}')
            print(f'  Total links: {len(page_links)}')
            
        except Exception as e:
            print(f'Error processing {page_url}: {str(e)}')
            continue
    
    return data

def parse_huggingface_docs(base_url: str, test_mode: bool = False) -> Dict[str, Any]:
    """Parse Hugging Face Transformers documentation.
    
    Args:
        base_url: The base URL of the Hugging Face documentation
        
    Returns:
        Dictionary mapping function/class names to their documentation URLs
    """
    data = {}
    base_domain = 'https://huggingface.co'
    
    # Get the main page content
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Find all model documentation links
    model_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'model_doc' in href:
            # Handle both absolute and relative URLs
            if href.startswith('http'):
                full_url = href
            elif href.startswith('//'):
                full_url = f'https:{href}'
            else:
                # Handle relative paths
                if href.startswith('/'):
                    full_url = f'{base_domain}{href}'
                else:
                    # Construct URL relative to the docs base path
                    docs_base = '/'.join(base_url.split('/')[:-1])
                    full_url = f'{docs_base}/{href}'
            model_links.append(full_url)
    
    # For testing, only process ZoeDepth
    if test_mode:
        model_links = ['https://huggingface.co/docs/transformers/model_doc/zoedepth']
    
    # Process each model's documentation
    for model_url in model_links:
        try:
            print(f'Processing {model_url}')
            print('Found model links:', len(model_links))
            model_resp = requests.get(model_url)
            model_soup = BeautifulSoup(model_resp.text, 'html.parser')
            
            # Extract model name from URL
            model_name = model_url.split('/')[-1].replace('-', '_')
            
            # Add the main model entry
            model_key = f'transformers.{model_name}'
            print(f'Adding model entry: {model_key}')
            data[model_key] = {
                'url': model_url
            }
            
            # Find all class definitions (h2 and h3 headers)
            class_sections = model_soup.find_all(['h2', 'h3'])
            current_class = None
            
            for section in class_sections:
                # Look for the class name in the text
                class_match = re.search(r'class transformers\.([\w]+)', section.text)
                if class_match:
                    current_class = class_match.group(1)
                    class_key = f'transformers.{model_name}.{current_class}'
                    print(f'Found class: {class_key}')
                    
                    data[class_key] = {
                        'url': f'{model_url}#transformers.{current_class.split(".")[-1]}'
                    }
                    continue
                
                section_id = section.get('id', '')
                if not section_id or section_id.startswith('_') or section_id.endswith('_'):
                    continue
                
                # If we're in a class context, this might be a method
                if current_class:
                    current_class = section_id
                    class_key = f'transformers.{model_name}.{current_class}'
                    print(f'Found class: {class_key}')
                    
                    # Get class description
                    desc = ''
                    next_p = section.find_next('p')
                    if next_p:
                        desc = next_p.text
                    
                    data[class_key] = {
                        'url': f'{model_url}#{section_id}',
                        'desc': desc
                    }
                    
                    # Find and add all methods in this class
                    method_sections = section.find_next(['h4', 'h5'])
                    while method_sections and method_sections.find_previous(['h2', 'h3']) == section:
                        method_id = method_sections.get('id', '')
                        if method_id and not method_id.startswith('_'):
                            method_key = f'{class_key}.{method_id}'
                            
                            # Get method description and parameters
                            desc = ''
                            params = []
                            next_elem = method_sections.find_next(['p', 'ul'])
                            while next_elem and next_elem.name in ['p', 'ul']:
                                if next_elem.name == 'p':
                                    desc += next_elem.text + ' '
                                elif next_elem.name == 'ul':
                                    for li in next_elem.find_all('li'):
                                        params.append(li.text)
                                next_elem = next_elem.find_next(['p', 'ul'])
                            
                            data[method_key] = {
                                'url': f'{model_url}#{method_id}',
                                'desc': desc.strip(),
                                'params': params
                            }
                        
                        method_sections = method_sections.find_next(['h4', 'h5'])
                
                # If we're in a class context, this might be a method
                elif current_class:
                    method_key = f'transformers.{model_name}.{current_class}.{section_id}'
                    
                    data[method_key] = {
                        'url': f'{model_url}#transformers.{current_class.split(".")[-1]}.{section_id}'
                    }
        
        except Exception as e:
            print(f'Error processing {model_url}: {str(e)}')
            continue
    
    return data


if __name__ == '__main__':
    # Load existing data if it exists
    doc_file = f'{data_dir}/ml.json'
    try:
        with open(doc_file, 'r') as f:
            data = json.load(f)
        print(f'Loaded {len(data)} existing entries')
    except FileNotFoundError:
        data = {}
    
    # Add base keywords if not present
    base_data = prepare_base_keywords()
    for key, value in base_data.items():
        if key not in data:
            data[key] = value
    
    seed_file = f'{data_dir}/seed.yaml'
    seed = load_seed_file(seed_file)
    
    # Process TensorFlow docs
    for tensorflow_doc in seed['tensorflow']:
        print(f'processing: {tensorflow_doc["name"]}')
        crawled = parse_tf_docs(tensorflow_doc['url'], tensorflow_doc['prefix'])
        data.update(crawled)
    
    # Process generated docs
    for api_doc in seed['generated']:
        print(f'processing: {api_doc["name"]}')
        doc_url = api_doc['url']
        
        # Special handling for Hugging Face Transformers
        if api_doc['name'] == 'transformers':
            print('Processing Hugging Face Transformers documentation...')
            crawled = parse_huggingface_docs(doc_url, test_mode=False)
            print(f'Crawled model data keys: {list(crawled.keys())}')
            # Preserve Hugging Face model entries
            for key, value in crawled.items():
                data[key] = value
                
            print('\nProcessing Hugging Face main API classes...')
            main_classes = parse_huggingface_main_classes()
            print('\nMain API Classes found:')
            for key, value in main_classes.items():
                print(f'  {key} -> {value["url"]}')
            # Add main API class entries
            for key, value in main_classes.items():
                data[key] = value
        else:
            data.update(parse_generated_docs(doc_url))

    print(f'Writing {len(data)} entries to {doc_file}')
    print('Sample keys:', list(data.keys())[:5], '...')
    print('Hugging Face keys:', [k for k in data.keys() if k.startswith('transformers.')])
    with open(doc_file, 'w') as f:
        json.dump(data, f, indent=2)
