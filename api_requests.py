import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_all_formations():
    try:
        url = f'{BASE_URL}/formations/' 
        # url = '#' 
        data = {}
        
        headers = {'Content-Type': 'application/json'}
        
        response = requests.get(url, headers=headers)   
        
        formations = response.json()
        formations    
    except Exception as e:
        print(e)
        
    return formations

def add_formations(
    libelle,
    description,
    status,
    formateurID,
):
    try:
        url = f'{BASE_URL}/formations/' 
        # url = '#' 
        data = {
            "libelle": libelle,
            "description": description,
            "status": status,
            "formateurID": formateurID,
            "imageUrl": None
        }
        print(data)
        data = json.dumps(data)
        print(data)
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(url, data=data, headers=headers)   
        
        formations = response.json()    
        return formations
    except Exception as e:
        print(e)
        
