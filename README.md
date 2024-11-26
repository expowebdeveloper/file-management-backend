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
   ```bash
   git clone https://github.com/your-repo/document-api.git
   cd document-api
