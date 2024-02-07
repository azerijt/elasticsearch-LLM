from elasticsearch import Elasticsearch
from pprint import pprint
import os
import time
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

ELASTIC_CLOUD_ID="My_deployment:ZXUtd2VzdC0yLmF3cy5jbG91ZC5lcy5pbyRjMDc3NTU4MmY1ZWE0MjI5OTQwOGQwYTM4YjYxOWQ1NCRlZWQ4OTcyMGJhMjI0ZmJmODhjNTQxY2U3NDMyODliNw=="
ELASTIC_API_KEY="Zzh1Y2ZvMEI5QUxrSk5oMm5jaVA6TE1wU3pnWEtUaHFYb3dhakc4V2RFUQ=="


class Search:
    def __init__(self):
        self.es = Elasticsearch(cloud_id=ELASTIC_CLOUD_ID,
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
