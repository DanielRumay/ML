document.getElementById('recomendation-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const movieTitle = document.getElementById('movie-title').value;
    const responseDiv = document.getElementById('response');

    responseDiv.innerHTML = 'Cargando...';

    try {
        const response = await fetch('https://ac23-38-255-108-181.ngrok-free.app/recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: movieTitle })
        });

        if (!response.ok) throw new Error(`Error del servidor: ${response.status}`);

        const result = await response.json();

        if (result.error) {
            responseDiv.innerHTML = `<p style="color: red;">${result.error}</p>`;
        } else if (result.length > 0) {
            responseDiv.innerHTML = `<h2>Recomendaciones:</h2><ul class="movie-list">${result.map(renderMovie).join('')}</ul>`;
        } else {
            responseDiv.innerHTML = `<p>No se encontraron recomendaciones.</p>`;
        }
    } catch (error) {
        responseDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});

// Función para generar HTML de una película
function renderMovie(movie) {
    const stars = generateStars(movie.vote_average);
    return `
        <li class="movie-item">
            <span class="movie-title">${movie.title}</span>
            <span class="movie-stars">${stars}</span>
        </li>
    `;
}

// Genera estrellas en base a vote_average
function generateStars(score) {
    const fullStars = Math.floor(score / 2); // 10 puntos = 5 estrellas
    const emptyStars = 5 - fullStars;
    return '★'.repeat(fullStars) + '☆'.repeat(emptyStars);
}
