# Instant Messaging Service with Telegram Bot Notifications

## Overview

This is an instant messaging service that allows users to exchange messages with each other and receive offline notifications via a Telegram bot. Registration is simple and requires only a username and password, without the need for email verification. There are no restrictions on the format of the username or password.

## Technologies Used

### Backend
- **Python**: The backend is built using several powerful Python frameworks and libraries:
  - **FastAPI**: For building the REST API.
  - **Aiogram3**: For interacting with the Telegram API to send notifications.
  - **SQLAlchemy**: For database interaction.
  - **WebSocket**: For real-time communication between users.
  - **Jose**: For creating and validating authentication tokens.

### Frontend
- **JavaScript (vanilla)**: The frontend is written using plain JavaScript, along with HTML and CSS for structure and styling.

### Infrastructure
- **Nginx**: Used for reverse proxying between the frontend and backend services.
- **SupervisorD**: Used to manage processes inside the backend container, particularly to ensure both the Telegram bot and backend server run from a single container. Given the simplicity of the bot (only one file), there's no need for a separate container.
- **PostgreSQL**: Used as the database for storing user and message data.
- **Docker**: The entire application is containerized for ease of deployment.

## Getting Started

To get started, clone the repository and run the following command from the root directory of the project:

```sh
docker-compose up --build
```

This command will build and run the Docker containers for the entire application stack, including the database, backend, and frontend.

## Features
- **User Registration**: Users can easily register with a username and password without email verification.
- **Real-Time Messaging**: Exchange messages with other users in real-time using WebSockets.
- **Telegram Bot Notifications**: Users receive notifications via a Telegram bot when they are offline and receive a message.

## Project Structure
- **backend**: Contains the backend API, WebSocket endpoint, and Telegram bot.
- **frontend**: Contains HTML, CSS, and JavaScript files for the user interface.
- **nginx**: Contains the Nginx configuration for reverse proxying.

## Usage
1. Access the application via `http://localhost`.
2. Register a new account by providing a username, Telegram ID, and password.
3. Log in to access your dashboard, send messages, and view message history.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, feel free to contact the maintainer of this project.

