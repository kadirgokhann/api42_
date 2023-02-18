from src.api42.all_moduls import *
from dotenv import load_dotenv

d = os.path.dirname(os.path.realpath(__file__))+""
settings_path = d+"/../credentials/settings.json"
keys_path = d+"/../credentials/keys.json"
# load_dotenv()


def getPublicKey(campus_id: int):
    return json.load(open(keys_path, "r"))[f"_{str(campus_id)}_api_key"]


def getPrivateKey(campus_id: int):
    return json.load(open(keys_path, "r"))[f"_{str(campus_id)}_api_secret"]


def getToken(campus_id: int):
    return json.load(open(keys_path, "r"))[f"_{str(campus_id)}_token"]


def getTokenTime(campus_id: int):
    return json.load(open(keys_path, "r"))[f"_{str(campus_id)}_tokentime"]


def getUri():
    return json.load(open(settings_path, "r"))["uri"]


def getEndpoint():
    return json.load(open(settings_path, "r"))["endpoint"]
