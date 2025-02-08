# AI Travel Agent

## Overview
This project is an AI-powered travel agent/chatbot that can book hotels, cancel bookings and change check-in/check-out dates through natural language using a Large Language Model (LLM). The AI processes user requests and interacts with external scripts to execute the required actions.

Disclaimer: This project is only intended for educational purposes.

## Features
- **Book a hotel**: Users can specify hotel name, check-in/out dates, and number of guests to create a booking in the database.
- **Cancel a booking**: Users provide a booking ID to cancel a reservation. The booking will be deleted from the database on cancel.
- **Modify booking dates**: Users can change the check-in and check-out dates for an existing reservation.

## Technologies Used
- **FastAPI**: For handling API requests and responses.
- **Python**: Core language for backend development.
- **Ollama**: Runs the LLM model on a remote server.
- **Docker**: For containerization and deployment.
- **Redis**: For session and conversation history storage.
- **SQLite**: Is the database where bookings info is stored.
- **Gradio**: Technology used for the chatbot interface

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/joeltaberne/ai-travel-agent.git
   cd ai-travel-agent
   ```
2. Run the project through docker-compose:

   ```bash
   docker compose up
   ```

   You can run the Ollama container with GPU acceleration using docker-compose-gpu.yml. You may need to follow the [previous steps](https://docs.docker.com/engine/containers/resource_constraints/#gpu) before being able to use GPU acceleration in Docker.

   ```bash
   docker compose -f docker-compose-gpu.yml up
   ```

3. Wait until the model is successfully downloaded. This can take some time depending on your network speed, as the default model defined in Modelfile (phi4) size is about 9.1GB. Once the model is installed successfully, you should be able to perform requests to the API.

4.  You can now access the GUI through ```http://localhost:80```

## Usage

![image](https://github.com/user-attachments/assets/d32704b2-2ca7-4f7c-97a3-ff418a642e51)

On the left side, you can interact with the model. Once a conversation has ended, you can clear the chat to start a new conversation with no context or previous history.

On the right side, the bookings made through the agent and its data will appear. When you create, modify, or cancel a booking, make sure to use the Refresh button to get updated information.
