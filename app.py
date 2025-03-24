from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entreprise', methods=['GET', 'POST'])
def entreprise():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('form_entreprise.html')

@app.route('/etudiant', methods=['GET', 'POST'])
def etudiant():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('etudiant_form.html')

if __name__ == '__main__':
    app.run(debug=True)