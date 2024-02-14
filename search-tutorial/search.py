import yaml
import json
from pprint import pprint
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
class Search:
    def __init__(self):
        self.es = Elasticsearch(cloud_id=os.getenv('ELASTIC_CLOUD_ID'),api_key=os.getenv('ELASTIC_API_KEY'))
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)
    
    def create_index(self):
        #if you need to add more indexes set index as an argument
        self.es.indices.delete(index='search-jaazbot', ignore_unavailable=True)
        self.es.indices.create(index='search-jaazbot')
    
    def insert_document(self, document):
        return self.es.index(index='search-jaazbot', body=document)

    def insert_documents(self, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': 'search-jaazbot'}})
            operations.append(document)
        return self.es.bulk(operations=operations)

    def reindex(self):
        self.create_index()
        with open('data.yaml', 'rt') as f:
            yaml_data = f.read()

            yaml_documents = list(yaml.safe_load_all(yaml_data))
        # json_documents = [json.dumps(doc).encode('utf-8') for doc in yaml_documents]
        return self.insert_documents(yaml_documents)

    # def reindex(self):
    #     self.create_index()
    #     with open('data.json', 'rt') as f:
    #         documents = json.loads(f.read())
    #     return self.insert_documents(documents)
    
    def search(self, **query_args):
        return self.es.search(index='search-jaazbot', **query_args)
    
    def retrieve_document(self, id):
        return self.es.get(index='search-jaazbot', id=id)
    




