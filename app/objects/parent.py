from dataclasses import dataclass

@dataclass
class Parent:
    first_name: str
    last_name: str
    email: str
    address: str
    parent_id: str
    phone_number: str
    relationship_to_child: str