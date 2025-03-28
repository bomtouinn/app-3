from flask import Flask, render_template, request, redirect, url_for
import dictionnaire_global
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entreprise', methods=['GET', 'POST'])
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
def etudiant():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        address = request.form.get('address')
        email = request.form.get('email')
        phone = request.form.get('phone')
        promotion = request.form.get('promotion')
        entreprise = request.form.get('entreprise')
        date_debut = request.form.get('date_debut')
        date_fin = request.form.get('date_fin')

        dictionnaire_global.ajouter_etudiant(
            nom, prenom, address, email, phone, promotion, entreprise, date_debut, date_fin
        )

        return redirect(url_for('index'))

    # Récupérer la liste des entreprises pour le formulaire
    entreprises = dictionnaire_global.get_entreprises()
    return render_template('form_etudiant.html', entreprises=entreprises)

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
        with open(SUIVI_CSV, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            suivi_data = list(reader)

def sauvegarder_suivi():
    with open(SUIVI_CSV, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'entreprise', 'etudiant', 'type_contrat', 'date_embauche', 'detail_missions'
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
def suivi():
    if request.method == 'POST':
        entreprise = request.form.get('entreprise', '')
        etudiant = request.form.get('etudiant', '')
        type_contrat = request.form.get('type_contrat', '')
        date_embauche = request.form.get('date_embauche', '')
        detail_missions = request.form.get('detail_missions', '')

        suivi_entry = {
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

if __name__ == '__main__':
    charger_suivi()
    app.run(debug=True)