import pandas as pd
import os

# Chemins des fichiers CSV
ENTREPRISES_CSV = 'entreprises.csv'
ETUDIANTS_CSV = 'etudiants.csv'

# Initialisation des dictionnaires
entreprises = {}
etudiants = {}

# Compteurs pour les IDs
entreprise_counter = 0
etudiant_counter = 0

def get_next_id(used_ids, max_id=255):
    """Trouver le prochain ID disponible entre 0 et max_id"""
    for i in range(max_id + 1):
        if str(i) not in used_ids:
            return i
    # Si tous les IDs sont pris, commencer à zéro et chercher le premier disponible
    return 0

# Charger les données existantes depuis les fichiers CSV
def charger_donnees():
    global entreprises, etudiants, entreprise_counter, etudiant_counter
    
    if os.path.exists(ENTREPRISES_CSV):
        try:
            df_entreprises = pd.read_csv(ENTREPRISES_CSV)
            entreprises = {}
            ids_used = set()
            
            # S'assurer que la colonne 'id' existe
            if 'id' not in df_entreprises.columns:
                df_entreprises['id'] = range(len(df_entreprises))
                df_entreprises.to_csv(ENTREPRISES_CSV, index=False)
            
            for index, row in df_entreprises.iterrows():
                if pd.notna(row['id']):
                    ids_used.add(str(int(row['id'])))
                
                entreprise_id = str(int(row['id']) if pd.notna(row['id']) else get_next_id(ids_used))
                if entreprise_id not in ids_used:
                    ids_used.add(entreprise_id)
                
                entreprises[entreprise_id] = {
                    'id': entreprise_id,
                    'nom': row['nom'],
                    'adresse': row['adresse'],
                    'email': row['email'],
                    'telephone': row['telephone']
                }
            
            entreprise_counter = get_next_id(ids_used)
        except Exception as e:
            print(f"Erreur lors du chargement des entreprises: {e}")
            entreprises = {}
    
    if os.path.exists(ETUDIANTS_CSV):
        try:
            df_etudiants = pd.read_csv(ETUDIANTS_CSV)
            etudiants = {}
            ids_used = set()
            
            # S'assurer que la colonne 'id' existe
            if 'id' not in df_etudiants.columns:
                df_etudiants['id'] = range(len(df_etudiants))
                df_etudiants.to_csv(ETUDIANTS_CSV, index=False)
            
            for index, row in df_etudiants.iterrows():
                if pd.notna(row['id']):
                    ids_used.add(str(int(row['id'])))
                
                etudiant_id = str(int(row['id']) if pd.notna(row['id']) else get_next_id(ids_used))
                if etudiant_id not in ids_used:
                    ids_used.add(etudiant_id)
                
                etudiant_info = {
                    'id': etudiant_id,
                    'nom': row['nom'],
                    'prenom': row['prenom'],
                    'address': row['address'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'promotion': row['promotion'],
                }
                etudiants[etudiant_id] = etudiant_info
            
            etudiant_counter = get_next_id(ids_used)
        except Exception as e:
            print(f"Erreur lors du chargement des étudiants: {e}")
            etudiants = {}

def ajouter_entreprise(nom, adresse, email, telephone):
    global entreprise_counter
    entreprise_id = str(entreprise_counter)
    entreprise_info = {
        'id': entreprise_id,
        'nom': nom,
        'adresse': adresse,
        'email': email,
        'telephone': telephone
    }
    entreprises[entreprise_id] = entreprise_info
    
    # Incrémenter le compteur et boucler si nécessaire
    entreprise_counter = (entreprise_counter + 1) % 256
    
    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(list(entreprises.values()))
    df.to_csv(ENTREPRISES_CSV, index=False)

def get_entreprises():
    return entreprises

# ///////////////////////////////////////////////////////////////////

def ajouter_etudiant(nom, prenom, address, email, phone, promotion):
    global etudiant_counter
    etudiant_id = str(etudiant_counter)
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
    
    # Incrémenter le compteur et boucler si nécessaire
    etudiant_counter = (etudiant_counter + 1) % 256
    
    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(list(etudiants.values()))
    df.to_csv(ETUDIANTS_CSV, index=False)

def get_etudiants():
    return etudiants

# Charger les données au démarrage du module
charger_donnees()