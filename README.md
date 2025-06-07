# FastAPI Calculator API

A simple calculator API built with FastAPI that allows users to perform basic arithmetic operations.

## Features

- Addition (`/add`)
- Subtraction (`/subtract`)
- Multiplication (`/multiply`)
- Division (`/divide`)

## Project Structure

```
.
├── main.py         # FastAPI application and calculator logic
├── requirements.txt  # Python dependencies
└── README.md       # This file
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    # git clone <repository-url>
    # cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the FastAPI application, use Uvicorn:

```bash
uvicorn main:app --reload
```

-   `main`: refers to the `main.py` file.
-   `app`: refers to the `app = FastAPI()` instance in `main.py`.
-   `--reload`: enables auto-reloading when code changes are detected (useful for development).

The API will typically be available at `http://127.0.0.1:8000`.

## API Endpoints

All calculator endpoints expect two query parameters: `x` (float) and `y` (float).

### Root

-   **GET /**
    -   Returns a welcome message.
    -   Example: `curl http://127.0.0.1:8000/`
    -   Response:
        ```json
        {"message":"Calculator API is running!"}
        ```

### Addition

-   **GET /add?x=<value>&y=<value>**
    -   Adds two numbers.
    -   Example: `curl "http://127.0.0.1:8000/add?x=5&y=3"`
    -   Response:
        ```json
        {"x":5.0,"y":3.0,"operation":"addition","result":8.0}
        ```

### Subtraction

-   **GET /subtract?x=<value>&y=<value>**
    -   Subtracts the second number from the first.
    -   Example: `curl "http://127.0.0.1:8000/subtract?x=10&y=4"`
    -   Response:
        ```json
        {"x":10.0,"y":4.0,"operation":"subtraction","result":6.0}
        ```

### Multiplication

-   **GET /multiply?x=<value>&y=<value>**
    -   Multiplies two numbers.
    -   Example: `curl "http://127.0.0.1:8000/multiply?x=7&y=6"`
    -   Response:
        ```json
        {"x":7.0,"y":6.0,"operation":"multiplication","result":42.0}
        ```

### Division

-   **GET /divide?x=<value>&y=<value>**
    -   Divides the first number by the second.
    -   Example: `curl "http://127.0.0.1:8000/divide?x=10&y=2"`
    -   Response:
        ```json
        {"x":10.0,"y":2.0,"operation":"division","result":5.0}
        ```
    -   **Error Handling (Division by Zero):**
        -   Example: `curl "http://127.0.0.1:8000/divide?x=10&y=0"`
        -   Response (Status Code 400):
            ```json
            {"detail":"Cannot divide by zero"}
            ```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:

-   Swagger UI: `http://127.0.0.1:8000/docs`
-   ReDoc: `http://127.0.0.1:8000/redoc`

These interfaces allow you to explore and test the API endpoints directly from your browser.
