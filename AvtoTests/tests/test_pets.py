import requests

status = 'available'
res = requests.get(f"https://petstore.swagger.io/v2/pet/findByStatus?status={status}",
                   headers={'accept': 'application/json'})
if 'application/json' in res.headers['Content-Type']:
    res.json()
else:
    res.text
print(res.text)
