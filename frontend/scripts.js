async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            document.getElementById('auth-page').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
        } else {
            alert('Ошибка входа');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function register() {
    const username = document.getElementById('register-username').value;
    const telegramId = document.getElementById('register-telegram-id').value;
    const password = document.getElementById('register-password').value;
    const passwordConfirm = document.getElementById('register-password-confirm').value;

    if (password !== passwordConfirm) {
        alert('Пароли не совпадают');
        return;
    }

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, telegram_id: telegramId, password })
        });
        
        if (response.ok) {
            alert('Регистрация успешна');
        } else {
            alert('Ошибка регистрации');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function sendMessage() {
    const recipient = document.getElementById('recipient-username').value;
    const message = document.getElementById('message-text').value;

    try {
        const response = await fetch('/send-message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ receiver_username: recipient, message_text: message })
        });

        if (response.ok) {
            alert('Сообщение отправлено');
        } else {
            alert('Ошибка отправки сообщения');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function getMessageHistory() {
    const username = document.getElementById('history-username').value;

    try {
        const response = await fetch(`/messages/history/${username}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const messages = await response.json();
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = '';
            messages.forEach(msg => {
                const div = document.createElement('div');
                div.textContent = `${msg.sender}: ${msg.content}`;
                historyList.appendChild(div);
            });
        } else {
            alert('Ошибка получения истории сообщений');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}