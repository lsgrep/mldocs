#!/usr/bin/python
# encoding: utf-8
import json
import math
import os
import string
import sys

import requests

from workflow import ICON_INFO
# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3, web


def get_ml_docs():
    data_url = 'https://raw.githubusercontent.com/lsgrep/mldocs/master/data/ml.json'
    result = web.get(data_url)
    # throw an error if request failed
    # Workflow will catch this and show it to the user
    result.raise_for_status()
    return result.json()


def get_ml_docs_local():
    with open('data/ml.json') as f:
        data = json.load(f)
    return data


def get_assets():
    asset_dir = 'assets'
    icon_suffix = '.icns'
    assets = os.listdir(asset_dir)
    res = {}
    for i in assets:
        if i.lower().endswith(icon_suffix):
            asset, _ = i.split('.')
            res[asset] = '{}/{}'.format(asset_dir, i)
    return res


def parse_domain(link):
    return link.split("//")[-1].split("/")[0]


# expand commonly used prefixes
# plt => pyplot
# sns => seaborn
# np => numpy
# pd => pandas
def expand_args(args):
    for i, arg in enumerate(args):
        if arg == 'plt':
            args[i] = 'pyplot'
            continue

        if arg.startswith('plt.'):
            _, rem = arg.split('.')
            args[i] = 'pyplot.' + rem
            continue

        if arg == 'sns':
            args[i] = 'seaborn'
            continue

        if arg.startswith('sns.'):
            _, rem = arg.split('.')
            args[i] = 'seaborn.' + rem
            continue

        if arg.lower() == 'np':
            args[i] = 'numpy'
            continue

        if arg.startswith('np.'):
            _, rem = arg.split('.')
            args[i] = 'numpy.' + rem
            continue

        if arg.lower() == 'pd':
            args[i] = 'pandas'
            continue

        if arg.startswith('pd.'):
            _, rem = arg.split('.')
            args[i] = 'pandas.' + rem
            continue

    return args


# Perfectly balanced, as all things should be
def search_priority_len(k):
    if "keras" in k.lower():
        return len(k) * (1 + math.pi) / 10.0
    if "torch" in k.lower():
        return len(k) * math.pi / 4.0
    else:
        return len(k)


def search(args, keywords):
    # args is lower case already
    args = expand_args(args)
    # performance hack, eliminate dot expression
    lower = string.lower
    for k in args:
        keywords = [i for i in keywords if k in lower(i)]
    result = sorted(keywords, key=search_priority_len)
    return result


def custom_search(title, base_url, asset, args_index=1):
    global wf
    query_str = ' '.join(wf.args[args_index:])
    query_url = base_url + requests.utils.quote(query_str)
    wf.add_item(title=title + ' ' + query_str,
                subtitle=query_url,
                arg=query_url,
                valid=True,
                icon=asset)


# make one big pickle, and make single disk read
def get_data():
    return get_ml_docs(), get_assets()


def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)`
    # import somemodule
    # import anothermodule

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = [i.lower() for i in wf.args]
    ml_data, assets = wf.cached_data('data', get_data, max_age=3600 * 24 * 3)
    asset_keywords = sorted(assets.keys(), key=len)

    if len(args) > 1 and args[0] == 'gds':
        gds_search = 'https://datasetsearch.research.google.com/search?query='
        title = 'Google Dataset Search'
        custom_search(title, base_url=gds_search, asset=assets['google'])
    elif len(args) > 1 and args[0] == 'paper':
        paper_search = 'http://paperswithcode.com/search?q='
        title = 'Papers With Code'
        custom_search(title, base_url=paper_search, asset=assets['paper'])
    else:
        result = search(args, ml_data.keys())
        # nothing to be found, let's Google
        if len(result) == 0:
            google_search = 'https://www.google.com/search?q='
            title = 'Google Search'
            # will use all the args
            custom_search(title, base_url=google_search, asset=assets['google'], args_index=0)
        else:
            for ml_keyword in result[:15]:
                doc_link = ml_data[ml_keyword]['url']
                doc_desc = doc_link  # default value

                # if there is a desc, we use it
                if ml_data[ml_keyword].get('desc'):
                    doc_desc = ml_data[ml_keyword]['desc']
                icon = None

                # if the asset is available
                for k in asset_keywords:
                    if k in parse_domain(doc_link):
                        icon = assets[k]

                wf.add_item(title=ml_keyword,
                            subtitle=doc_desc,
                            arg=doc_link,
                            valid=True,
                            icon=icon)

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3(update_settings={'github_slug': 'lsgrep/mldocs',
                                    'frequency': 3})
    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item('New version available',
                    'Upgrade mldocs workflow',
                    autocomplete='workflow:update',
                    icon=ICON_INFO)

    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
