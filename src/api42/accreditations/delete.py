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


def delete_accreditations(self, id: int = None):
    """
    This action requires one of theses roles: Basic tutor, Basic staff
    Examples
    --------
    >>> api = API(49)
    >>> re = api.delete_accreditations(id=273)
    >>> print(re)
    204
    """
    _params = {"id": id}
    params = {}
    for k, v in _params.items():
        if v == None:
            continue
        params[k] = v
    #########################
    response = self.request("delete", "/v2/accreditations", params=params)
    ############################
    return response
