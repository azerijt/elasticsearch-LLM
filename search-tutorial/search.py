import json
from pprint import pprint
import os
import time
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

ELASTIC_CLOUD_ID="chatbot:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQxZjJjNjY1OTZiYWE0ZDVkYmQzMDY4ODA4YzFkNmJmOSRjZmUzNzAzMzQ2YjY0YWE0YjFhY2U5NWQyMGFiMWQ3YQ=="
ELASTIC_API_KEY="N1gxcVNZd0JLVl9xTUcxejdBT3Y6YmZCcE9BalpUeGVyclhJcFpINHc3dw=="


class Search:
    def __init__(self):
        self.es = Elasticsearch(cloud_id=ELASTIC_CLOUD_ID,
                                api_key=ELASTIC_API_KEY)
        client_info = self.es.info()
        print('Connected to Elasticsearch!')
        pprint(client_info.body)