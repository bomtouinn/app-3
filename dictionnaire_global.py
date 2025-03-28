import pandas as pd
import os
import uuid

# Chemins des fichiers CSV
ENTREPRISES_CSV = 'entreprises.csv'
ETUDIANTS_CSV = 'etudiants.csv'

# Initialisation des dictionnaires
entreprises = {}
etudiants = {}

# Charger les données existantes depuis les fichiers CSV
def charger_donnees():
    global entreprises, etudiants
    
    if os.path.exists(ENTREPRISES_CSV):
        try:
            df_entreprises = pd.read_csv(ENTREPRISES_CSV)
            entreprises = {}
            for index, row in df_entreprises.iterrows():
                # Use existing id or generate a new one
                entreprise_id = row['id'] if 'id' in row else str(uuid.uuid4())
                nom = row['nom']
                entreprises[entreprise_id] = {
                    'id': entreprise_id,
                    'nom': nom,
                    'adresse': row['adresse'],
                    'email': row['email'],
                    'telephone': row['telephone']
                }
        except Exception as e:
            print(f"Erreur lors du chargement des entreprises: {e}")
            entreprises = {}
    
    if os.path.exists(ETUDIANTS_CSV):
        try:
            df_etudiants = pd.read_csv(ETUDIANTS_CSV)
            etudiants = {}
            for index, row in df_etudiants.iterrows():
                # Use existing id or generate a new one
                etudiant_id = row['id'] if 'id' in row else str(uuid.uuid4())
                nom = row['nom']
                etudiant_info = {
                    'id': etudiant_id,
                    'nom': nom,
                    'prenom': row['prenom'],
                    'address': row['address'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'promotion': row['promotion'],
                }
                etudiants[etudiant_id] = etudiant_info
        except Exception as e:
            print(f"Erreur lors du chargement des étudiants: {e}")
            etudiants = {}

def ajouter_entreprise(nom, adresse, email, telephone):
    entreprise_id = str(uuid.uuid4())
    entreprise_info = {
        'id': entreprise_id,
        'nom': nom,
        'adresse': adresse,
        'email': email,
        'telephone': telephone
    }
    entreprises[entreprise_id] = entreprise_info
    
    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(list(entreprises.values()))
    df.to_csv(ENTREPRISES_CSV, index=False)

def get_entreprises():
    return entreprises

# ///////////////////////////////////////////////////////////////////

def ajouter_etudiant(nom, prenom, address, email, phone, promotion):
    etudiant_id = str(uuid.uuid4())
    etudiant_info = {
        'id': etudiant_id,
        'nom': nom,
        'prenom': prenom,
        'address': address,
        'email': email,
        'phone': phone,
        'promotion': promotion
    }
    etudiants[etudiant_id] = etudiant_info
    
    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(list(etudiants.values()))
    df.to_csv(ETUDIANTS_CSV, index=False)

def get_etudiants():
    return etudiants

# Charger les données au démarrage du module
charger_donnees()