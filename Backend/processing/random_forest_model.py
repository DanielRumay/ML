import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_random_forest(data):
    """
    Entrena un modelo Random Forest para clasificar películas como relevantes o no.
    Args:
        data (list): Lista de diccionarios con los datos de las películas.
    Returns:
        model: Modelo entrenado.
    """
    # Prepara los datos
    X = [[movie['popularity'], movie['vote_average']] for movie in data]
    y = [1 if movie['popularity'] > 50 else 0 for movie in data]  # Relevante si popularidad > 50

    # Divide los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrena el modelo Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evalúa el modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precisión del modelo Random Forest: {accuracy:.2f}")

    # Guarda el modelo entrenado
    with open("random_forest_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    return model

def load_model():
    """
    Carga el modelo Random Forest guardado.
    Returns:
        model: Modelo cargado.
    """
    with open("random_forest_model.pkl", "rb") as f:
        return pickle.load(f)

def get_relevant_movies(model, data, num_recommendations=5):
    """
    Predice las películas relevantes usando el modelo entrenado.
    Args:
        model: Modelo Random Forest.
        data (list): Lista de diccionarios con los datos de las películas.
        num_recommendations (int): Número de recomendaciones a devolver.
    Returns:
        list: Lista de películas relevantes.
    """
    X = [[movie['popularity'], movie['vote_average']] for movie in data]
    predictions = model.predict(X)
    relevant_movies = [
        movie for movie, pred in zip(data, predictions) if pred == 1
    ]
    # Ordena las películas por popularidad
    relevant_movies.sort(key=lambda x: x['popularity'], reverse=True)
    return relevant_movies[:num_recommendations]