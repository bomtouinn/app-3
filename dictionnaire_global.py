import pandas as pd
import os

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
            entreprises = df_entreprises.set_index('nom').to_dict('index')
        except:
            entreprises = {}
    
    if os.path.exists(ETUDIANTS_CSV):
        try:
            df_etudiants = pd.read_csv(ETUDIANTS_CSV)
            etudiants = df_etudiants.set_index('nom').to_dict('index')
        except:
            etudiants = {}

def ajouter_entreprise(nom, adresse, email, telephone):
    entreprise_info = {
        'nom': nom,
        'adresse': adresse,
        'email': email,
        'telephone': telephone
    }
    entreprises[nom] = entreprise_info
    
    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(list(entreprises.values()))
    df.to_csv(ENTREPRISES_CSV, index=False)

def get_entreprises():
    return entreprises

# ///////////////////////////////////////////////////////////////////

def ajouter_etudiant(nom, prenom, promotion, entreprise):
    etudiant_info = {
        'nom': nom,
        'prenom': prenom,
        'promotion': promotion,
        'entreprise': entreprise
    }
    etudiants[nom] = etudiant_info
    
    # Sauvegarde dans le fichier CSV
    df = pd.DataFrame(list(etudiants.values()))
    df.to_csv(ETUDIANTS_CSV, index=False)

def get_etudiants():
    return etudiants

# Charger les données au démarrage du module
charger_donnees()