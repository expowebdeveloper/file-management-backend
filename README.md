# Define the content of the README file

# FastAPI Document Management API

This is a backend application for managing document listings using FastAPI. The API allows CRUD operations on documents stored in a SQLite database.

---

## Features

- **List documents**: View all documents with optional search, sorting, and pagination.
- **Retrieve a document**: Fetch a document by its ID.
- **Create a document**: Add a new document with name and content.
- **Delete a document**: Remove a document by its ID.

---

## Setup Instructions

### Prerequisites

Ensure you have the following installed on your system:
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
- Python 3.12+ (only for local setup without Docker).
- Git.

---

### Running the Application

#### Using Docker Compose (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/expowebdeveloper/file-management-backend.git
   cd file-management-backend



## Build and start the application:



```
docker-compose up --build
```
### Access the API documentation:

Swagger UI: http://localhost:8000/docs 

ReDoc: http://localhost:8000/redoc



# API Documentation

## Endpoints

| Method | Endpoint                | Description                      |
|--------|-------------------------|----------------------------------|
| GET    | `/documents`             | List all documents              |
| GET    | `/documents/{id}`        | Retrieve a specific document    |
| POST   | `/documents`             | Create a new document           |
| DELETE | `/documents/{id}`        | Delete a document               |

