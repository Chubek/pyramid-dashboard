from scripts.data.s3 import main_s3
import sys
from dotenv import dotenv_values

temp = dotenv_values(".env")


if __name__ == "__main__":
    bucket_name = sys.argv[1]
    es_host = sys.argv[2]

    if bucket_name == "env":
        main_s3(temp["MAIN_BUCKET"], temp["MAIN_ES_HOST"])
    else:
        main_s3(bucket_name, es_host)