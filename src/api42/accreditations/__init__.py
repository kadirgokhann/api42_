from src.api42.accreditations.get import get_accreditations
from src.api42.accreditations.put import put_accreditations
from src.api42.accreditations.post import post_accreditations
from src.api42.accreditations.delete import delete_accreditations


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
