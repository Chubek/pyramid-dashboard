from scripts.data.es import get_results
from dotenv import dotenv_values

temp = dotenv_values(".env")

def filter_product(product_name):
    return get_results(temp['INDEX_NAME'], "match", "Product", product_name)


def filter_customer_name(customer_name):
    return get_results(temp['INDEX_NAME'], "match", "Customer Name", customer_name)

def filter_customer_type(customer_type):
    return get_results(temp['INDEX_NAME'], "match", "Product", customer_type)

def filter_subtype_a(subtype_a):
    return get_results(temp['INDEX_NAME'], "match", "Sub Type A", subtype_a)

def filter_subtype_a(subtype_b):
    return get_results(temp['INDEX_NAME'], "match", "Sub Type A", subtype_b)