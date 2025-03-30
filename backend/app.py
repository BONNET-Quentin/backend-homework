import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 
@app.route('/')
def home():
    return "API du serveur marche !"

@app.route('/api/alive')
def alive():
    return jsonify({"message": "Alive"}), 200

@app.route('/api/associations', methods=['GET'])
def association_list():
    L = []
    for i in range(len(associations_df)):
        L.append(int(associations_df.loc[i, 'id']))
    return jsonify(L), 200

@app.route('/api/association/<int:id>', methods=['GET'])
def detail_association(id: int):
    if id not in associations_df['id'].values:
        return jsonify({"error": "Association not found"}), 404
    else:
        association = associations_df[associations_df['id'] == id].to_dict(orient='records')[0]
        return jsonify(association), 200

@app.route('/api/evenements', methods=['GET'])
def event_list():
    L = []
    for i in range(len(evenements_df)):
        L.append(int(evenements_df.loc[i, 'id']))
    return jsonify(L), 200

@app.route('/api/evenement/<int:id>', methods=['GET'])
def detail_event(id: int):
    if id not in evenements_df['id'].values:
        return jsonify({"error": "Event not found"}), 404
    else:
        event = evenements_df[evenements_df['id'] == id].to_dict(orient='records')[0]
        return jsonify(event), 200


if __name__ == '__main__':
    app.run(debug=False)
