# Table for 

## Description


## Instructions
The following instructions are for creating two separate apps in Heroku. In one app runs the web interface of the table with access to a Postgres database and on the other app runs airflow that extracts data from the web api and load it to the database of the first app. 

1. Clone repository

2. Create conda environment for python project

    `conda create -n myenv python=3.8.10`

    `conda activate myenv`

3. Install libraries


    ```
    pip install dash pandas psycopg2-binary requests pandas
    pip install apache-airflow==2.1.0 apache-airflow-providers-postgres
    ```

4. Login to Heroku CLI

    `heroku login`

### Web app

5. Inside `dashApp` directory create git repository

    ```
        cd dashApp
        git init
    ```

6. Create app in Heroku

    `heroku create --app <WEB-APP-NAME>`

7. Add Heroku Postgres to app

    Run from terminal `heroku addons:create heroku-postgresql:hobby-dev --app <WEB-APP-NAME>`

8. Write down `DATABASE_URL` to use in step 14

9. Commit changes

    `git add .`
    `git commit -am "Initial commit"`
    `git push heroku master`

### Airflow

10. Inside `airflowApp` directory create git repository

    `git init`


11. Create an app in Heroku CLI

    `heroku create --app <AIRFLOW-APP-NAME>`

12. Add Heroku Postgres to app

    Run from terminal `heroku addons:create heroku-postgresql:hobby-dev --app <AIRFLOW-APP-NAME>`

13. Create Fernet key

    From Python terminal
    ```
    >>> from cryptography import fernet
    >>> fernet.Fernet.generate_key()
    b'pZcwcoB8RQfjtE9n0Du5Weu8zLKoFphKkiGDBihOwcM='
    >>>
    ```

14. Create `Config Vars`

    Create the following Config Vars
    - `AIRFLOW__CORE__FERNET_KEY = <YOUR-FERNET-KEY>`
    - `AIRFLOW__CORE__LOAD_EXAMPLES = False`
    - `AIRFLOW__CORE__SQL_ALCHEMY_CONN = <SAME-AS-DATABASE_URL-FROM-STEP-8>`
    - `AIRFLOW__WEBSERVER__AUTHENTICATE = True`
    - `AIRFLOW_HOME = /app`
    
    Can be created in two ways:

    1. Heroku CLI as: `heroku config:set <CONFIG-VAR-NAME> = <CONFIG-VAR-VALUE>`
    2. From Settings in Heroku App webpage


15. Set `Procfile`

    - On `Procfile` write `web: airflow db init`

16. Commit changes to heroku repo

    ```
    git add .
    git commit -am "Initial commit"
    git push heroku master
    ```

17. SSH to Heroku instance

    Run  `heroku run bash`

18. Create User

    ```
    airflow users create \
        --username admin \
        --firstname Peter \
        --lastname Parker \
        --role Admin \
        --email your-email@mail.org
    ```

19. Exit from heroku app terminal

20. Log in to Airflow Web UI and create variable to store web app database url

    Name the variable `db_url`

21. Update `Procfile` to run scheduler

    - On `Procfile` write `web: airflow webserver --port $PORT --daemon & airflow scheduler`

22. Commit changes to heroku repo

    ```
    git add .
    git commit -am "Update Procfile"
    git push heroku master
    ```

23. Log in to Airflow Web UI and run DAG

## References

- [Running Airflow on Heroku](https://medium.com/@damesavram/running-airflow-on-heroku-ed1d28f8013d)