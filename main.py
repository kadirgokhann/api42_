from src.api42 import API42
from src.api42.all_moduls import *

api = API42(49)
print(api.get_accreditations()[0].cursus_id)
response = api.request("get", "/v2/users/49")
