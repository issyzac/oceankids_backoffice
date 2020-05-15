from dataclasses import dataclass

@dataclass
class Child:
    first_name: str
    last_name: str
    gender: str = ""
    date_of_birth: str = ""
    firebase_id: str = ""
    allergies: str = ""
    checked_in: int = 0
    level = str = ""
    nationality: str = "Tanzania"
    
    #parents: List[ChildParent] = {[]}
