from src.api42 import API42
from src.api42.all_moduls import *

api = API42(49)
print(api.get_accreditations(range="created_at=2022-10-03T06:42:00.000Z,2023-01-03T06:42:00.000Z")[0].cursus_id)

# How to request simply
response = api.request("get", "/v2/users/49", params={"filter[login]": "kgokhan"})
print(response)
print("\n\n\n\n")
print(response.json)
print("\n\n\n\n")
# print(response.headers)
print(response.status_code)
print("\n\n\n\n")
print(response.text)
print("\n\n\n\n")

print("\n\n\n\n")
print(response.content)
