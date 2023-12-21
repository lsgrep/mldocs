# Alfred mldocs
> Alfred workflow for searching essential machine learning library API docs(it requires `macOS`, `Alfred with Powerpack license`).
![demo](https://raw.githubusercontent.com/lsgrep/mldocs/master/assets/mldocs.gif)

## Supported Libraries(all stable versions unless specified otherwise)
- [TensorFlow](https://www.tensorflow.org/api_docs/python/tf?hl=en) `nightly`
- [PyTorch](https://pytorch.org/docs/stable/index.html)
- [NumPy](https://numpy.org/doc/stable/reference/)
- [Pandas](https://pandas.pydata.org/docs/reference/index.html)
- [Matplotlib](https://matplotlib.org/3.2.2/api/index.html) `v3.2.2`
- [Scikit-learn](https://scikit-learn.org/stable/modules/classes.html)
- [Statsmodels](https://www.statsmodels.org/stable/index.html)
- [Seaborn](https://seaborn.pydata.org/api.html)
- [Jax](https://jax.readthedocs.io/en/latest/jax.html)
- [Ray](https://docs.ray.io/en/latest/genindex.html)
- [Langchain](https://api.python.langchain.com/en/latest/langchain_api_reference.html)

## Install
Checkout the [Releases](https://github.com/lsgrep/mldocs/releases), download the latest `mldocs.alfredworkflow`,
then double click it(You have to have Alfred + Powerpack License).
For MacOS Monterey or newer versions, please install `1.x.x` or new versions.
For older MacOS versions, please use `0.0.5`.

## Update
There is a background process that checks update every 7 days, 
and there will be an option to upgrade to the latest version.
![demo](https://raw.githubusercontent.com/lsgrep/mldocs/master/assets/update-demo.jpg)

- `ml workflow:update` will force update.
- `ml workflow:noautoupdate` will turn off the auto update.
- `ml workflow:autoupdate` will enable the auto update.

## Conventions
For convenience, a few prefixes are automatically expanded(see [PR](https://github.com/lsgrep/mldocs/pull/8) for more).
- `np` => `numpy`
- `pd` => `pandas`
- `plt` => `pyplot`
- `sns` => `seaborn`

## How does it work
- `mldocs` fetches the doc data from Github(`data/ml.json`), then caches the data for a few days
- The first query will be slow then it will be pretty fast afterwards
- The plan is to update the `ml.json` periodically, so you won't have to update the workflow manually

## Clear the Cache
To force update the local cache
- `ml workflow:delcache`

## Commonly used keywords
I've also merged my commonly used links(`data/base.json`) into the `ml.json` as well. 
If you want to add your favorite website or link please submit a PR(just edit the `base.json`).


| `keyword`   | `link`  | `description`  | 
|---|---|---|
| `?`     | `https://github.com/lsgrep/mldocs`  |   |
| `colab` | `http://colab.research.google.com/`  |   |
| `kaggle` | `https://www.kaggle.com/` |    | 
| `Google Dataset Search` | `https://datasetsearch.research.google.com/` |    | 
| `gds` | `https://datasetsearch.research.google.com/` |    | 
| `paper` | `https://paperswithcode.com/` |    |

## Google Dataset Search
You can enter the query directly in the Alfred with the keyword `ml gds KEYWORD...`
![demo](https://raw.githubusercontent.com/lsgrep/mldocs/master/assets/gds-demo.jpg)

## [Papers With Code](https://paperswithcode.com/)
You can enter the query directly in the Alfred with the keyword `ml paper KEYWORD...`
![demo](https://raw.githubusercontent.com/lsgrep/mldocs/master/assets/papers-with-code-demo.jpg)

## Supported Versions
- `ml.json` will be periodically updated to the latest versions of TensorFlow & PyTorch

## Keyword Descriptions
- Not supported yet, but will add them in the future.

## TODO
- [x] add Scikit-learn support
- [x] add NumPy support
- [x] add Pandas support 
- [x] add Matplotlib support
- [x] add Statsmodels support
- [x] add Seaborn support
- [x] add Jax support
- [x] Add Ray support
- [x] Add LightGBM support
- [x] Add XGBoost support
- [x] add Automatic Update
- [ ] add Github Actions to generate `ml.json`
- [ ] add keyword descriptions for TensorFlow
- [ ] add keyword descriptions for PyTorch


## Credits
Icon made by [Becris](https://creativemarket.com/Becris) from [Flaticon](https://www.flaticon.com/)
