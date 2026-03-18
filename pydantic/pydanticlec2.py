from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int 
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value

patient_info={
    'name': 'nitish',
    'age': 30,
    'email': 'abc@hdfc.com',
    'linkedin_url': 'http://linkedin.com/12345',
    'weight': 75.2,
    'married': False,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'email': 'abc@gmail.com',
        'phone': '2356462'
    }
}

patient1 = Patient(**patient_info)

def insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print('data inserted successfully')

insert(patient1)