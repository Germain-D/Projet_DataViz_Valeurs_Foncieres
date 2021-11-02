import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from functools import wraps
import logging
import time
import datetime

logger = logging.getLogger(__name__)

logger.setLevel("INFO")
handler = logging.FileHandler(filename="log.txt", mode="a")
log_format = "%(asctime)s %(levelname)s -- %(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.info('\nNew Execution at :', time.time(), "\n")

def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper




#Fonctions :

@st.cache(allow_output_mutation=True)
def loadDF2017():
    path = "./Ressourcescsv/2017new.csv"
    df = pd.read_csv(path, delimiter = ',')
    return df

@st.cache(allow_output_mutation=True)
def loadDF2018():
    path = "./Ressourcescsv/2018new.csv"
    df = pd.read_csv(path, delimiter = ',')
    return df

@st.cache(allow_output_mutation=True)
def loadDF2019():
    path = "./Ressourcescsv/2019new.csv"
    df = pd.read_csv(path, delimiter = ',')
    return df

@st.cache(allow_output_mutation=True)
def loadDF2020():
    path = "./Ressourcescsv/2020new.csv"
    df = pd.read_csv(path, delimiter = ',')
    return df

@st.cache(allow_output_mutation=True)
def loadDFglob(df17,df18,df19,df20):  
    dfglob = pd.concat([df17,df18,df19,df20])
    return dfglob

@st.cache(allow_output_mutation=True)
def dflalon(df):
    dflalon = df[['latitude','longitude']]
    return dflalon

@st.cache(allow_output_mutation=True)
def date(dfglob):
    dfDate = dfglob[['date_mutation','valeur_fonciere']]
    dfDate['date_mutation'] = pd.to_datetime(dfDate['date_mutation'])
    dfDate = dfDate.groupby(pd.Grouper(key='date_mutation',freq = 'D')).mean()
    return dfDate

#Première option: Données globales (2017 + 2018 + 2019 + 2020)
@timed
def opt1(mybar,percent_complete,dfglob):

    
    #Camembert de la nature des mutations:
    st.header('Nature des mutations:')
    labels=['Vente',"Vente en l'état futur d'achèvement","Echange","Vente terrain à bâtir","Adjudication","Expropriation"]
    values = dfglob['nature_mutation'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Choix de la région de la carte à afficher   
    option = st.selectbox(' Quelle carte voulez vous afficher ?', ('France Métropolitaine', 'Martinique', 'Île de la Réunion' ))
    if option == ('France Métropolitaine') :
      
        #Affichage de la carte
        fig = px.density_mapbox(dflalon(dfglob), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.52, lon=2.19), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig)

    if option == 'Martinique':

        #Affichage de la carte
        fig2 = px.density_mapbox(dflalon(dfglob), lat='latitude', lon='longitude', radius=1,center=dict(lat=16, lon=-61), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig2)    

    if option == ('Île de la Réunion'):

        #Affichage de la carte
        fig3 = px.density_mapbox(dflalon(dfglob), lat='latitude', lon='longitude', radius=1,center=dict(lat=-21.1, lon=55.3), zoom=7,mapbox_style="stamen-terrain")
        st.plotly_chart(fig3)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage des latitudes/longitudes max/min 
    col5,col6,col7,col8 = st.columns(4)
    col5.metric('Latitude Maximum',str(round(dflalon(dfglob)['latitude'].max(), 2))+'°')
    col6.metric('Longitude Maximum',str(round(dflalon(dfglob)['longitude'].max(), 2))+'°')
    col7.metric('Latitude Minimum',str(round(dflalon(dfglob)['latitude'].min(), 2))+'°')
    col8.metric('Longitude Minimum',str(round(dflalon(dfglob)['longitude'].min(), 2))+'°')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Histogramme de la fréquence des différentes valeurs foncières
    x = dfglob['valeur_fonciere']
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)],)
    fig.update_layout(title_text="Fréquence des différentes valeurs foncières",title_font_size=20)
    st.plotly_chart(fig)
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage du prix moyen des valeurs foncières et équivalence en lingots d'or
    ling1,ling2 = st.columns(2)
    ling1.metric('Prix Moyen',str(round(dfglob['valeur_fonciere'].mean(), 2))+' €')
    ling1.metric("Soit l'équivalent de: ",str(round(dfglob['valeur_fonciere'].mean()/50000, 2)) + "Lingots d'or")
    image = Image.open('lingot.png')
    ling2.image(image, use_column_width='auto')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #TOP 5 des communes les plus représentées
    n = st.slider('Nombre de communes :', 1, 30,5)
    st.header('TOP '+str(n)+ ' des communes les plus représentées')
    values = dfglob['nom_commune'].value_counts().head(n)
    st.bar_chart(values)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Moyenne des sommes dépensées par jours
    st.header('Moyenne des sommes dépensées par jours')
    st.write(date(dfglob).head())
    st.line_chart(date(dfglob))

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

