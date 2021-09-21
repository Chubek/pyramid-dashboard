from dotenv import main
from flask import Flask, request, jsonify
from scripts.data.s3 import main_s3
from scripts.data.filter_by_time import *
from scripts.data.filter_data import *
from scripts.data.es import get_all_indices, get_all_results
from scripts.util.format_date import *
from flask_cors import CORS, cross_origin
import datetime


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/insert_from_s3", methods=["POST"])
@cross_origin()
def insert_flask():
    es_host = request.form['es_host']
    access_key_id = request.form['access_key_id']
    secret_access_key = request.form['secret_access_key']
    bucket_name = request.form['bucket_name']

    result = main_s3(bucket_name, es_host, access_key_id, secret_access_key)

    return jsonify({"inserted_files": result})


@app.route("/get_all_results", methods=["POST"])
@cross_origin()
def get_flask():
    es_host = request.form['es_host']
    index_name = request.form['index_name']

    results = get_all_results(index_name, es_host)

    return jsonify({"data": results.to_dict()})


@app.route("/get_results_with_added_days", methods=["POST"])
@cross_origin()
def get_days():
    es_host = request.form['es_host']
    index_name = request.form['index_name']
    days = int(request.form['days'])

    df = get_all_results(index_name, es_host)

    results = filter_daily(df, datetime.datetime.today(), days)

    return jsonify({"inserted_files": results})