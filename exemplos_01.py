import requests

url = 'https://jsonplaceholder.typicode.com/posts/1'

resposta = requests.get(url)
data = resposta.json()

print(data)