import yaml
import json 
import re
from search import Search

client = Search()

json_file_path = 'Elasticsearch/data.json'

def preprocess_text(text):
    text = text.lower()
    # Remove special characters and numbers
    return text

with open(json_file_path, "r") as f:
  file_contents = json.load(f)

operations = []
for item in file_contents:
  print('\n',item)
  index_action = {
    "index": {
      "_index": "search-jaazbot",
      "_id": item["name"]
  }
  }
  operations.extend([index_action, item])

bulk_response = client.perform_bulk_indexing(operations, pipeline="ent-search-generic-ingestion")

search_result = client.perform_search(index="search-jaazbot", query="foo")


print(search_result)
