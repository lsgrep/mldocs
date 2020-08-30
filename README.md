# Alfred mldocs
> Alfred Workflow for TensorFlow, PyTorch Python API docs(it requires `macOS`, `Alfred with Powerpack license`).

![demo](https://raw.githubusercontent.com/lsgrep/mldocs/master/assets/mldocs.gif)

## How to install
Checkout the [Releases](https://github.com/lsgrep/mldocs/releases), download `mldocs.alfredworkflow`, 
double click(You have to have Alfred + Powerpack License).

## How does it work
- `mldocs` fetches the doc data from Github(`data/ml.json`), then cache the data for a few days
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
| `colab` | `http://colab.research.google.com/`  |   |
| `kaggle` | `https://www.kaggle.com/` |    | 


## Supported Versions
- `ml.json` will be periodically updated to the latest stable versions of TensorFlow & PyTorch

## Keyword Descriptions
- Not supported yet, but will add them in the future.

## TODO
- [ ] add Github Actions to generate `ml.json`
- [ ] add keyword descriptions for TensorFlow
- [ ] add keyword descriptions for PyTorch

## Credits
Icon made by [Becris](https://creativemarket.com/Becris) from [Flaticon](https://www.flaticon.com/)
