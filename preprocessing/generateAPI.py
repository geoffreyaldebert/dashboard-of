import pandas as pd
import numpy as np
import json
import os
from tqdm import tqdm
import time

df = pd.read_csv('data.csv',sep=';',dtype=str)

df = df.replace({np.nan:None})

df = df.rename(columns={
    'numeroDeclarationActivite': 'num_decla',
    'numerosDeclarationActivitePrecedent': 'num_decla_precedent',
    'siretEtablissementDeclarant': 'siret',
    'certifications.actionsDeFormation': 'cert_action_formation',
    'certifications.bilansDeCompetences': 'cert_bilan_competence',
    'certifications.VAE': 'cert_vae',
    'certifications.actionsDeFormationParApprentissage': 'cert_action_formation_apprentissage',
    'informationsDeclarees.dateDerniereDeclaration': 'date_derniere_decla',
    'informationsDeclarees.debutExercice': 'debut_exercice',
    'informationsDeclarees.finExercice': 'fin_exercice',
    'informationsDeclarees.specialitesDeFormation.codeSpecialite1': 'code_specialite1',
    'informationsDeclarees.specialitesDeFormation.libelleSpecialite1': 'specialite1',
    'informationsDeclarees.specialitesDeFormation.codeSpecialite2': 'code_specialite2',
    'informationsDeclarees.specialitesDeFormation.libelleSpecialite2': 'specialite2',
    'informationsDeclarees.specialitesDeFormation.codeSpecialite3': 'code_specialite3',
    'informationsDeclarees.specialitesDeFormation.libelleSpecialite3': "specialite3",
    'informationsDeclarees.nbStagiaires': 'nb_stagiaires',
    'informationsDeclarees.nbStagiairesConfiesParUnAutreOF': 'nb_stagiaires_confies_of',
    'informationsDeclarees.effectifFormateurs': 'effectif_formateurs',
})

df = df.drop(columns=['Unnamed: 30', 'adressePhysiqueOrganismeFormation.voie', 'adressePhysiqueOrganismeFormation.codePostal', 'adressePhysiqueOrganismeFormation.ville', 'adressePhysiqueOrganismeFormation.codeRegion', 
    'organismeEtrangerRepresente.denomination',
    'organismeEtrangerRepresente.voie',
    'organismeEtrangerRepresente.codePostal',
    'organismeEtrangerRepresente.ville',
    'organismeEtrangerRepresente.pays'])

if not os.path.exists('siren'):
    os.makedirs('siren')

for i in tqdm(range(df['siren'].nunique())):
    siren = df['siren'].unique()[i]
    with open('siren/'+siren+'.json', 'w') as fp:
        json.dump(df[df['siren'] == df.iloc[0]['siren']].to_dict(orient="records"), fp)

