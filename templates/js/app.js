let page = 1; // Página inicial
const $postContainer = $("#postContainer");
const $loading = $("#loading");

// Función para obtener publicaciones simuladas
function fetchPosts(page) {
    // Simulamos una API que devuelve publicaciones
    $loading.removeClass("d-none");
    return $.get(`https://jsonplaceholder.typicode.com/photos?_page=${page}&_limit=6`)
        .done(function () {
            $loading.addClass("d-none");
        });
}

// Función para renderizar las publicaciones
function renderPosts(posts) {
    posts.forEach(post => {
        const postElement = `
            <div class="col-md-4">
                <div class="post-card">
                    <img src="${post.url}" alt="${post.title}">
                    <div class="card-body">
                        <div class="username">User_${post.id}</div>
                        <div class="description">${post.title}</div>
                    </div>
                </div>
            </div>
        `;
        $postContainer.append(postElement);
    });
}

// Scroll infinito
$(window).on("scroll", function () {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
        page++;
        fetchPosts(page).then(renderPosts);
    }
});

// Cargar la primera tanda de publicaciones al iniciar
fetchPosts(page).then(renderPosts);
