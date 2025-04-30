import firebase_admin
from firebase_admin import credentials, firestore
import os

# Cargar la ruta del archivo desde la variable de entorno
firebase_key_path = os.getenv("FIREBASE_KEY_PATH")

# Inicializar Firebase
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)

# Crear cliente Firestore
db = firestore.client()

# Funciones de manejo de loadouts
def get_server_loadouts(server_id):
    return db.collection('loadouts').document(str(server_id)).collection('items')

def save_server_loadout(server_id, weapon_name, data):
    ref = db.collection('loadouts').document(str(server_id)).collection('items').document(weapon_name)
    ref.set(data)

def delete_server_loadout(server_id, weapon_name):
    ref = db.collection('loadouts').document(str(server_id)).collection('items').document(weapon_name)
    ref.delete()

def get_single_loadout(server_id, weapon_name):
    ref = db.collection('loadouts').document(str(server_id)).collection('items').document(weapon_name)
    return ref.get()

