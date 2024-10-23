// Функция для входа пользователя в систему.
async function login() {
    // Получаем введенные имя пользователя и пароль.
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        // Отправляем POST-запрос для получения токена.
        const response = await fetch('/api/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ username, password })
        });

        if (response.ok) {
            // Если вход успешен, сохраняем токен и имя пользователя.
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('username', username);

            // Подключаемся к WebSocket после успешного логина.
            connectWebSocket(username);

            // Переход в личный кабинет.
            document.getElementById('auth-page').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
        } else {
            alert('Ошибка входа. Неверный логин или пароль');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Функция для регистрации нового пользователя.
async function register() {
    // Получаем введенные данные.
    const username = document.getElementById('register-username').value;
    const telegramId = document.getElementById('register-telegram-id').value;
    const password = document.getElementById('register-password').value;
    const passwordConfirm = document.getElementById('register-password-confirm').value;

    // Проверяем, совпадают ли пароли.
    if (password !== passwordConfirm) {
        alert('Пароли не совпадают');
        return;
    }

    try {
        // Отправляем POST-запрос для регистрации.
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                username: username, 
                telegram_id: telegramId, 
                password: password 
            })
        });

        if (response.ok) {
            alert('Регистрация успешна');
        } else {
            // Показываем ошибку, если регистрация не удалась.
            const errorData = await response.json();
            alert(`Ошибка регистрации: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при регистрации');
    }
}

// Переменная для хранения WebSocket соединения.
let socket;

// Функция для подключения к WebSocket.
function connectWebSocket(username) {
    // Получаем токен из localStorage.
    const token = localStorage.getItem('access_token');

    // Проверяем, что пользователь авторизован.
    if (!token) {
        alert("Требуется авторизация");
        return;
    }

    // Подключаемся к WebSocket эндпоинту с токеном.
    socket = new WebSocket(`ws://localhost/api/ws/${username}?token=${token}`);

    // Событие открытия соединения.
    socket.onopen = function(event) {
        console.log("Соединение установлено");
    };

    // Событие получения сообщения.
    socket.onmessage = function(event) {
        const message = JSON.parse(event.data);
        console.log("Получено сообщение:", message);

        // Отображаем сообщение на странице в разделе "Входящие сообщения".
        const messagesList = document.getElementById("messages-list");
        const messageItem = document.createElement("div");
        messageItem.textContent = `${message.sender}: ${message.message}`;
        messagesList.appendChild(messageItem);
    };

    // Событие закрытия соединения.
    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log(`Соединение закрыто чисто, код=${event.code} причина=${event.reason}`);
        } else {
            console.error("Соединение прервано");
        }
    };

    // Событие ошибки.
    socket.onerror = function(error) {
        console.error("Ошибка WebSocket:", error);
    };
}

// Функция отправки сообщения через WebSocket.
function sendMessage() {
    // Получаем введенные данные.
    const recipient = document.getElementById('recipient-username').value;
    const message = document.getElementById('message-text').value;

    // Проверяем, что WebSocket соединение открыто.
    if (socket.readyState === WebSocket.OPEN) {
        const messageData = {
            receiver: recipient,
            message: message
        };
        // Отправляем сообщение.
        socket.send(JSON.stringify(messageData));
        console.log(`Сообщение отправлено: ${JSON.stringify(messageData)}`);
    } else {
        console.error("WebSocket соединение не открыто");
    }
}

// Функция для получения истории сообщений между текущим пользователем и другим пользователем.
async function getMessageHistory() {
    const user2 = document.getElementById('history-username').value;
    const user1 = localStorage.getItem('username');  // Текущий пользователь, сохраняемый при логине.

    // Проверяем, что указаны оба пользователя.
    if (!user1 || !user2) {
        alert("Оба пользователя должны быть указаны для получения истории сообщений");
        return;
    }

    try {
        // Отправляем GET-запрос для получения истории сообщений.
        const response = await fetch(`/api/history/${user1}/${user2}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            // Отображаем историю сообщений.
            const messages = await response.json();
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = '';
            messages.forEach(msg => {
                const div = document.createElement('div');
                div.textContent = `${msg.sender}: ${msg.message}`;
                historyList.appendChild(div);
            });
        } else {
            alert('Ошибка получения истории сообщений');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Функция для показа личного кабинета и скрытия форм авторизации и регистрации.
function showDashboard() {
    document.getElementById('auth-page').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
}

// Функция для проверки валидности токена.
function isTokenValid(token) {
    try {
        const payloadBase64 = token.split('.')[1];
        const decodedPayload = JSON.parse(atob(payloadBase64));
        const currentTime = Math.floor(Date.now() / 1000);
        return decodedPayload.exp > currentTime;
    } catch (error) {
        console.error('Ошибка проверки токена:', error);
        return false;
    }
}

// Событие, которое происходит при загрузке страницы.
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем наличие и валидность токена.
    const token = localStorage.getItem('access_token');
    const username = localStorage.getItem('username');

    if (token && isTokenValid(token)) {
        // Если токен валиден, показываем личный кабинет и подключаем WebSocket.
        showDashboard();
        connectWebSocket(username);
    } else {
        // Если токен недействителен, очищаем его и остаемся на странице логина.
        localStorage.removeItem('access_token');
        localStorage.removeItem('username');
    }
});

// Функция для выхода из системы.
function logout() {
    // Удаляем токен и имя пользователя из localStorage.
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');

    // Закрываем WebSocket соединение, если оно существует.
    if (socket) {
        socket.close();
    }

    // Показываем страницу авторизации.
    document.getElementById('auth-page').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}

