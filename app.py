from flask import Flask, render_template, request, redirect, url_for
import dictionnaire_global
import csv
import os
import folium

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



@app.route('/carte', methods=['GET', 'POST'])
def carte():
    if request.method == 'POST':
        # Récupérer la sélection de l'utilisateur
        entreprise = request.form.get('entreprise')
        # Création d'une carte centrée sur Calais
        m = folium.Map(location=[50.5271636,2.2342776], zoom_start=8)
        # Ajouter des marqueurs et un chemin en fonction de la sélection
        if entreprise == 'ow':
            folium.Marker([50.713732012728045, 1.6110945258837055], popup='Opale Web').add_to(m)
        elif entreprise == 'ccpo':
            folium.Marker([50.86636033821647, 1.8615185514152992], popup="Communauté de communes Pays d'opale").add_to(m)        
        elif entreprise == 'elp':
            folium.Marker([50.59322596797254, 2.4032327528607142], popup="Espace Learning Pro").add_to(m)        
        elif entreprise == 'air':
            folium.Marker([50.713273245714944, 1.5813148547195892], popup="Airspire").add_to(m)
        elif entreprise == 'atm':  
            folium.Marker([50.95501254810064, 1.915033539391012], popup="Atoucom").add_to(m)
        elif entreprise == 'dp':
            folium.Marker([50.94756364052157, 1.8556709240468794], popup="DocPro SARL").add_to(m)
        elif entreprise == 'ce':
            folium.Marker([50.951272479327585, 1.8573451663753346], popup="Opale CE").add_to(m)
        elif entreprise == 'bar':
            folium.Marker([50.87670391270745, 2.2500746120419253], popup="Théâtre La Barcarolle").add_to(m)
    
    if request.method == 'POST':
        # Récupérer la sélection de l'utilisateur
        etudiant = request.form.get('etudiant')
        # Création d'une carte centrée sur Calais
        m = folium.Map(location=[50.5271636,2.2342776], zoom_start=8)
        # Ajouter des marqueurs et un chemin en fonction de la sélection
        if etudiant == 'zoe':
            folium.Marker([50.713732012728045, 1.6110945258837055], popup='Zoe').add_to(m)
        elif etudiant == 'tom':
            folium.Marker([50.86636033821647, 1.8615185514152992], popup="Tom").add_to(m)        
        elif etudiant == 'juliette':
            folium.Marker([50.59322596797254, 2.4032327528607142], popup="Juliette").add_to(m)        
        elif etudiant == 'arthur':
            folium.Marker([50.713273245714944, 1.5813148547195892], popup="Arthur").add_to(m)
        elif etudiant == 'mathys':  
            folium.Marker([50.95501254810064, 1.915033539391012], popup="Mathys").add_to(m)
        elif etudiant == 'emilie':
            folium.Marker([50.94756364052157, 1.8556709240468794], popup="Emilie").add_to(m)
        elif etudiant == 'mario':
            folium.Marker([50.951272479327585, 1.8573451663753346], popup="Mario").add_to(m)
        elif etudiant == 'baptiste':
            folium.Marker([50.87670391270745, 2.2500746120419253], popup="Baptiste").add_to(m)




        m.save('static/carte.html')
    return render_template('carte.html')

if __name__ == '__main__':
    charger_suivi()
    app.run(debug=True)