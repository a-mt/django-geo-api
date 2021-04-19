
## Install

* Install the dependencies

    ```
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

* Initialize the database

    ```
    cd site
    python manage.py migrate
    python manage.py createsuperuser  # optional
    python manage.py populatedb
    ```

## Run

* Make sure you're using the right environment

  ```
  source env/bin/activate
  cd site
  ```

* Start the server

  ```
  python manage.py runserver
  ```

* Go to http://localhost:8000  

  ```
  /         : UI
  /api      : api endpoints
  /api/docs : api documentation
  ```

## Update css

* Install the dependencies

  ```
  npm install --only=dev
  ```

* Build .css and minify to .min.css

  ```
  npm run build:css
  npm run minify:css
  ```
