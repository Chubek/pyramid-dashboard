# Dashboard App Backend

## URL
The API is hosted at the following URLs:
```
54.242.81.180
pyramid.chubakbidpaa.com
```


## Endpoints


### Get from S3 to ES

```
Endpoint: /insert_from_s3
Request Method: POST
Request Body Type: Form Data

Required Parametes:
--- bucket_name: S3 Bucket Name
--- es_host: ES Host
--- access_key_id: Access Key ID you get from Amazon.
--- secret_access_key: Secrect Aceess Key you get from Amazon.

Returns:
--- inserted_files: List of inserted files.
```

### Get All Data


```
Endpoint: /get_all_result
Request Method: POST
Request Body Type: Form Data

Required Parametes:
--- es_host: ES Host.
--- index_name: The index name.


Returns:
---  data: The dataset in JSON form.
```


### Add Days from Today and Return Data:
```
Endpoint: /get_results_with_added_days
Request Method: POST
Request Body Type: Form Data

Required Parametes:
--- es_host: ES Host.
--- index_name: The index name.
--- days: Number of days to add to today.

Returns:
---  data: The dataset in JSON form.
```