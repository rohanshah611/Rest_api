import requests
base='http://127.0.0.1:5000/resources/tracks/all'
response = requests.get(base)
print(response.json())
