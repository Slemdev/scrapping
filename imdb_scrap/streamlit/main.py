import streamlit as st
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')

client = pymongo.MongoClient(ATLAS_KEY)

db = client.imdb
collection = client.top_250.top_250_movies



def display_answers():
    st.subheader("Réponses aux questions")

    st.title("1. Quel est le film le plus long ?")
    longest_film = collection.find().sort("duration", pymongo.DESCENDING).limit(1)
    for film in longest_film:
        st.write(f"{film['original_title']} ({film['duration']} minutes)")

    st.title("2. Quels sont les 5 films les mieux notés ?")
    top_rated_films = collection.find().sort("rating", pymongo.DESCENDING).limit(5)
    for film in top_rated_films:
        st.write(f"{film['original_title']} ({film['rating']})")

    st.title("3. Combien de films du top 250 ont été joués par Morgan Freeman et Tom Cruise ?")
    count_MF = collection.count_documents({"casting": "Morgan Freeman"})
    count_TC = collection.count_documents({"casting": "Tom Cruise"})
    st.write(f"Morgan Freeman a joué dans {count_MF} film(s) du top 250.")
    st.write(f"Tom Cruise a joué dans {count_TC} film(s) du top 250.")

    st.title("4. Quels sont les 3 films d'horreur les mieux notés ?")
    top_horror_films = collection.find({"genre": "Horror"}).sort("rating", pymongo.DESCENDING).limit(3)
    for film in top_horror_films:
        st.write(f"{film['original_title']} ({film['rating']})")

    st.title("5. Quel pourcentage de films français et américains figure dans le top 250 ?")
    count_fr = collection.count_documents({"country": "France"})
    count_us = collection.count_documents({"country": "United States"})
    st.write(f"Il y a {round((count_fr * 100) / 250, 2)}% de films français et {round((count_us * 100) / 250, 2)}% de films américains.")

    st.title("6. Quelle est la durée moyenne des films de comédie ?")
    comedy_films = collection.find({"genre": "Comedy"})
    count_comedy_films = collection.count_documents({"genre": "Comedy"})
    duration_average = sum([film["duration"] for film in comedy_films]) / count_comedy_films
    st.write(f"La durée moyenne des films de comédie est de {round(duration_average, 2)} minutes.")



def search_by_name(name):
    results = collection.find({"original_title": {"$regex": name, "$options": "i"}})
    return results


def search_by_actor(actor):
    results = collection.find({"casting": {"$regex": actor, "$options": "i"}})
    return results


def search_by_genre(genre):
    results = collection.find({"genre": {"$regex": genre, "$options": "i"}})
    return results


def search_by_duration(duration):
    results = collection.find({"duration": {"$lte": duration}})
    return results


def search_by_rating(rating):
    results = collection.find({"rating": {"$gte": rating}})
    return results




def main():
    st.title('Recherche de films dans la base de données')

    menu = st.sidebar.selectbox(
        "Menu",
        (
            "Recherche",
            "Réponses aux questions",
        ),
    )

    if menu == "Recherche":
        search_type = st.selectbox(
            "Sélectionnez le type de recherche",
            (
                "Par nom",
                "Par acteur(s)",
                "Par genre",
                "Par durée (inférieure à x minutes)",
                "Par note minimale"
            ),
        )

        search_input = st.text_input("Entrez votre recherche")

        if search_type == "Par nom" and search_input:
            results = search_by_name(search_input)

        elif search_type == "Par acteur(s)" and search_input:
            results = search_by_actor(search_input)

        elif search_type == "Par genre" and search_input:
            results = search_by_genre(search_input)

        elif search_type == "Par durée (inférieure à x minutes)" and search_input:
            try:
                duration = int(search_input)
                results = search_by_duration(duration)
            except ValueError:
                st.error("Veuillez entrer une durée en minutes (nombre entier).")

        elif search_type == "Par note minimale" and search_input:
            try:
                rating = float(search_input)
                results = search_by_rating(rating)
            except ValueError:
                st.error("Veuillez entrer une note minimale (nombre décimal).")

        else:
            results = []

        if results:
            for result in results:
                st.write(f"Titre: {result['original_title']}")
                st.write(f"Durée: {result['duration']} minutes")
                st.write(f"Genre: {result['genre']}")
                st.write(f"Note: {result['rating']}")
                st.write(f"Acteurs: {', '.join(result['casting'])}")
                st.write(f"Pays: {result['country']}")
                st.write(f"Année: {result['year']}")
                st.write("---")
        else:
            st.write("Aucun résultat trouvé.")
        
    elif menu == "Réponses aux questions":
        display_answers()



if __name__ == "__main__":
    main()
