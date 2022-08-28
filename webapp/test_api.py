import requests

BASE = "http://127.0.0.1:5000/"
response = requests.get(
    BASE + "api/get",
    {
        "first_name": "Adam",
        "last_name": "Walkiewicz",
        "year": 1925,
        "age": 30,
        "sex": "M",
        "occupation": "AUthoR",
    },
)

print(response.text)
print(response.headers)
