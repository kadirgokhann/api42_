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


def post_accreditations(self, name: str = None, user_id: int = None, cursus_id: int = None, validated: bool = None, difficulty: int = None, skill_id: int = None, value: int = None, destroy: str = None):
    """
    This action requires one of theses roles: Basic tutor, Basic staff
    Examples
    --------
    >>> api = API(49)
    >>> re = api.post_accredidations(id=273,name="test",user_id=21732,cursus_id=21,validated=False,difficulty=55555,skill_id=1,value=1)
    >>> print(re)
    201
    """
    _params = {"name": name, "user_id": user_id, "cursus_id": cursus_id,
               "validated": validated, "difficulty": difficulty, "skill_id": skill_id, "value": value, "destroy": destroy}
    params = {}
    for k, v in _params.items():
        if v == None:
            continue
        params[k] = v
    ############################
    response = self.request("post", "/v2/accreditations", params=params)
    ############################
    return [ACCREDITATIONS(**response.json)]
