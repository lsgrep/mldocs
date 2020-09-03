# Alfred mldocs
> Alfred workflow for searching essential machine learning library API docs(it requires `macOS`, `Alfred with Powerpack license`).

![demo](https://raw.githubusercontent.com/lsgrep/mldocs/master/assets/mldocs.gif)

## Supported Libraries(all stable versions unless specified otherwise)
- [TensorFlow](https://www.tensorflow.org/api_docs/python/tf?hl=en)
- [PyTorch](https://pytorch.org/docs/stable/index.html)
- [NumPy](https://numpy.org/doc/stable/reference/)
- [Pandas](https://pandas.pydata.org/docs/reference/index.html)
- [Matplotlib](https://matplotlib.org/3.2.2/api/index.html) `v3.2.2`
- [Scikit-learn](https://scikit-learn.org/stable/modules/classes.html)
- [Statsmodels](https://www.statsmodels.org/stable/index.html)

## Install
Checkout the [Releases](https://github.com/lsgrep/mldocs/releases), download the latest `mldocs.alfredworkflow`,
then double click it(You have to have Alfred + Powerpack License).

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


## Supported Versions
- `ml.json` will be periodically updated to the latest stable versions of TensorFlow & PyTorch

## Keyword Descriptions
- Not supported yet, but will add them in the future.

## TODO
- [x] add Scikit-learn support
- [x] add NumPy support
- [x] add Pandas support 
- [x] add Matplotlib support
- [x] add Statsmodels support
- [ ] add Github Actions to generate `ml.json`
- [ ] add keyword descriptions for TensorFlow
- [ ] add keyword descriptions for PyTorch


## Credits
Icon made by [Becris](https://creativemarket.com/Becris) from [Flaticon](https://www.flaticon.com/)
