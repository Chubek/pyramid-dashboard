from elasticsearch import Elasticsearch
from dotenv import dotenv_values
from elasticsearch import helpers
import pandas as pd
from scripts.util.to_datetime import to_datetime
import numpy as np
import time

temp = dotenv_values(".env")

current_es_host = temp['MAIN_ES_HOST']
es = Elasticsearch([{'host': temp['MAIN_ES_HOST'], 'port': 443}], use_ssl=True, verify_certs=True)

def change_es_host(new_host):
    global es, current_es_host
    
    if new_host != current_es_host:
        es = Elasticsearch([{'host': new_host, 'port': 443}], use_ssl=True, verify_certs=True)
        current_es_host = new_host


def get_all_indices():
    return [l for l in list(es.indices.get_alias("*").keys()) if l != ".kibana_1"]

def get_results(index_name, query_type, field_name, field_match):
    res = es.search(index=index_name, body={"query":{query_type:{field_name: field_match}}})

    sources = [r['_source'] for r in res['hits']['hits']]

    df = pd.DataFrame(sources)

    df[temp['DATE_TIME_COLUMN']] = df[temp['DATE_TIME_COLUMN']].apply(lambda x: to_datetime(x))

    return df


def get_all_results(index_name, es_host):
    print("Changing host...")
    change_es_host(es_host)
    print("Host changed... Retrieving data.")
    res = es.search(index=index_name, body={"query":{"match_all":{}}})

    print("Data retrieved.")
    sources = [r['_source'] for r in res['hits']['hits']]

    df = pd.DataFrame(sources)

    print(f"Got {len(df)} records.")

    print(df.columns)
    df[temp['DATE_TIME_COLUMN']] = df[temp['DATE_TIME_COLUMN']].apply(lambda x: to_datetime(x))

    return df

def doc_generator(df, index_name):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
                "_index": index_name,
                "_type": "_doc",
                "_id" : index,
                "_source": document.to_dict(),
            }
    return True

def insert_doc(df, index_name):
    helpers.bulk(es, doc_generator(df, index_name))