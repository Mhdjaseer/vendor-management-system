# Vendor Management System with Performance Metrics

## Introduction

This Vendor Management System is built using Django and Django REST Framework. The system handles vendor profiles, purchase orders, and calculates vendor performance metrics. It provides API endpoints for managing vendors, tracking purchase orders, and evaluating vendor performance.


## Installation and Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/mhdjaseer/vendor-management-system.git
    ```

2. Change to the project directory:

    ```bash
    cd vendor-management-system
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

8. Open your browser and navigate to [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) to access the API.

