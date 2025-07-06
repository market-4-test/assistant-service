# Task 3: Assistant Service (Tag Suggestion)

This is a Python service that implements a `/suggest-tags` endpoint for automatically generating product tags using a local language model via Ollama.

## Tech Stack

* **Python 3.11**
* **FastAPI**: A modern, fast web framework for building APIs.
* **Ollama + Mistral**: For running the LLM locally.
* **Docker & Docker Compose**: For containerization and orchestration.

---

## Project Structure

```
.
├── config.py
├── main.py
├── schemas.py
├── services.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

---

## Prerequisites

1.  **Docker & Docker Compose**: Ensure they are installed and running on your system.
2.  **Ollama**: Install Ollama from the [official website](https://ollama.com/).

---

## Getting Started

#### 1. Run Ollama and Pull the Model

After installing Ollama, make sure the application is running. Then, execute the following command in your terminal to download the Mistral model:
```sh
ollama pull mistral
```

#### 2. Configure Environment Variables

Create a `.env` file in the project root. Make sure the `OLLAMA_BASE_URL` variable points to the Ollama instance on your host machine.
* **For macOS and Windows**: The value `http://host.docker.internal:11434` usually works out of the box.
* **For Linux**: Replace `host.docker.internal` with your host's IP address on the Docker network (often `172.17.0.1`). You can find it by running `ip a | grep docker0`.

#### 3. Build and Run the Service

Execute the following command in the project's root directory to build the Docker image and start the container:
```sh
docker-compose up --build -d
```
The service will then be available at `http://localhost:8001`.

---

## Usage

The service provides a single endpoint: `POST /suggest-tags`. You can test it using `curl` or any other HTTP client.

#### Sample Request

```sh
curl -X POST "http://localhost:8001/suggest-tags" \
-H "Content-Type: application/json" \
-d '{
  "name": "GoPro HERO11 Black",
  "description": "Get incredible highlight videos sent to your phone automatically with the HERO11 Black. Its new, larger image sensor captures more of the scene with higher image quality, letting you instantly share vertical shots to social media. HyperSmooth 5.0 features AutoBoost and Horizon Lock built-in, ensuring your smoothest, most stunning shots yet. Ideal for action sports, vlogging, and travel."
}'
```

#### Sample Response

```json
{
  "suggestedTags": [
    "action camera",
    "gopro",
    "vlogging",
    "4k video",
    "travel gear"
  ]
}
```

You can also access the interactive API documentation (Swagger UI) by navigating to `http://localhost:8001/docs` in your browser.