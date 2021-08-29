import boto3
import os
import pandas as pd
from scripts.data.es import insert_doc, change_es_host
s3_resource = boto3.resource('s3')
from dotenv import dotenv_values
import datetime
import re

temp = dotenv_values(".env")

sesssion = boto3.Session(temp['ACCESS_KEY_ID'], temp['SECRET_ACCESS_KEY'])

s3 = sesssion.resource('s3')

def get_already_added():
    if not os.path.exists(temp['ADDED_FILE']):
        return []

    with open(temp['ADDED_FILE'], "r") as fr: 
        return fr.readlines()

def add_to_added(f):
    mode = 'a' if os.path.exists(temp['ADDED_FILE']) else 'w'
    
    with open(temp['ADDED_FILE'], mode) as faw:
        faw.write(f"{f}\n")

def get_already_indexed():
    if not os.path.exists(temp['INDEX_FILE']):
        return []

    with open(temp['INDEX_FILE'], "r") as fr: 
        return fr.readlines()

def add_to_index(f):
    mode = 'a' if os.path.exists(temp['INDEX_FILE']) else 'w'
    
    with open(temp['INDEX_FILE'], mode) as faw:
        faw.write(f"{f}\n")

def main_s3(bucket_name, es_host=temp[temp['MAIN_ES_HOST']]):
    if not os.path.exists(temp['TEMP_FOLDER']):
        os.makedirs(temp['TEMP_FOLDER'])
    
    already_added = get_already_added()

    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.all():
        file_name = obj.key
        print(f"Doing {file_name}...")
        if file_name in already_added:
            continue
        dt = datetime.datetime.now()
        
        if not os.path.exists(os.path.join(temp['TEMP_FOLDER'], file_name)):
            s3.Object(bucket_name, file_name).download_file(os.path.join(temp['TEMP_FOLDER'], file_name))
        change_es_host(es_host)
        insert_file_to_es(file_name)
        add_to_added(file_name)


def insert_file_to_es(file_name):
    df = pd.read_csv(os.path.join(temp['TEMP_FOLDER'], file_name))

    insert_doc(df, re.sub(r"[\s\[\"\*\\\<\|\,\>,/\?\]-]", "", file_name.split(".")[-2]).lower())

    add_to_index(re.sub(r"[\s\[\"\*\\\<\|\,\>,/\?\]-]", "", file_name.split(".")[-2]).lower())

    #os.remove(os.path.join("tmp", file_name))
