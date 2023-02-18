from src.api42 import API42
from src.api42.all_moduls import *

api = API42(49)
print(api.get_accreditations(id=278)[0].cursus_id)
