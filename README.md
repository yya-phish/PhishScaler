# PhishScaler

PhishScaler is a phishing detection framework, based on the collection of network-based features, spanning across the different levels of the network stack (from the network and transport layers to the applicative layer), as well as features extracted from the website’s content metadata and the content itself.

## Getting Started

### Installing

* Install requirements.txt

### Collecting data

* Read a dataframe (from csv, parquet, etc.) of URLs and their labels (0 for benign, 1 for phishing). Labels can be also updated later.
* Run on urls_df:
```
from data_collector import collect_data
responses_df = collect_data(urls_df)
```

### Feature extraction

On responses dataframe, run:
```
from feature_extraction import extract_features_from_df
extacted_df = extract_features_from_df(responses_df)
```

### Training and Testing

To train a model (e.g., XGBoost):
```
from trainer import normalize_df, split_df, train_xgboost, train_catboost, print_model_metrics
normalized_df = normalize_df(extacted_df)
X_train, X_test, y_train, y_test = split_df(normalized_df)
clf = train_xgboost(X_train, y_train, X_test, y_test, scale_pos_weight=1000) # scale_pos_weight should be adjusted to achieve the required precision-recall tradeoff.
```
To test the trained model and print accuracy metrics (or to predict on new data):
```
print_model_metrics(clf, X_train, y_train, X_test, y_test)
```

## License

Shield: [![CC BY-NC-ND 4.0][cc-by-nc-nd-shield]][cc-by-nc-nd]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International License][cc-by-nc-nd].

[![CC BY-NC-ND 4.0][cc-by-nc-nd-image]][cc-by-nc-nd]

[cc-by-nc-nd]: http://creativecommons.org/licenses/by-nc-nd/4.0/
[cc-by-nc-nd-image]: https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png
[cc-by-nc-nd-shield]: https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg
