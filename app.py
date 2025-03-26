from flask import Flask, render_template, request, redirect, url_for
import dictionnaire_global

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
        promotion = request.form.get('promotion')
        entreprise = request.form.get('entreprise')

        dictionnaire_global.ajouter_etudiant(nom, prenom, promotion, entreprise)

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

if __name__ == '__main__':
    app.run(debug=True)