from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

def load_data():
    with open('doctor_appointment/patients.json', 'r') as f:
        data = json.load(f)
    return data

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