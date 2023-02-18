from src.api42 import API42

api = API42(49)
print(api.get_accreditations(id=278)[0].cursus_id)
