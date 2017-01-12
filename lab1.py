import requests
print requests.__version__

response = requests.get("http://google.com/")

print response.text
print response.status_code
