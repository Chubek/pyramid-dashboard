from elasticsearch import Elasticsearch
from dotenv import dotenv_values
from elasticsearch import helpers
import pandas as pd
from scripts.util.to_datetime import to_datetime

temp = dotenv_values(".env")

es = Elasticsearch([temp['ES_HOST']], maxsize=25)


def get_results(index_name, query_type, field_name, field_match):
    res = es.search(index=index_name, body={"query":{query_type:{field_name: field_match}}})

    sources = [r['_source'] for r in res['hits']['hits']]

    df = pd.DataFrame(sources)

    df[temp['DATE_TIME_COLUMN']] = df[temp['DATE_TIME_COLUMN']].apply(lambda x: to_datetime(x))

    return df


def get_all_results(index_name):
    res = es.search(index=index_name, body={"query":{"match_all":{}}})


    sources = [r['_source'] for r in res['hits']['hits']]

    df = pd.DataFrame(sources)

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
    return helpers.bulk(es, doc_generator(df, index_name))