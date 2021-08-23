from scripts.data.es import get_results
from dotenv import dotenv_values

temp = dotenv_values(".env")

def filter_product(index_name, product_name):
    return get_results(index_name, "match", "Product", product_name)


def filter_customer_name(index_name, customer_name):
    return get_results(index_name, "match", "Customer Name", customer_name)

def filter_customer_type(index_name, customer_type):
    return get_results(index_name, "match", "Product", customer_type)

def filter_subtype_a(index_name, subtype_a):
    return get_results(index_name, "match", "Sub Type A", subtype_a)

def filter_subtype_a(index_name, subtype_b):
    return get_results(index_name, "match", "Sub Type A", subtype_b)