#Deuxième option: Données de l'année 2020
@timed
def opt2(mybar,percent_complete,df20):

    #Camembert de la nature des mutations:
    st.header('Nature des mutations:')
    labels=['Vente',"Vente en l'état futur d'achèvement","Echange","Vente terrain à bâtir","Adjudication","Expropriation"]
    values = df20['nature_mutation'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Choix de la région de la carte à afficher   
    option = st.selectbox(' Quelle carte voulez vous afficher ?', ('France Métropolitaine', 'Martinique', 'Île de la Réunion' ))
    if option == ('France Métropolitaine') :
      
        #Affichage de la carte
        fig = px.density_mapbox(dflalon(df20), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.52, lon=2.19), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig)

    if option == 'Martinique':

        #Affichage de la carte
        fig2 = px.density_mapbox(dflalon(df20), lat='latitude', lon='longitude', radius=1,center=dict(lat=16, lon=-61), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig2)    

    if option == ('Île de la Réunion'):

        #Affichage de la carte
        fig3 = px.density_mapbox(dflalon(df20), lat='latitude', lon='longitude', radius=1,center=dict(lat=-21.1, lon=55.3), zoom=7,mapbox_style="stamen-terrain")
        st.plotly_chart(fig3)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage des latitudes/longitudes max/min 
    col5,col6,col7,col8 = st.columns(4)
    col5.metric('Latitude Maximum',str(round(dflalon(df20)['latitude'].max(), 2))+'°')
    col6.metric('Longitude Maximum',str(round(dflalon(df20)['longitude'].max(), 2))+'°')
    col7.metric('Latitude Minimum',str(round(dflalon(df20)['latitude'].min(), 2))+'°')
    col8.metric('Longitude Minimum',str(round(dflalon(df20)['longitude'].min(), 2))+'°')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Histogramme de la fréquence des différentes valeurs foncières
    x = df20['valeur_fonciere']
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
    fig.update_layout(title_text="Fréquence des différentes valeurs foncières",title_font_size=20)
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage du prix moyen des valeurs foncières et équivalence en lingots d'or
    ling1,ling2 = st.columns(2)
    ling1.metric('Prix Moyen',str(round(df20['valeur_fonciere'].mean(), 2))+' €')
    ling1.metric("Soit l'équivalent de: ",str(round(df20['valeur_fonciere'].mean()/50000, 2)) + "Lingots d'or")
    image = Image.open('lingot.png')
    ling2.image(image, use_column_width='auto')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #TOP 5 des communes les plus représentées
    n = st.slider('Nombre de communes :', 1, 30,5)
    st.header('TOP '+str(n)+ ' des communes les plus représentées')
    values = df20['nom_commune'].value_counts().head()
    st.bar_chart(values)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Moyenne des sommes dépensées par jours
    st.header('Moyenne des sommes dépensées par jours')
    st.area_chart(date(df20))

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

#Troisème option: Données de l'année 2019
@timed
def opt3(mybar,percent_complete,df19):

    #Camembert de la nature des mutations:
    st.header('Nature des mutations:')
    labels=['Vente',"Vente en l'état futur d'achèvement","Echange","Vente terrain à bâtir","Adjudication","Expropriation"]
    values = df19['nature_mutation'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Choix de la région de la carte à afficher   
    option = st.selectbox(' Quelle carte voulez vous afficher ?', ('France Métropolitaine', 'Martinique', 'Île de la Réunion' ))
    if option == ('France Métropolitaine') :
      
        #Affichage de la carte
        fig = px.density_mapbox(dflalon(df19), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.52, lon=2.19), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig)

    if option == 'Martinique':

        #Affichage de la carte
        fig2 = px.density_mapbox(dflalon(df19), lat='latitude', lon='longitude', radius=1,center=dict(lat=16, lon=-61), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig2)    

    if option == ('Île de la Réunion'):

        #Affichage de la carte
        fig3 = px.density_mapbox(dflalon(df19), lat='latitude', lon='longitude', radius=1,center=dict(lat=-21.1, lon=55.3), zoom=7,mapbox_style="stamen-terrain")
        st.plotly_chart(fig3)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage des latitudes/longitudes max/min 
    col5,col6,col7,col8 = st.columns(4)
    col5.metric('Latitude Maximum',str(round(dflalon(df19)['latitude'].max(), 2))+'°')
    col6.metric('Longitude Maximum',str(round(dflalon(df19)['longitude'].max(), 2))+'°')
    col7.metric('Latitude Minimum',str(round(dflalon(df19)['latitude'].min(), 2))+'°')
    col8.metric('Longitude Minimum',str(round(dflalon(df19)['longitude'].min(), 2))+'°')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Histogramme de la fréquence des différentes valeurs foncières
    x = df19['valeur_fonciere']
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
    fig.update_layout(title_text="Fréquence des différentes valeurs foncières",title_font_size=20)
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage du prix moyen des valeurs foncières et équivalence en lingots d'or
    ling1,ling2 = st.columns(2)
    ling1.metric('Prix Moyen',str(round(df19['valeur_fonciere'].mean(), 2))+' €')
    ling1.metric("Soit l'équivalent de: ",str(round(df19['valeur_fonciere'].mean()/50000, 2)) + "Lingots d'or")
    image = Image.open('lingot.png')
    ling2.image(image, use_column_width='auto')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #TOP 5 des communes les plus représentées
    n = st.slider('Nombre de communes :', 1, 30,5)
    st.header('TOP '+str(n)+ ' des communes les plus représentées')
    values = df19['nom_commune'].value_counts().head()
    st.bar_chart(values)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Moyenne des sommes dépensées par jours
    st.header('Moyenne des sommes dépensées par jours')
    st.area_chart(date(df19))

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

