from flask import Flask, render_template, request, redirect, url_for, flash
import dictionnaire_global
import csv
import os

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
    return render_template('index.html', entreprises=entreprises, etudiants=etudiants, suivi_data=suivi_data)

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