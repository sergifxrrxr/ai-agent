# AI Travel Agent

## Overview
This project is an AI-powered travel agent that can book hotels, cancel bookings and change check-in/check-out dates through natural language using a Large Language Model (LLM) with FastAPI. The AI processes user requests and interacts with external scripts to execute the required actions.

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

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/ai-travel-agent.git
   cd ai-travel-agent
   ```
2. Run the project through docker-compose:

   ```bash
   docker compose up
   ```

   You can run the LLM with GPU acceleration using docker-compose-gpu.yml. You may need to follow the [previous steps](https://docs.docker.com/engine/containers/resource_constraints/#gpu) before being able to use GPU acceleration in Docker.

   ```bash
   docker compose -f docker-compose-gpu.yml up
   ```

3. Wait until the model is successfully downloaded. This can take some time depending on your network speed, as the default model defined in Modelfile (phi4) size is about 9.1GB. Once the model is installed successfully, you should be able to perform requests to the API.

## API Endpoints
### `POST /chat`
The system handles user input and generates responses from the AI. The AI will prompt the user for information until it identifies the intended action and gathers all the necessary data to complete that action. Once all required data is collected, the model will respond with a JSON object. This JSON response will be processed by FastAPI, which will execute the corresponding action on the database and return a fixed response to the user.

#### Query Parameters:
| Parameter  | Type   | Description |
|-----------|--------|-------------|
| `user_input` | `string` | The message from the user. |
| `session_id` | `string` | Unique session identifier. It is generated at the first request, and it must be added to the next ones so the model can access the conversation history and give more accurate responses.|

#### Example Request:
```bash
curl -X POST "http://localhost:5005/chat?user_input=Book%20The%20Ritz%20from%202025-07-01%20to%202025-07-05%20for%202%20adults&session_id=12345"
```

#### Example Response:
```json
{
  "action": "book",
  "hotel": "Magic Ski",
  "check_in": "2025-07-01",
  "check_out": "2025-07-05",
  "adults": 2,
  "children": 0
}
```