#Quatrième option: Données de l'année 2018
@timed
def opt4(mybar,percent_complete,df18):

    #Camembert de la nature des mutations:
    st.header('Nature des mutations:')
    labels=['Vente',"Vente en l'état futur d'achèvement","Echange","Vente terrain à bâtir","Adjudication","Expropriation"]
    values = df18['nature_mutation'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Choix de la région de la carte à afficher   
    option = st.selectbox(' Quelle carte voulez vous afficher ?', ('France Métropolitaine', 'Martinique', 'Île de la Réunion' ))
    if option == ('France Métropolitaine') :
      
        #Affichage de la carte
        fig = px.density_mapbox(dflalon(df18), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.52, lon=2.19), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig)

    if option == 'Martinique':

        #Affichage de la carte
        fig2 = px.density_mapbox(dflalon(df18), lat='latitude', lon='longitude', radius=1,center=dict(lat=16, lon=-61), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig2)    

    if option == ('Île de la Réunion'):

        #Affichage de la carte
        fig3 = px.density_mapbox(dflalon(df18), lat='latitude', lon='longitude', radius=1,center=dict(lat=-21.1, lon=55.3), zoom=7,mapbox_style="stamen-terrain")
        st.plotly_chart(fig3)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage des latitudes/longitudes max/min 
    col5,col6,col7,col8 = st.columns(4)
    col5.metric('Latitude Maximum',str(round(dflalon(df18)['latitude'].max(), 2))+'°')
    col6.metric('Longitude Maximum',str(round(dflalon(df18)['longitude'].max(), 2))+'°')
    col7.metric('Latitude Minimum',str(round(dflalon(df18)['latitude'].min(), 2))+'°')
    col8.metric('Longitude Minimum',str(round(dflalon(df18)['longitude'].min(), 2))+'°')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Histogramme de la fréquence des différentes valeurs foncières
    x = df18['valeur_fonciere']
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
    fig.update_layout(title_text="Fréquence des différentes valeurs foncières",title_font_size=20)
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage du prix moyen des valeurs foncières et équivalence en lingots d'or
    ling1,ling2 = st.columns(2)
    ling1.metric('Prix Moyen',str(round(df18['valeur_fonciere'].mean(), 2))+' €')
    ling1.metric("Soit l'équivalent de: ",str(round(df18['valeur_fonciere'].mean()/50000, 2)) + "Lingots d'or")
    image = Image.open('lingot.png')
    ling2.image(image, use_column_width='auto')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #TOP 5 des communes les plus représentées
    n = st.slider('Nombre de communes :', 1, 30,5)
    st.header('TOP '+str(n)+ ' des communes les plus représentées')
    values = df18['nom_commune'].value_counts().head()
    st.bar_chart(values)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Moyenne des sommes dépensées par jours
    st.header('Moyenne des sommes dépensées par jours')
    st.area_chart(date(df18))

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

