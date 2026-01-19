from sklearn.model_selection import train_test_split
from sklearn import metrics
from xgboost import XGBClassifier
from catboost import CatBoostClassifier


DEFAULT_FEATURES_LIST = ['url_len', 'response_time_sec', 'response_time_2_sec', 'cache-control_cat', 'content-type_cat','pragma_cat', 'ttl', 'response_time_ratio', 'response_time_diff',
                         'x_xss_protection_cat', 'is_utf_8', 'is_php', "keepalive_timeout", "keepalive_max", 'x-powered-by_cat', 'dns_time_sec', 'dns_time_2_sec', 'cachecontrol_max', 'nel_cat',
                         'a_tag_count', 'x-ua-compatible_cat', 'dash_count', 'www_count', 'content-encoding_cat', 'server_cat', 'content-length_new']
DEFAULT_SCALE_POS_WEIGHT = 100000000  # Should be adjusted to data size and distribution
DEFAULT_MAX_DEPTH = 20
DEFAULT_ITERATIONS = 50


def normalize_df(responses_labeled_df, features_list=DEFAULT_FEATURES_LIST):
	existing_features_list = [x for x in features_list if x in responses_labeled_df.columns]
	X = responses_labeled_df[features_list]              
	y = responses_labeled_partial_df.label
	return X, y
	

def split_df(X, y, ratio=0.3):
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ratio, random_state=1)
	return X_train, X_test, y_train, y_test
	

def train_xgboost(X_train, y_train, X_test=None, y_test=None, scale_pos_weight=DEFAULT_SCALE_POS_WEIGHT, max_depth=DEFAULT_MAX_DEPTH, **kwargs):
	clf = XGBClassifier(scale_pos_weight=scale_pos_weight, max_depth=max_depth)
	clf = clf.fit(X_train, y_train)
	print_model_metrics(clf, X_train, y_train, X_test=X_test, y_test=y_test)
		
	return clf

	
def train_catboost(X_train, y_train, X_test=None, y_test=None, iterations=DEFAULT_ITERATIONS, learning_rate=1, scale_pos_weight=DEFAULT_SCALE_POS_WEIGHT, max_depth=DEFAULT_MAX_DEPTH, **kwargs):
	clf = CatBoostClassifier(iterations=iterations, learning_rate=learning_rate, depth=max_depth, scale_pos_weight=scale_pos_weight)
	clf = clf.fit(X_train, y_train)
	print_model_metrics(clf, X_train, y_train, X_test=X_test, y_test=y_test)
	
	return clf
	
	
def print_model_metrics(clf, X_train, y_train, X_test=None, y_test=None, digits_precision=3):
	print("Features used:")
	print(list(X_test.columns))
	print("Train:")
	print(metrics.classification_report(y_train, clf.predict(X_train), digits=digits_precision))
	if X_test:
		y_pred = clf.predict(X_test)
		print("Test:")
		print(metrics.classification_report(y_test, y_pred, digits=digits_precision))
  
