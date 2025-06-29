document.getElementById('recomendation-form').addEventListener('submit', async function (event) {
    event.preventDefault();  // Prevenir la acción predeterminada del formulario

    const movieTitle = document.getElementById('movie-title').value;
    const responseDiv = document.getElementById('response');

    // Limpiar la respuesta previa
    responseDiv.innerHTML = 'Cargando...';

    try {
        // Realizar la solicitud POST al servidor con el título de la película
        const response = await fetch('https://aea9-2800-200-fdc0-1e48-9c2-be58-506b-72e6.ngrok-free.app/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: movieTitle })  // Enviar el título de la película como JSON
        });

        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }

        const result = await response.json();

        if (result.error) {
            // Si hay un error en la respuesta, mostrar el error
            responseDiv.innerHTML = `<p style="color: red;">${result.error}</p>`;
        } else {
            // Mostrar las recomendaciones si no hay error
            const recommendations = result;  // La respuesta es directamente un arreglo de películas
            if (recommendations.length > 0) {
                responseDiv.innerHTML = `
                    <h2>Recomendaciones:</h2>
                    <ul>
                        ${recommendations.map(movie => `<li>${movie}</li>`).join('')}
                    </ul>
                `;
            } else {
                responseDiv.innerHTML = `<p>No se encontraron recomendaciones.</p>`;
            }
        }
    } catch (error) {
        // En caso de error en la solicitud, mostrar el mensaje de error
        responseDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});

