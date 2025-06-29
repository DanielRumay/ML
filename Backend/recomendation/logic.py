# recommendation/logic.py

import math

def cosine_similarity(v1, v2):
    """
    Calcula la similitud coseno entre dos vectores.
    """
    import math
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0
    return dot_product / (magnitude_v1 * magnitude_v2)

def get_recommendations(title, num_recommendations, data):
    """
    Genera recomendaciones basadas en similitud coseno.
    Args:
        title (str): Título de la película base.
        num_recommendations (int): Número de recomendaciones.
        data (list): Lista de datos de películas.
    Returns:
        list: Lista de títulos recomendados (únicos).
    """
    base_movie = next((movie for movie in data if movie.get("title") == title), None)
    if not base_movie:
        return ["No se encontró la película base"]

    try:
        base_vector = [float(base_movie["popularity"]), float(base_movie["vote_average"])]
    except (KeyError, TypeError, ValueError):
        return ["La película base no tiene datos válidos para recomendación"]

    similarities = []
    seen_titles = set()

    for movie in data:
        if movie.get("title") != title:
            try:
                other_vector = [float(movie["popularity"]), float(movie["vote_average"])]
                similarity = cosine_similarity(base_vector, other_vector)
                title_movie = movie["title"]

                if title_movie not in seen_titles:
                    similarities.append((title_movie, similarity))
                    seen_titles.add(title_movie)

            except (KeyError, TypeError, ValueError):
                continue  # Ignorar si los datos no son válidos

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [title for title, _ in similarities[:num_recommendations]]
