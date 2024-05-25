How to run Project

Provide step-by-step instructions on how to set up the project locally.

1. Clone the repository:
    ```bash
    git clone https://github.com/daiyan52/FootFusion-E-commerce-Site
    ```

2. Change into the project directory:
    ```bash
    cd  FootFusion-E-commerce-Site
    cd  FootFusion
    ```

3. Create and activate a virtual environment:
    ```bash
    virtualenv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up the database:
    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

6. Create a superuser to access the Django admin:
    ```bash
    python3 manage.py createsuperuser
    ```

7. Run the development server:
    ```bash
    python3 manage.py runserver
    ```
