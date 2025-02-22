import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# Fonction de scraping pour "Poules, lapins et pigeons"
def scrape_poules_lapins(num_pages):
    df = pd.DataFrame()
    for i in range(num_pages):  # Scraper sur le nombre de pages choisi par l'utilisateur
        url = f'https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons?page={i}'
        html_code = requests.get(url)
        soup = bs(html_code.text, "html.parser")
        containers = soup.find_all('div', class_="col s6 m4 l3")

        data = []
        for container in containers:
            try:
                # Récupérer l'URL de la page de détail de l'annonce
                url_container = "https://sn.coinafrique.com" + container.find('a', class_='card-image ad__card-image waves-block waves-light')['href']
                res_c = requests.get(url_container)
                soup_c = bs(res_c.text, 'html.parser')

                # Extraire les détails de l'annonce
                details = soup_c.find('div', class_="ad__info__box ad__info__box-descriptions").text.strip()
                prix = container.find('p', class_="ad__card-price").text.strip()
                adresse = container.find('p', class_='ad__card-location').text.strip()
                image_lien = container.find('img', class_='ad__card-img')['src']

                # Ajouter les données à la liste
                data.append({
                    'details': details,
                    'prix': prix,
                    'adresse': adresse,
                    'image_lien': image_lien
                })
            except:
                pass

        # Ajouter les données de la page actuelle au DataFrame
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df

# Fonction de scraping pour "Autres animaux"
def scrape_autres_animaux(num_pages):
    df = pd.DataFrame()
    for i in range(num_pages):  # Scraper sur le nombre de pages choisi par l'utilisateur
        url = f'https://sn.coinafrique.com/categorie/autres-animaux?page={i}'
        html_code = requests.get(url)
        soup = bs(html_code.text, "html.parser")
        containers = soup.find_all('div', class_="col s6 m4 l3")

        data = []
        for container in containers:
            try:
                nom = container.find('p', class_='ad__card-description').text.strip()
                prix = container.find('p', class_='ad__card-price').text.strip()
                adresse = container.find('p', class_='ad__card-location').text.strip()
                image_lien = container.find('img', class_='ad__card-img')['src']
                data.append({
                    'nom': nom,
                    'prix': prix,
                    'adresse': adresse,
                    'image_lien': image_lien
                })
            except:
                pass

        # Ajouter les données de la page actuelle au DataFrame
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df

# Configuration de la page Streamlit
st.set_page_config(page_title="Scraping de Coinafrica", page_icon="🐔", layout="wide")

# Titre de l'application
st.title("Scraping de Coinafricaa 🐔🐰🐦")
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stSelectbox div {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Onglets pour organiser les fonctionnalités
tab1, tab2, tab3 = st.tabs(["Scraping", "Importer des données", "Évaluation"])

with tab1:
    st.header("📊 Scraping des données")
    st.markdown("Scrapez les données des annonces de Coinafrica en fonction de la catégorie choisie.")

    # Slider pour choisir le nombre de pages à scraper
    num_pages = st.slider("Choisissez le nombre de pages à scraper :", min_value=1, max_value=30, value=3)

    # Option de scraping
    option = st.selectbox("Choisissez une catégorie :", ["Poules, lapins et pigeons", "Autres animaux"])

    if st.button("Lancer le scraping"):
        with st.spinner("Scraping en cours... Veuillez patienter."):
            if option == "Poules, lapins et pigeons":
                data = scrape_poules_lapins(num_pages)
            else:
                data = scrape_autres_animaux(num_pages)

        st.success(f"Scraping terminé sur {num_pages} pages ! Voici un aperçu des données :")
        st.dataframe(data.head(10))

        # Télécharger les données en CSV (sans utiliser io)
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les données en CSV",
            data=csv,
            file_name="scraped_data.csv",
            mime="text/csv"
        )

with tab2:
    st.header("📂 Importer des données")
    st.markdown("Importez un fichier CSV exporté depuis Web Scraper pour visualiser les données.")

    uploaded_file = st.file_uploader("Téléchargez un fichier CSV", type=["csv"])
    if uploaded_file:
        df_uploaded = pd.read_csv(uploaded_file)
        st.dataframe(df_uploaded.head(20))

with tab3:
    st.header("📝 Évaluation de l'application")
    st.markdown("Merci de prendre quelques minutes pour évaluer l'application.")

    # Option pour choisir le formulaire
    form_option = st.selectbox("Choisissez un formulaire :", ["Formulaire Kobo", "Formulaire Google Forms"])

    if form_option == "Formulaire Kobo":
        st.markdown("""
            <iframe src="https://ee-eu.kobotoolbox.org/x/V0PTKZ7J" width="100%" height="800" style="border:none;"></iframe>
        """, unsafe_allow_html=True)
    elif form_option == "Formulaire Google Forms":
        st.markdown("""
            <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScKVi8HpSYaeYnxaSp6ckDtkkC95xaqi2VZ3QV6IW5AYiKaWA/viewform?usp=dialog" width="100%" height="800"
             style="border:none;"></iframe>""", unsafe_allow_html=True)
