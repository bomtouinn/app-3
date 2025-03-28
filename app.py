from flask import Flask, render_template, request, redirect, url_for, flash
import dictionnaire_global
import csv
import os
import folium

import uuid

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Changez cette clé pour sécuriser les sessions

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige les utilisateurs non connectés vers la page de connexion

# Exemple d'utilisateur (vous pouvez remplacer cela par une base de données)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Liste des utilisateurs (à remplacer par une base de données)
users = {
    "admin": User(id=1, username="admin", password="password123")
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route('/')
def index():
    entreprises = dictionnaire_global.get_entreprises()
    etudiants = dictionnaire_global.get_etudiants()
    # S'assurer que les données de suivi sont chargées
    charger_suivi()
    # Organiser les suivis par entreprise pour faciliter l'affichage
    suivis_par_entreprise = {}
    for suivi in suivi_data:
        entreprise = suivi['entreprise']
        if entreprise not in suivis_par_entreprise:
            suivis_par_entreprise[entreprise] = []
        suivis_par_entreprise[entreprise].append(suivi)
    
    return render_template('index.html', entreprises=entreprises, etudiants=etudiants, 
                          suivi_data=suivi_data, suivis_par_entreprise=suivis_par_entreprise)

@app.route('/entreprise', methods=['GET', 'POST'])
@login_required
def entreprise():
    if request.method == 'POST':
        nom = request.form.get('name')
        adresse = request.form.get('address')
        email = request.form.get('email')
        telephone = request.form.get('phone')

        dictionnaire_global.ajouter_entreprise(nom, adresse, email, telephone)

        return redirect(url_for('index'))

    return render_template('form_entreprise.html')

@app.route('/etudiant', methods=['GET', 'POST'])
@login_required
def etudiant():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        promotion = request.form.get('promotion')

        dictionnaire_global.ajouter_etudiant(
            nom, prenom, address, email, phone, promotion
        )

        return redirect(url_for('index'))

    return render_template('form_etudiant.html')

@app.route('/liste-entreprises')
def liste_entreprises():
    entreprises = dictionnaire_global.get_entreprises()
    return render_template('liste_entreprises.html', entreprises=entreprises)

@app.route('/liste-etudiants')
def liste_etudiants():
    etudiants = dictionnaire_global.get_etudiants()
    return render_template('liste_etudiants.html', etudiants=etudiants)

SUIVI_CSV = 'suivi.csv'
suivi_data = []

def charger_suivi():
    global suivi_data
    if os.path.exists(SUIVI_CSV):
        try:
            with open(SUIVI_CSV, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                suivi_data = []
                for row in reader:
                    # Add ID if it doesn't exist
                    if 'id' not in row:
                        row['id'] = str(uuid.uuid4())
                    suivi_data.append(row)
        except Exception as e:
            print(f"Erreur lors du chargement du suivi: {e}")
            suivi_data = []

def sauvegarder_suivi():
    with open(SUIVI_CSV, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'id', 'entreprise', 'etudiant', 'type_contrat', 'date_embauche', 'detail_missions'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Filtrer les données pour ne garder que les champs présents dans fieldnames
        filtered_data = []
        for entry in suivi_data:
            filtered_entry = {k: entry.get(k, '') for k in fieldnames}
            filtered_data.append(filtered_entry)
            
        writer.writerows(filtered_data)

@app.route('/suivi', methods=['GET', 'POST'])
@login_required
def suivi():
    if request.method == 'POST':
        entreprise = request.form.get('entreprise', '')
        etudiant = request.form.get('etudiant', '')
        type_contrat = request.form.get('type_contrat', '')
        date_embauche = request.form.get('date_embauche', '')
        detail_missions = request.form.get('detail_missions', '')

        # Ajouter une nouvelle entrée pour chaque suivi, même si l'entreprise est la même
        suivi_entry = {
            'id': str(uuid.uuid4()),
            'entreprise': entreprise,
            'etudiant': etudiant,
            'type_contrat': type_contrat,
            'date_embauche': date_embauche,
            'detail_missions': detail_missions
        }
        suivi_data.append(suivi_entry)

        sauvegarder_suivi()
        return redirect(url_for('liste_suivi'))

    entreprises = dictionnaire_global.get_entreprises()
    etudiants = dictionnaire_global.get_etudiants()
    return render_template('form_suivi.html', entreprises=entreprises, etudiants=etudiants)

@app.route('/liste-suivi')
def liste_suivi():
    return render_template('liste_suivi.html', suivi_data=suivi_data)

@app.route('/carte', methods=['GET', 'POST'])
def carte():
    # Création d'une carte centrée sur Calais par défaut
    m = folium.Map(location=[50.5271636, 2.2342776], zoom_start=8)
    
    # Définir les coordonnées des entreprises
    entreprises_coords = {
        'ow': {'nom': 'Opale Web', 'coords': [50.713732012728045, 1.6110945258837055]},
        'ccpo': {'nom': "Communauté de communes Pays d'opale", 'coords': [50.86636033821647, 1.8615185514152992]},
        'elp': {'nom': "Espace Learning Pro", 'coords': [50.59322596797254, 2.4032327528607142]},
        'air': {'nom': "Airspire", 'coords': [50.713273245714944, 1.5813148547195892]},
        'atm': {'nom': "Atoucom", 'coords': [50.95501254810064, 1.915033539391012]},
        'dp': {'nom': "DocPro SARL", 'coords': [50.94756364052157, 1.8556709240468794]},
        'ce': {'nom': "Opale CE", 'coords': [50.951272479327585, 1.8573451663753346]},
        'bar': {'nom': "Théâtre La Barcarolle", 'coords': [50.87670391270745, 2.2500746120419253]},
    }
    
    # Correspondance des codes d'entreprises avec les IDs dans la base de données
    # (à adapter selon votre système)
    entreprise_codes_to_ids = {
        'ow': '0',
        'ccpo': '1',
        'elp': '2',
        'air': '3',
        'atm': '4',
        'dp': '5',
        'ce': '6',
        'bar': '7',
    }
    
    # Récupérer les entreprises réelles
    entreprises_data = dictionnaire_global.get_entreprises()
    
    # Coordonnées connues pour certaines villes en France
    villes_coords = {
        'Calais': [50.9513, 1.8587],
        'Lille': [50.6292, 3.0573],
        'Dunkerque': [51.0343, 2.3768],
        'Saint-Quentin': [49.8466, 3.2873],
        '123 Main St': [50.7133, 1.6111],
        '456 Elm St': [50.8664, 1.8615],
        '789 Oak St': [50.5932, 2.4032],
        '101 Pine St': [50.7133, 1.5813],
        '202 Maple St': [50.9550, 1.9150],
    }
    
    # Chargement des données pour trouver les associations entre étudiants et entreprises
    charger_suivi()
    
    # Récupérer les données des étudiants
    etudiants_data = dictionnaire_global.get_etudiants()
    
    if request.method == 'POST':
        # Récupérer la sélection de l'entreprise
        entreprise_code = request.form.get('entreprise')
        
        # Debug - pour vérifier que les données sont bien chargées
        print(f"Entreprise sélectionnée: {entreprise_code}")
        print(f"Nombre d'étudiants chargés: {len(etudiants_data)}")
        print(f"Nombre de suivis chargés: {len(suivi_data)}")
        
        if entreprise_code in entreprises_coords:
            # Afficher le marqueur de l'entreprise sélectionnée
            entreprise_info = entreprises_coords[entreprise_code]
            folium.Marker(
                entreprise_info['coords'], 
                popup=entreprise_info['nom'],
                icon=folium.Icon(color='green', icon='building', prefix='fa')
            ).add_to(m)
            
            # Trouver les étudiants associés à cette entreprise
            etudiants_entreprise = []
            for suivi in suivi_data:
                # Debug pour vérifier les associations
                print(f"Suivi: entreprise={suivi['entreprise']}, etudiant={suivi['etudiant']}")
                
                # Vérifier si l'entreprise correspond à celle sélectionnée
                if suivi['entreprise'] == entreprise_code:
                    etudiants_entreprise.append(suivi['etudiant'])
            
            print(f"Étudiants trouvés dans cette entreprise: {etudiants_entreprise}")
            
            # Pour chaque étudiant associé à cette entreprise
            for etudiant_id in etudiants_entreprise:
                # Vérifier que l'ID de l'étudiant est dans les données
                if etudiant_id in etudiants_data:
                    etudiant = etudiants_data[etudiant_id]
                    adresse = etudiant.get('address', '')  # Utiliser get() pour éviter KeyError
                    nom_complet = f"{etudiant.get('prenom', '')} {etudiant.get('nom', '')}"
                    
                    print(f"Traitement de l'étudiant {etudiant_id}: {nom_complet}, adresse: {adresse}")
                    
                    # Si l'adresse est dans notre dictionnaire de coordonnées connues
                    if adresse and adresse in villes_coords:
                        coords = villes_coords[adresse]
                        print(f"Coordonnées trouvées pour {adresse}: {coords}")
                        folium.Marker(
                            coords, 
                            popup=f"{nom_complet}<br>{adresse}",
                            icon=folium.Icon(color='blue', icon='user', prefix='fa')
                        ).add_to(m)
                    elif adresse:  # Si l'adresse existe mais n'est pas dans notre dictionnaire
                        print(f"Adresse inconnue, utilisation des coordonnées par défaut")
                        folium.Marker(
                            [50.5272, 2.2343],  # Coordonnées par défaut
                            popup=f"{nom_complet}<br>{adresse} (position approximative)",
                            icon=folium.Icon(color='red', icon='question', prefix='fa')
                        ).add_to(m)
                    else:
                        print(f"Pas d'adresse pour cet étudiant")
                else:
                    print(f"Étudiant ID {etudiant_id} non trouvé dans la base de données")

        m.save('static/carte.html')
    
    # Récupérer les noms complets des entreprises pour l'affichage
    entreprises_liste = [(code, info['nom']) for code, info in entreprises_coords.items()]
    return render_template('carte.html', entreprises=entreprises_liste)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérification des identifiants
        user = next((u for u in users.values() if u.username == username), None)
        if user and user.password == password:
            login_user(user)
            flash('Connexion réussie.', 'success')
            return redirect(url_for('index'))
        elif user:
            flash('Mot de passe incorrect.', 'danger')
        else:
            flash('Nom d\'utilisateur introuvable.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))

USERS_CSV = 'users.csv'

def charger_utilisateurs():
    global users
    if os.path.exists(USERS_CSV):
        with open(USERS_CSV, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(id=int(row['id']), username=row['username'], password=row['password'])
                users[row['username']] = user

def sauvegarder_utilisateur(user):
    with open(USERS_CSV, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'username', 'password'])
        if file.tell() == 0:  # Si le fichier est vide, écrire l'en-tête
            writer.writeheader()
        writer.writerow({'id': user.id, 'username': user.username, 'password': user.password})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérifier si l'utilisateur existe déjà
        if username in users:
            flash('Nom d\'utilisateur déjà pris.', 'danger')
            return redirect(url_for('register'))

        # Créer un nouvel utilisateur
        new_id = max([user.id for user in users.values()] or [0]) + 1
        new_user = User(id=new_id, username=username, password=password)
        users[username] = new_user

        # Sauvegarder dans le fichier CSV
        sauvegarder_utilisateur(new_user)

        flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    context = ('local.crt', 'local.key')
    charger_utilisateurs()
    charger_suivi()

    app.run(debug=True, ssl_context=('cert.pem','key.pem'))
