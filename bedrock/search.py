from elasticsearch import Elasticsearch
from pprint import pprint
import os
import time
from dotenv import load_dotenv
from elasticsearch import Elasticsearch


ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY=os.getenv("ELASTIC_API_KEY")

class Search:
    def __init__(self):
        self.es = Elasticsearch(cloud_id=ELASTIC_CLOUD_ID
,
                                api_key=ELASTIC_API_KEY)
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        print(client_info.body)

    def perform_bulk_indexing(self, data, pipeline):
    # Perform bulk indexing here using self.es
        response = self.es.bulk(operations=data, pipeline=pipeline)
        # Process the response if needed
        return response

    def perform_search(self, index, query):
        # Perform a search here using self.es
        result = self.es.search(index=index, q=query)
        # Process the search result if needed
        return result

        

client = Search()

print(client.perform_search(index="search-jaazbot", query="avios"))