#Cinquième option: Données de l'année 2017
@timed
def opt5(mybar,percent_complete,df17):

    #Camembert de la nature des mutations:
    st.header('Nature des mutations:')
    labels=['Vente',"Vente en l'état futur d'achèvement","Echange","Vente terrain à bâtir","Adjudication","Expropriation"]
    values = df17['nature_mutation'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Choix de la région de la carte à afficher   
    option = st.selectbox(' Quelle carte voulez vous afficher ?', ('France Métropolitaine', 'Martinique', 'Île de la Réunion' ))
    if option == ('France Métropolitaine') :
      
        #Affichage de la carte
        fig = px.density_mapbox(dflalon(df17), lat='latitude', lon='longitude', radius=1,center=dict(lat=48.52, lon=2.19), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig)

    if option == 'Martinique':

        #Affichage de la carte
        fig2 = px.density_mapbox(dflalon(df17), lat='latitude', lon='longitude', radius=1,center=dict(lat=16, lon=-61), zoom=5,mapbox_style="stamen-terrain")
        st.plotly_chart(fig2)    

    if option == ('Île de la Réunion'):

        #Affichage de la carte
        fig3 = px.density_mapbox(dflalon(df17), lat='latitude', lon='longitude', radius=1,center=dict(lat=-21.1, lon=55.3), zoom=7,mapbox_style="stamen-terrain")
        st.plotly_chart(fig3)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage des latitudes/longitudes max/min 
    col5,col6,col7,col8 = st.columns(4)
    col5.metric('Latitude Maximum',str(round(dflalon(df17)['latitude'].max(), 2))+'°')
    col6.metric('Longitude Maximum',str(round(dflalon(df17)['longitude'].max(), 2))+'°')
    col7.metric('Latitude Minimum',str(round(dflalon(df17)['latitude'].min(), 2))+'°')
    col8.metric('Longitude Minimum',str(round(dflalon(df17)['longitude'].min(), 2))+'°')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Histogramme de la fréquence des différentes valeurs foncières
    x = df17['valeur_fonciere']
    fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True)])
    fig.update_layout(title_text="Fréquence des différentes valeurs foncières",title_font_size=20)
    st.plotly_chart(fig)

    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #Affichage du prix moyen des valeurs foncières et équivalence en lingots d'or
    ling1,ling2 = st.columns(2)
    ling1.metric('Prix Moyen',str(round(df17['valeur_fonciere'].mean(), 2))+' €')
    ling1.metric("Soit l'équivalent de: ",str(round(df17['valeur_fonciere'].mean()/50000, 2)) + "Lingots d'or")
    image = Image.open('lingot.png')
    ling2.image(image, use_column_width='auto')
    
    #Mise à jour de la barre de chargement
    percent_complete += 10
    mybar.progress(percent_complete)

    #TOP 5 des communes les plus représentées
    n = st.slider('Nombre de communes :', 1, 30,5)
    st.header('TOP '+str(n)+ ' des communes les plus représentées')
    values = df17['nom_commune'].value_counts().head()
    st.bar_chart(values)

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

    #Moyenne des sommes dépensées par jours
    st.header('Moyenne des sommes dépensées par jours')
    st.area_chart(date(df17))

    #Mise à jour de la barre de chargement
    percent_complete += 20
    mybar.progress(percent_complete)

def sel(op,df):
    st.write(df[op].head())

def check(dfglob):
    agree = st.checkbox('Voir une partie du Dataset')
    if agree:
        st.write(dfglob.head())
        agree2 = st.checkbox("Ne voir qu'une colonne")
        if agree2:
            op = st.selectbox('Choix de la colonne',('id_mutation','date_mutation','nature_mutation','valeur_fonciere','adresse_nom_voie','code_postal','code_commune','nom_commune','id_parcelle','longitude','latitude'))
            sel(op,dfglob)

def main():
    df17 = loadDF2017()
    df18 = loadDF2018()
    df19 = loadDF2019()
    df20 = loadDF2020()
    dfglob = loadDFglob(df17,df18,df19,df20)

    st.title('Project Dashboard Germain Deffontaines Valeurs Foncières')

    #Side bar :

    option1 = st.sidebar.selectbox(' Quelle année voulez vous afficher ?', ('Global','Année 2020', 'Année 2019', 'Année 2018', 'Année 2017' ))

    st.sidebar.write('Chargement :')
    mybar = st.sidebar.progress(0)
    percent_complete = 0

    st.sidebar.video('https://www.youtube.com/watch?v=AVhaRg4xG4Q')
    st.sidebar.video('https://www.youtube.com/watch?v=pVQUmGDesqc')
    st.sidebar.video('https://www.youtube.com/watch?v=yauu_vYDzCw')

    if option1 == 'Global':
        opt1(mybar,percent_complete,dfglob)
        check(dfglob)
    if option1 == 'Année 2020':
        opt2(mybar,percent_complete,df20)
        check(df20)
    if option1 == 'Année 2019':
        opt3(mybar,percent_complete,df19)
        check(df19)
    if option1 == 'Année 2018':
        opt4(mybar,percent_complete,df18)
        check(df18)
    if option1 == 'Année 2017':
        opt5(mybar,percent_complete,df17)
        check(df17)

if __name__ == "__main__":
    main()
