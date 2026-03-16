from pydantic import BaseModel
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int 
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

patient_info={
    'name': 'nitish',
    'age': 30
}

patient1 = Patient(**patient_info)

def insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('data inserted successfullt')

insert(patient1)