import boto3
import os
import pandas as pd
from scripts.data.es import insert_doc, change_es_host, get_all_indices
s3_resource = boto3.resource('s3')
from dotenv import dotenv_values
import datetime
import re
import time

temp = dotenv_values(".env")

sesssion = boto3.Session(temp['ACCESS_KEY_ID'], temp['SECRET_ACCESS_KEY'])

s3 = sesssion.resource('s3')


def main_s3(bucket_name, es_host, access_key_id, secret_access_key):
    if not os.path.exists(temp['TEMP_FOLDER']):
        os.makedirs(temp['TEMP_FOLDER'])
    
    change_es_host(es_host)

    sesssion = boto3.Session(access_key_id, secret_access_key)

    s3 = sesssion.resource('s3')


    already_added = get_all_indices()

    bucket = s3.Bucket(bucket_name)
    files_inserted = []
    for obj in bucket.objects.all():
        file_name = obj.key
        print(f"Doing {file_name}...")
        if do_repl(file_name) in already_added:
            print("File already added. Continuing...")
            continue
        
        if not os.path.exists(os.path.join(temp['TEMP_FOLDER'], file_name)):
            s3.Object(bucket_name, file_name).download_file(os.path.join(temp['TEMP_FOLDER'], file_name))
        insert_file_to_es(file_name)
        files_inserted.append(file_name)

    return files_inserted


def insert_file_to_es(file_name):
    df = pd.read_csv(os.path.join(temp['TEMP_FOLDER'], file_name))

    insert_doc(df, do_repl(file_name))

def do_repl(string):
    string = string.split(".")[-2].lower()
    return re.sub(r"[\s+\[\"\*\\\<\|\,\>,/\?\]]", "", string).lower()