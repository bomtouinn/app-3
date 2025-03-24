entreprises = {}

def ajouter_entreprise(nom, adresse, email, telephone):
    entreprise_info = {
        'nom': nom,
        'adresse': adresse,
        'email': email,
        'telephone': telephone
    }
    entreprises[nom] = entreprise_info

def get_entreprises():
    return entreprises

# ///////////////////////////////////////////////////////////////////

etudiants = {}

def ajouter_etudiant(nom, prenom, promotion, entreprise):
    etudiant_info = {
        'nom': nom,
        'prenom': prenom,
        'promotion': promotion,
        'entreprise': entreprise
    }
    etudiants[nom] = etudiant_info

def get_etudiants():
    return etudiants