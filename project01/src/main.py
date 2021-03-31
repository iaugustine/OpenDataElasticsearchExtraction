import time
import requests
import argparse
import json
import pandas as pd

from os import environ
from sodapy import Socrata
from datetime import datetime
from elasticsearch import Elasticsearch, helpers



DATASET_ID = environ['DATASET_ID']
USERNAME = environ['ES_USERNAME']
PASSWORD = environ['ES_PASSWORD']
APP_TOKEN = environ['APP_TOKEN'] 
HOST = environ['ES_HOST'] 


parser = argparse.ArgumentParser(description='Process data from OpenDataNYC')
parser.add_argument('--page_size', help='Enter the number of records per page', type=int, required=True)
parser.add_argument('--num_pages', help='Enter the number of pages to fetch', type=int)
args = parser.parse_args()


JSON = {
    "settings": 
    {
        "index.mapping.ignore_malformed": True   
    },
    "mappings":
    {
        "properties":{
            "issue_date": { "type":   "date", "format": "yyyy-MM-dd'T'HH:mm:ss", "null_value": "2021-06-30T00:00:00" },  

            "precinct" : { "type": "scaled_float", "scaling_factor": 10},
            "fine_amount" : { "type": "scaled_float", "scaling_factor": 10},
            "penalty_amount" : { "type": "scaled_float", "scaling_factor": 10},
            "interest_amount" : { "type": "scaled_float", "scaling_factor": 10},
            "reduction_amount" : { "type": "scaled_float", "scaling_factor": 10},
            "payment_amount" : { "type": "scaled_float", "scaling_factor": 10},
            "amount_due" : { "type": "scaled_float", "scaling_factor": 10}
        }
    }
}


def doc_generator(df, index_name):
    x = df.iterrows()
    for index, document in x:
        yield {
                "_index": index_name,
                "_type": "_doc",
                "_source": document.to_dict(),
            }

if __name__ == "__main__":
    
    print(DATASET_ID)
    print(args.page_size)
    print(args.num_pages)
    
    client = Socrata(
        "data.cityofnewyork.us",
        APP_TOKEN,
    )
    client.timeout = 200
    count = client.get(DATASET_ID, select = 'COUNT(*)')
    #requested = args.num_pages * args.page_size
    
    # if requested > count:
    #     print('Requested records are more than the total count of available records. Please re-launch application and enter other values')
    # else:
    try:
        es = Elasticsearch(
            [HOST],
            http_auth =(USERNAME, PASSWORD),
            http_compress=True
        ) 
        print(es.info())
    except Exception as e:
        print('Unable to connect to elasticsearch due to : ', e)
        
    
    index_name = "my-index-1"
    
    try:
        response = es.indices.create(index=index_name, body=JSON, request_timeout=100)
        print(response)
    except Exception as e:
        print('Index already exists. Message: \t', e)
    
    offset = 0
    print('Starting data extraction...')
    
    
    for i in range(args.num_pages):
        print("Loading page number: \t", i+1)
        try:
            data = client.get(DATASET_ID, limit = args.page_size, offset = offset, order=":id")
            offset = args.page_size + offset
        except Exception as e:
            print(e)
            continue
        
        
        # Preprocess data:
        data = pd.DataFrame.from_records(data)
        data['issue_date'] = pd.to_datetime(data['issue_date'], errors = 'coerce')
        data.dropna(axis = 0, inplace = True, subset = ['issue_date'] )
        data = data.where(pd.notnull(data), None)
        try:
            for success, info in helpers.parallel_bulk(es, doc_generator(data, index_name), request_timeout=150, thread_count = 20):
                if not success:
                    print('A document failed:', info) 
                
            print('Loaded page number: ', i+1)
        
        except Exception as e:
            print(e)
        time.sleep(3)
        
        #del data
            
    print(offset, 'records loaded. Phew!')
