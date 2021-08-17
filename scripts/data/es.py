from elasticsearch import Elasticsearch
from dotenv import dotenv_values
from elasticsearch import helpers

temp = dotenv_values(".env")

es = Elasticsearch([temp['ES_HOST']], maxsize=25)


def get_results(index_name, query_type, field_name, field_match):
    return es.search(index=index_name, body={"query":{query_type:{field_name: field_match}}})


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