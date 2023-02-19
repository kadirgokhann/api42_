from src.api42.all_moduls import *


class ACCREDITATIONS():
    def __init__(self,
                 cursus_id: int = "xox",
                 difficulty: int = "xox",
                 id: int = "xox",
                 name: str = "xox",
                 user_id: int = "xox",
                 validated: bool = "xox"):
        self.cursus_id: int = cursus_id
        self.difficulty: int = difficulty
        self.id: int = id
        self.name: str = name
        self.user_id: int = user_id
        self.validated: bool = validated


def get_accreditations(self, id: int = None, name: str = None, user_id: int = None, cursus_id: int = None, difficulty: int = None, validated: bool = None, created_at: "2022-01-03T06:42:00.000Z" = None, updated_at: "2022-01-03T06:42:00.000Z" = None,
                       sort: "user_id,-id" = None, range: "created_at=min,max" = None) -> List[ACCREDITATIONS]:
    """
    Examples
    --------
    >>> >> api =API(49)
    >>> >> name = api.get_accreditations(id=2)[0].name
    >>> >> s=api.get_accreditations(sırt="user_id")
    [
        ACCREDITATIONS(cursus_id=1, difficulty=1, id=2, name="Piscine C", user_id=1, validated=True),
        ACCREDITATIONS(cursus_id=1, difficulty=1, id=3, name="Piscine C", user_id=1, validated=True),
        ...
    ]
    >>> >> s[0].cursus_id
    1
    >>> >> api.get_accreditations(range="created_at=2022-01-03T06:42:00.000Z,2022-05-03T06:42:00.000Z")
    """
    key, value = None, None
    if range != None:
        key, value = self._range_to_kv(range)
        if value == None:
            raise Exception("get_accreditations:"+key)
    _params = {"filter[id]": id, "filter[name]": name, "filter[user_id]": user_id, "filter[cursus_id]": cursus_id,
               "filter[difficulty]": difficulty, "filter[validated]": validated, "filter[created_at]": created_at, "filter[updated_at]": updated_at, "sort": sort, f"range[{key}]": value}
    params = {}
    for k, v in _params.items():
        if v == None:
            continue
        params[k] = v
    #########################
    response = []
    all_response = self.request("get", "/v2/accreditations", params=params)
    ############################
    for i in all_response.json:
        response.append(ACCREDITATIONS(**i))
    return response
