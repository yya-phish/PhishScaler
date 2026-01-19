import socket
import datetime
import subprocess
import pandas as pd
import requests


def prepare_df(websites_path, to_shuffle=True, remove_domain_families=True, remove_http=True, remove_weebly=True):
  """ Used for filtering out irrelevant URLs when multiple datasources are used. Should not be used on a single data source"""
	urls_df = pd.read_csv(websites_path)
	if remove_http:
		urls_df['url'] = urls_df['url'].apply(lambda x: str(x) if ("http://" in str(x) or "https://" in str(x)) else "https://" + str(x))
	urls_df['url'] = urls_df['url'].apply(lambda x: x[:-1] if x[-1] == '/' else x)
	if remove_domain_families and remove_http:
		urls_partial_df = urls_partial_df[urls_df['url'].apply(lambda x: "*" not in x and x.count(":") < 2 and x[:-1].count("/") < 3 and "http://" not in x)]
	urls_partial_df = urls_partial_df[urls_partial_df['url'].apply(lambda x: "weebly" not in x)]
	urls_partial_df = urls_partial_df.drop_duplicates('url', keep='last')
	if to_shuffle:
		urls_partial_df = urls_partial_df.sample(len(urls_partial_df), random_state=1)
	return urls_partial_df
	

def collect_data(urls_df, limit=None, save_path=None, print_progress=50, save_backups_method=[250,49]):
  """
  Sends required requests to URLs and collects responses.
  save_backups_method - [x, y] saves the current collected data every x URLs, when idx%x=y.
  """
	http_responses = []
	resp_times = []
	resp_times_2 = []
	dns_times = []
	dns_times_2 = []
	scanned_urls = []
	phish_lbls = []
	ttls_lst = []

	if limit:
		urls_df = urls_df[:limit]
	for idx, web_url in enumerate(urls_df['url']):
		if print_progress and idx % print_progress == 1:
			print('---------------------------------------------------------')
			print(idx)
			print(len(dns_times))
		if save_backups_method and idx % save_backups_method[0] == save_backups_method[1]:
			tmpp_responses_df = pd.DataFrame.from_dict([{k.lower(): v for k, v in [("url", scanned_urls[i]),
																				   ("label", phish_lbls[i]),
																				   ("ttl", ttls_lst[i]),
																				   ("response_time", resp_times[i]),
																				   ("response_time_2", resp_times_2[i]),
																				   ("content", x.content),
																				   ("dns_time", dns_times[i]),
																				   ("dns_time_2", dns_times_2[i])] + list(dict(x.headers).items())} for i, x in enumerate(http_responses)])
			tmpp_responses_df.to_parquet("tmpp_resp_df_backup_" + str(CONCURRENCY_INDEX) + ".parquet")
			tmpp_responses_df = pd.DataFrame.from_dict([{k.lower(): v for k, v in [("url", scanned_urls[i]),
																				   ("label", phish_lbls[i]),
																				   ("ttl", ttls_lst[i]),
																				   ("response_time", resp_times[i]),
																				   ("response_time_2", resp_times_2[i]),
																				   ("dns_time", dns_times[i]),
																				   ("dns_time_2", dns_times_2[i])] + list(dict(x.headers).items())} for i, x in enumerate(http_responses)])
			tmpp_responses_df.to_csv("tmpp_resp_df_backup_no_content_" + str(CONCURRENCY_INDEX) + ".csv")
			print("Saved backup")
		
        try:
            cur_time = datetime.datetime.now()
            dns_url = web_url.replace("http://", "").replace("https://", "")
            dns_url = dns_url if dns_url[-1] != "/" else dns_url[:-1]
            dns_url = dns_url.split("/")[0]
            socket.getaddrinfo(dns_url, 80)
            cur_dns_time_diff = datetime.datetime.now() - cur_time
            cur_time = datetime.datetime.now()
            socket.getaddrinfo(dns_url, 80)
            cur_dns_time_diff_2 = datetime.datetime.now() - cur_time

            cur_time = datetime.datetime.now()
            http_response = requests.get(web_url, timeout=5)
            cur_time_1_diff = datetime.datetime.now() - cur_time
            p = subprocess.Popen(["ping", "-4", "-n", "1", web_url.replace("https://", "").replace("http://", "")], stdout=subprocess.PIPE)
            res=p.communicate()[0]

            if "Request timed out." in str(res) or "Ping request could not find host" in str(res) or "Destination net unreachable" in str(res) or "TTL expired in transit" in str(res):
                ttl_to_append = 0
            else:
                if "TTL=" in str(res):
                    ttl_to_append = int(str(res).split("TTL=")[1].split("\\r\\n")[0])
                else:
                    print(res)
                    ttl_to_append = 0
            if http_response.status_code != 200:
                print(http_response.status_code)
            cur_time = datetime.datetime.now()
            http_response = requests.get(web_url, timeout=5)
            cur_time_diff = datetime.datetime.now() - cur_time
            scanned_urls.append(web_url)
            http_responses.append(http_response)
            resp_times.append(cur_time_1_diff)
            resp_times_2.append(cur_time_diff)
            phish_lbls.append(list(cur_urls_df['phish_prediction'][idx:idx+1])[0])
            dns_times.append(cur_dns_time_diff)
            dns_times_2.append(cur_dns_time_diff_2)
            ttls_lst.append(ttl_to_append)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.InvalidURL,
                requests.exceptions.TooManyRedirects,
                requests.exceptions.SSLError,
                socket.error,
                socket.gaierror) as exc:
            print(web_url, dns_url, exc)
            print()
	
	responses_df = pd.DataFrame.from_dict([{k.lower(): v for k, v in [("url", scanned_urls[i]),
																	  ("label", phish_lbls[i]),
																	  ("ttl", ttls_lst[i]),
																	  ("response_time", resp_times[i]),
																	  ("response_time_2", resp_times_2[i]),
																	  ("content", x.content),
																	  ("dns_time", dns_times[i]),
																	  ("dns_time_2", dns_times_2[i])] + list(dict(x.headers).items())} for i, x in enumerate(http_responses)])
																	  
	if save_path:
		responses_df.to_parquet(save_path + ".parquet")
	
	return responses_df
	
