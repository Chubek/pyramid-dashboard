import boto3
import os
import pandas as pd
from scripts.data.es import insert_doc
s3_resource = boto3.resource('s3')
from dotenv import dotenv_values
import datetime

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

def download_file(bucket_name):
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
    
    already_added = get_already_added()

    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.all():
        file_name = obj.key

        if file_name in already_added:
            continue
        dt = datetime.datetime.now()
        s3.Object(bucket_name, file_name).download_file(os.path.join("tmp", file_name))
        insert_file_to_es(file_name, f"{file_name}_{dt.day}/{dt.month}/{dt.year}")
        add_to_added(file_name)


def insert_file_to_es(file_name, index_name):
    df = pd.read_csv(os.path.join("tmp", file_name))

    insert_doc(df, index_name)

    os.remove(os.path.join("tmp", file_name))
