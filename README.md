# Projet de Data Visualisation
## _Germain Deffontaines M1APP-BDIA_

Lien vers les différents Dataset utilisés :
[![N|Solid](https://upload.wikimedia.org/wikipedia/fr/thumb/8/84/Data_gouv_fr_logo.svg/2560px-Data_gouv_fr_logo.svg.png)](https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres/)


### L'objectif du projet est de contruire un application streamlit et de la publier sur streamlitshare.

Lien vers l'application streamlit :
[![N|Solid](https://media-exp1.licdn.com/dms/image/C560BAQFI3jAiQutmSw/company-logo_200_200/0/1614704116029?e=2159024400&v=beta&t=lcQQMHkvNe92LtVs8YF6tVfHsM1dQVtQCn5oSTFZQhg)](https://share.streamlit.io/germain-d/projet_dataviz_valeurs_foncieres/main/Projet_DataViz_Germain_Deffontaines.py)
## Contraintes
- 2 internal streamlit plots : st.line or st.bar_chart AND st.map
- 4 different external plots (histograms, Bar, Scatter or Pie charts) integrated with your application from external librairies like matplotlib, seaborn, plotly or Altair
- 2 checkbox that interacts with your dataset
- A slider that interacts with one or multiple plots
- Cache usage : At minimum a cache for data loading and pre-processing, you can use the st.cache
- A decorator that logs in a file the time execution interval in seconds (30 seconds, 2 seconds, 0.01 seconds, ...) and the timestamp of the call ()


## Etapes 
- Visualisation des différentes colonnes des datasets
```sh
from pandas_profiling import ProfileReport
profile = ProfileReport(df, title="Pandas Profiling Report",minimal=True)
profile.to_file("pj_report.html")
```
https://github.com/Germain-D/Projet_DataViz_Valeurs_Foncieres/blob/48cf51f0f8a704a497c340b83a651518b52ab50e/pj_report3.html

- Nettoyages des données et créations de nouveaux datasets

```sh
import numpy as np
import pandas as pd


df = pd.read_csv('full_2017.csv')
dfpropre = df.dropna(axis='columns',thresh=len(df)/1.2)
dfpropre = dfpropre.drop('nombre_lots',axis=1)
dfpropre = dfpropre.drop('code_departement',axis=1)
dfpropre = dfpropre.drop('numero_disposition',axis=1)
dfpropre = dfpropre.drop('adresse_code_voie',axis=1)
#On supprime les valeurs aberrantes
#On calcule Q1
q1=dfpropre["valeur_fonciere"].quantile(q=0.25)
#On calcule Q3
q3=dfpropre["valeur_fonciere"].quantile(q=0.75)
#On calcule l'écart interquartile (IQR)
IQR=q3-q1
#On calcule la borne inférieure à l'aide du Q1 et de l'écart interquartile
borne_inf = 20000
print(borne_inf)
#On calcule la borne supérieure à l'aide du Q3 et de l'écart interquartile
borne_sup = q3 +1.5*IQR
print(borne_sup)
#On garde les valeurs à l'intérieur de la borne inférieure et supérieure
dfpropre= dfpropre[dfpropre["valeur_fonciere"]<borne_sup]
dfpropre=dfpropre[dfpropre["valeur_fonciere"]>borne_inf]
#On sélectionne une partie représentative du dataset
dfpropre = dfpropre.sample(frac = 0.5)
#On créé un nouveau fichier csv
compression_opts = dict(method='zip', archive_name='2017new.csv')  
dfpropre.to_csv('2017.zip', index=False, compression=compression_opts)
```

- Tests de différents graphs en python
```sh
#Histogramme
dfpropre.hist(column='valeur_fonciere')
#Camembert
plt.pie(dfpropre['nature_mutation'].value_counts(), labels=['Vente',"Vente en l'état futur d'achèvement","Echange","Vente terrain à bâtir","Adjudication","Expropriation"])
```

- Passage au développement de l'application streamlit


