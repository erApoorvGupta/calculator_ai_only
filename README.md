# Scientific Calculator - FastAPI Backend and Next.js Frontend

This project implements a scientific calculator with a Python FastAPI backend and a Next.js frontend.

## Project Structure

The project is organized into two main directories:

-   `/backend`: Contains the FastAPI application that provides the calculator logic and API endpoints.
-   `/frontend`: Contains the Next.js application that provides the user interface.

Each directory has its own README with more specific instructions if needed, but basic setup and run commands are provided below.

## Backend (FastAPI)

The backend provides API endpoints for basic arithmetic and scientific calculations.

### Setup & Running (Backend)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend API will typically be available at `http://127.0.0.1:8000`.
    You can see the API documentation at `http://127.0.0.1:8000/docs`.

## Frontend (Next.js)

The frontend provides a web interface for the calculator, including an animated "magnet lines" background.

### Setup & Running (Frontend)

1.  **Navigate to the frontend application directory:**
    ```bash
    cd frontend/calculator-ui
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    # or
    # yarn install
    ```

3.  **Run the Next.js development server:**
    ```bash
    npm run dev
    # or
    # yarn dev
    ```
    The frontend application will typically be available at `http://localhost:3000`.

## Using the Calculator

Open your browser and navigate to the frontend URL (usually `http://localhost:3000`). The frontend will make API calls to the backend (usually running on `http://localhost:8000`). Ensure both servers are running.

You can configure the backend API URL for the frontend by setting the `NEXT_PUBLIC_API_BASE_URL` environment variable in a `.env.local` file within the `frontend/calculator-ui` directory. For example:
`NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`

If this variable is not set, it defaults to `http://localhost:8000`.
