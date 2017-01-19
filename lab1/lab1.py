import requests
print requests.__version__

response = requests.get("https://raw.githubusercontent.com/adamjford/cmput404w1lab/master/lab1.py")

print response.text
print response.status_code
