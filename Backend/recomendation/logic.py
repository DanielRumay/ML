import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(title, top_n, data):
    # Buscar la película base
    base_movie = next((m for m in data if m.get("title", "").lower() == title.lower()), None)

    if not base_movie or "genre_ids" not in base_movie:
        return []

    # Filtrar películas del mismo género y con datos válidos
    same_genre = [
        m for m in data
        if m.get("title") != base_movie["title"]
        and "genre_ids" in m
        and any(g in m["genre_ids"] for g in base_movie["genre_ids"])
        and isinstance(m.get("vote_average"), (int, float))
        and isinstance(m.get("popularity"), (int, float))
    ]

    # Ordenar por popularidad descendente
    sorted_movies = sorted(same_genre, key=lambda x: -x["popularity"])

    # Eliminar duplicados por título
    seen_titles = set()
    unique_movies = []
    for m in sorted_movies:
        if m["title"] not in seen_titles:
            seen_titles.add(m["title"])
            unique_movies.append({
                "title": m["title"],
                "vote_average": m["vote_average"]
            })
        if len(unique_movies) == top_n:
            break

    return unique_movies
