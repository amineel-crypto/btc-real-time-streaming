# Real-Time Bitcoin Price Streaming Pipeline

A complete, real-time data streaming pipeline for ingesting, processing, storing, and visualizing live Bitcoin price data. The entire system is built on a dockerized microservices architecture, with each component running in its own container, orchestrated by Docker Compose.

---

## 🏛️ Architecture & Workflow

This diagram illustrates the end-to-end data flow of the microservices pipeline.

![Architecture Diagram](docs/images/architecture.png)

The system follows an event-driven pattern where services are decoupled using a message broker (like Kafka or Redpanda). This creates a scalable and resilient data pipeline.

1.  **Producer Service (`/producer` & `/api`):** A Python service (either a standalone script or a FastAPI endpoint) continuously fetches the latest Bitcoin price from an external API. It then publishes this data as a JSON message to a Kafka/Redpanda topic.
2.  **Streaming Platform (Redpanda):** Redpanda, a Kafka-compatible streaming platform, serves as the central message bus. It receives data from the producer and queues it in the `btc-metrics` topic, providing a durable buffer between services.
3.  **Consumer Service (`/consumer`):** A Python script subscribes to the Kafka/Redpanda topic. It listens for new price messages, processes them, and stores them in a MongoDB database for persistence.
4.  **Dashboard Service (`/dashboard`):** A Streamlit application provides the user-facing visualization. It queries the MongoDB database to retrieve data and displays it in a real-time, auto-updating chart.
5.  **Orchestration (`docker-compose.yml`):** The central Docker Compose file defines and connects all the services, their networks, and volumes.

---

## 🛠️ Tech Stack

*   **API / Producer:** [FastAPI](https://fastapi.tiangolo.com/), [Python](https://www.python.org/)
*   **Streaming Platform:** [Redpanda](https://redpanda.com/) (or any Kafka-compatible broker)
*   **Database:** [MongoDB](https://www.mongodb.com/)
*   **Dashboard/Visualization:** [Streamlit](https://streamlit.io/)
*   **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started (Docker Method)

This is the recommended way to run the entire application stack.

### Prerequisites

*   [**Docker**](https://www.docker.com/get-started) installed and running.
*   [**Docker Compose**](https://docs.docker.com/compose/install/) (usually included with Docker Desktop).
*   [**Git**](https://git-scm.com/) (to clone the repository).

### Installation & Execution

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/btc-real-time-streaming.git
    cd btc-real-time-streaming
    ```

2.  **Build and Run the Services**
    ```bash
    docker-compose up --build -d
    ```

---

## 🧪 Local Testing (Without Docker)

Use this method for development and debugging individual Python services directly on your host machine. We will still use Docker for the databases.

### Step 1: Start Backing Services

First, start Redpanda and MongoDB using Docker. This avoids having to install them manually.
```bash
docker-compose up -d redpanda mongodb


This command only starts the two specified services from your docker-compose.yml file.

Step 2: Set Up Python Environment

Create a Virtual Environment

Generated bash
python -m venv btc-venv
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Activate It

On Windows:

Generated cmd
.\btc-venv\Scripts\activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Cmd
IGNORE_WHEN_COPYING_END

On macOS/Linux:

Generated bash
source btc-venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Install All Dependencies
Install the requirements from all services into your single virtual environment.

Generated bash
pip install -r api/requirements.txt -r producer/requirements.txt -r consumer/requirements.txt -r dashboard/requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
Step 3: Run Each Service in a Separate Terminal

Open a new terminal for each service. Remember to activate the virtual environment in each new terminal.

Run the Producer (Open Terminal 1)

Generated bash
python producer/app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Run the Consumer (Open Terminal 2)

Generated bash
python consumer/app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Run the API (Open Terminal 3)

Generated bash
uvicorn api.main:app --reload
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Run the Dashboard (Open Terminal 4)

Generated bash
streamlit run dashboard/app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

You now have all Python services running locally, connected to the databases running in Docker.

📁 Project Structure
Generated code
.
├── api/                     # FastAPI service
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── consumer/                # Kafka consumer service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── dashboard/               # Streamlit dashboard service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── docs/                    # Documentation and assets
│   └── images/
│       └── architecture.png
├── producer/                # Standalone producer service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── docker-compose.yml       # Orchestrates all services, networks, and volumes.
├── .gitignore               # Specifies files for Git to ignore.
└── README.md                # This file.
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
🖥️ Accessing the Services

Streamlit Dashboard (Visualization):
Open your browser and go to: http://localhost:8501

FastAPI (API Docs):
To view the auto-generated API documentation, go to: http://localhost:8000/docs

🛑 Stopping the Application

To stop the local Python scripts: Press Ctrl + C in each of their terminals.

To stop the Docker containers (Redpanda & MongoDB):

Generated bash
docker-compose down
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
Generated code
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
