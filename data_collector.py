import pandas as pd


def extract_features_from_df(responses_labeled_df, full_url_len=False, use_keepalive_timeout=True, use_dns_time_2=False, top_domains_limit=20000):
	responses_labeled_partial_df = responses_labeled_df.drop_duplicates('url').copy()
	responses_labeled_partial_df["content-type"] = responses_labeled_partial_df["content-type"].astype('category')
	responses_labeled_partial_df["content-type_cat"] = responses_labeled_partial_df["content-type"].cat.codes
	if full_url_len:
		responses_labeled_partial_df["url_len"] = responses_labeled_partial_df["url"].apply(len)
	else:
    # Only domain length
		responses_labeled_partial_df["url_len"] = responses_labeled_partial_df["url"].apply(lambda x: len(x.replace("https://", "").replace("http://", "").split("/")[0]))
	responses_labeled_partial_df["response_time_sec"] = responses_labeled_partial_df["response_time"].apply(lambda x: pd.Timedelta(x).to_pytimedelta().total_seconds())
	responses_labeled_partial_df["response_time_2_sec"] = responses_labeled_partial_df["response_time_2"].apply(lambda x: pd.Timedelta(x).to_pytimedelta().total_seconds())
	responses_labeled_partial_df["response_time_ratio"] = responses_labeled_partial_df.apply(lambda x: pd.Timedelta(x['response_time_2']).to_pytimedelta().total_seconds() / pd.Timedelta(x['response_time']).to_pytimedelta().total_seconds(), axis=1)
	responses_labeled_partial_df["response_time_diff"] = responses_labeled_partial_df.apply(lambda x: pd.Timedelta(x['response_time_2']).to_pytimedelta().total_seconds() - pd.Timedelta(x['response_time']).to_pytimedelta().total_seconds(), axis=1)
	responses_labeled_partial_df['cache-control_cat'] = responses_labeled_partial_df['cache-control'].astype('category').cat.codes
	responses_labeled_partial_df["content-encoding_cat"] = responses_labeled_partial_df["content-encoding"].astype('category').cat.codes
	responses_labeled_partial_df["server_cat"] = responses_labeled_partial_df["server"].astype('category').cat.codes
	responses_labeled_partial_df["pragma_cat"] = responses_labeled_partial_df["pragma"].astype('category').cat.codes
	responses_labeled_partial_df["content-length_new"] = responses_labeled_partial_df["content-length"].apply(lambda x: 0 if (str(x).lower() == "nan" or x is None) else x).astype(int)
	responses_labeled_partial_df["age_new"] = responses_labeled_partial_df["age"].apply(lambda x: 0 if str(x).lower() == "nan" else x)
	responses_labeled_partial_df["is_php"] = responses_labeled_partial_df["x-powered-by"].apply(lambda x: "php" in str(x).lower()).astype('category').cat.codes
	responses_labeled_partial_df["is_dotnet"] = responses_labeled_partial_df["x-powered-by"].apply(lambda x: "asp.net" in str(x).lower()).astype('category').cat.codes
	responses_labeled_partial_df["is_utf_8"] = responses_labeled_partial_df["content-type"].apply(lambda x: "utf-8" in str(x).lower()).astype('category').cat.codes
	if use_keepalive_timeout:
		responses_labeled_partial_df["keepalive_timeout"] = responses_labeled_partial_df["keep-alive"].apply(lambda x: -1 if "timeout" not in str(x) else int(x.split("timeout=")[1].split(",")[0]))
	responses_labeled_partial_df["keepalive_max"] = responses_labeled_partial_df["keep-alive"].apply(lambda x: -1 if "max" not in str(x) else int(x.split("max=")[1].split(",")[0]))
	responses_labeled_partial_df["cachecontrol_max"] = responses_labeled_partial_df["cache-control"].apply(lambda x: -1 if "max-age=" not in str(x) else int(x.split("max-age=")[1].split(",")[0].replace(";", "")))
	responses_labeled_partial_df["cachecontrol_max"] = responses_labeled_partial_df["cachecontrol_max"].apply(lambda x: -2 if str(x) == "nan" else x)  # Handle edge case
	responses_labeled_partial_df['has_outlook'] = responses_labeled_partial_df["url"].apply(lambda x: "outlook" in str(x).lower()).astype('category').cat.codes
	responses_labeled_partial_df['has_bank'] = responses_labeled_partial_df["url"].apply(lambda x: "bank" in str(x).lower()).astype('category').cat.codes
	responses_labeled_partial_df["alt_svc_ma"] = responses_labeled_partial_df["alt-svc"].apply(lambda x: -1 if "ma" not in str(x) else int(x.split("ma=")[1].split(",")[0].split(";")[0]))
	responses_labeled_partial_df["x_xss_protection_cat"] = responses_labeled_partial_df["x-xss-protection"].astype('category').cat.codes
	responses_labeled_partial_df["nel_cat"] = responses_labeled_partial_df["nel"].astype('category').cat.codes
	responses_labeled_partial_df['dash_count'] = responses_labeled_partial_df["url"].apply(lambda x: x.count("-"))
	responses_labeled_partial_df['underscore_count'] = responses_labeled_partial_df["url"].apply(lambda x: x.count("_"))
	responses_labeled_partial_df["dns_time_sec"] = responses_labeled_partial_df["dns_time"].apply(lambda x: pd.Timedelta(x).to_pytimedelta().total_seconds())
	if use_dns_time_2:
		responses_labeled_partial_df["dns_time_2_sec"] = responses_labeled_partial_df["dns_time_2"].apply(lambda x: pd.Timedelta(x).to_pytimedelta().total_seconds())
	responses_labeled_partial_df["a_tag_count"] = responses_labeled_partial_df["content"].apply(lambda x: str(x).count("<a>"))
	responses_labeled_partial_df['x-ua-compatible_cat'] = responses_labeled_partial_df['x-ua-compatible'].astype('category').cat.codes
	responses_labeled_partial_df["x-powered-by_cat"] = responses_labeled_partial_df["x-powered-by"].astype('category').cat.codes
	responses_labeled_partial_df['content_str_len'] = responses_labeled_partial_df['content'].apply(len)
	responses_labeled_partial_df['has_suspicious_strings'] = responses_labeled_partial_df['url'].apply(lambda x: len([y for y in {'pay', 'whats', 'face', 'google', 'bet', 'telegra', 'airbnb', 'amazon', 'github'} if y in x.lower()]))
	responses_labeled_partial_df['www_count'] = responses_labeled_partial_df["url"].apply(lambda x: x.count("www."))

  return responses_labeled_partial_df
