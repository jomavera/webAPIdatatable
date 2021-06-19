# Table forfor accesible query of data from Web API using Airflow, Dash and Heroku

An ecuadorian supermarket shows its prices in a webpage so as to consumer can check product prices. This webpage doesn't allow to effectively filter, sort and search the price for a particular product. In this way, the purpose of this app is to create an app to access the product prices information and improve the accessibility to consumers. The app can be accessed in [link](http://pulldashboard.herokuapp.com/). This repo is for testing only so it extracts and loads data for 200 products but the DAG can be easily modified to extract the whole data.

## Description

The application is made up a **Airflow** app that schedules daily updates to the Webpsage database. The Webpage is a **Dash** app that reads data from a Postgress database and present it in a table. The table is capable of filtering and searching. The architecture is discribed in the following figure.


## Instructions
The following instructions guides to the creation of two separate apps in Heroku. One app runs the web interface of the table and connection to a Postgres database. The other app runs Airflow DAG that extracts data from the Web API and then loads the data the database of the first app. 

1. Clone repository

2. Create conda environment for Python project (In case of local testing)

    `conda create -n myenv python=3.8.10`

    `conda activate myenv`

3. Install libraries


    ```
    pip install dash pandas psycopg2-binary requests pandas
    pip install apache-airflow==2.1.0 apache-airflow-providers-postgres
    ```

4. Login to Heroku CLI (Instructions for [installation](https://devcenter.heroku.com/articles/heroku-cli#download-and-install))

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

8. Write down `DATABASE_URL` config var to use it in step 20

    `heroku config`

9. Commit changes

    ```
    git add .
    git commit -am "Initial commit"
    git push heroku master
    ```

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
    - `AIRFLOW__CORE__SQL_ALCHEMY_CONN = <SAME-AS-DATABASE_URL-CONFIG-VAR>`
    - `AIRFLOW__WEBSERVER__AUTHENTICATE = True`
    - `AIRFLOW_HOME = /app`
    
    Can be created in two ways:

    1. Heroku CLI as: `heroku config:set <CONFIG-VAR-NAME> = <CONFIG-VAR-VALUE>`
    2. From Settings in Heroku App webpage


15. Set `Procfile` to initialize airflow database

    - On `Procfile` write `web: airflow db init`

16. Commit changes to heroku repo

    ```
    git add .
    git commit -am "Initial commit"
    git push heroku master
    ```

17. SSH to Heroku instance

    Run  `heroku run bash`

18. In heroku app terminal create User

    ```
    airflow users create \
        --username admin \
        --firstname Peter \
        --lastname Parker \
        --role Admin \
        --email your-email@mail.org
    ```

19. Exit from heroku app terminal

20. Log in to Airflow Web UI at `<AIRFLOW-APP-NAME>.herokuapp.com` and create variable to store web app's database url from step 8

    Name the variable `db_url`

21. Set `Procfile` to run airflow webserver and scheduler

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