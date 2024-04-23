import requests

# Test Walmart search
response = requests.post("http://localhost:8000/search", json={"name": "Sony XR85X93L 85 4K Mini LED Smart Google TV with PS5 Features (2023)", "website": "walmart"})
print("Walmart search response:")
print(response.json())

# Test Newegg search
response = requests.post("http://localhost:8000/search", json={"name": "Sony XR85X93L 85 4K Mini LED Smart Google TV with PS5 Features (2023)", "website": "newegg"})
print("Newegg search response:")
print(response.json())