let page = 1; // Página inicial
const $postContainer = $("#postContainer");
const $loading = $("#loading");

// Función para obtener imagenes
function fetchPosts(page) {
    // Simulamos una API que devuelve publicaciones
    $loading.removeClass("d-none");
    return $.get('http://127.0.0.1:8000/ver_imagenes')
        .done(function (data) {
            $loading.addClass("d-none");
            // Llamamos a renderPosts con el array de imágenes recibido
            renderPosts(data.images); // 'data.images' es el array de publicaciones
        });
}

// Función para renderizar las publicaciones
function renderPosts(posts) {
    posts.forEach(post => {
        const postElement = `
            <div class="col-md-4">
                <div class="post-card">
                    <img src="${post.image_path}" alt="${post.title}">
                    <div class="card-body">
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


// Función para registrar un usuario
function registerUser() {
    document.getElementById("registerForm").addEventListener("submit", function(e) {
        e.preventDefault();
        
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const data = {
            username: username,
            password: password
        };

        fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            // Cerrar el modal después de registrar
            $('#registerModal').modal('hide');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un error al registrar el usuario.');
        });
    });
}

// Llamamos a la función de registro
registerUser();

// Función de login con jQuery
$("#loginForm").on("submit", function(event) {
    event.preventDefault();

    // Obtener datos del formulario
    const username = $("#username_login").val();
    const password = $("#password_login").val();

    // Enviar los datos al backend para hacer el login
    $.ajax({
        url:"/login",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            username: username,
            password: password
        }),
        success: function(data) {
            // Guardar el token en el localStorage
            localStorage.setItem("access_token", data.access_token);
            alert("Login exitoso");

            // Redirigir a una página de inicio o cerrar el modal
            window.location.href = "/"; // Redirigir a una página de inicio
        },
        error: function(xhr, status, error) {
            const errorMessage = xhr.responseJSON ? xhr.responseJSON.detail : "Error en el login";
            alert(errorMessage);
        }
    });
});

// Visibilidad de botones
$(document).ready(function () {
    // Ocultar el botón por defecto
    $('#boton_cargar_imagen').hide();
    $('#boton_logout').hide();

    // Mostrar el botón si existe el access_token en localStorage
    if (localStorage.getItem('access_token')) {
        $('#boton_cargar_imagen').show();
        $('#boton_logout').show();
    }

    // Ocultar botones si no existe esl access_token en el localstorage
    if (localStorage.getItem('access_token')) {
        $('#boton_registro').hide();
        $('#boton_login').hide();

    }

    // Controlar el cierre de sesión     
    $('#confirmLogout').on('click', function () {
        // Borrar todo el contenido del localStorage
        localStorage.clear();

        // Redirigir a la página principal
        window.location.href = '/';
    });

    /***************************** */
    // carga de imagenes
     $('#uploadForm').submit(function (e) {
        e.preventDefault(); // Prevenir el comportamiento predeterminado del formulario

        // Obtener el token de acceso del localStorage
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            alert('No estás autenticado');
            return;
        }

        // Crear un FormData para enviar la imagen
        const formData = new FormData();
        const imageTitle = $('#imageTitle').val();
        const imageFile = $('#imageFile')[0].files[0];

        if (!imageFile) {
            alert('Por favor, selecciona una imagen');
            return;
        }

        formData.append('title', imageTitle);
        formData.append('image', imageFile);

        // Realizar la solicitud AJAX para subir la imagen
        $.ajax({
            url: '/upload-image', // Ruta donde se manejará la carga de la imagen en el backend
            type: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}` // Enviar el token en el encabezado
            },
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                alert('Imagen subida exitosamente');
                $('#uploadModal').modal('hide'); // Cerrar el modal
            },
            error: function (error) {
                alert('Error al subir la imagen');
            }
        });
    });
});
