from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='Id of the patient', examples=['POO1'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='city where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi 
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else :
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

app = FastAPI()

def load_data():
    with open('doctor_appointment/patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)

@app.get('/')
def index():
    return {
        'message': 'Doctor appointment is running'
    }

@app.get('/view')
def display_data():
    data = load_data()
    return data

@app.get('/patients/{patient_id}')
def view_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patient(sort_by: str, order: str):
    if sort_by not in ['height', 'weight', 'bmi']:
        raise HTTPException(status_code=400, detail='sort_by not in [height, weight, bmi]')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='order not in asc and desc')
    data = load_data()
    sorted_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sorted_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patients already exists')
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    