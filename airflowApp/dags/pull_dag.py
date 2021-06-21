from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

import datetime
import psycopg2
import requests
import numpy as np

def pullData():
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "proveedores.elrosado.com",
        "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT",
        "Origin": "https://www.elrosado.com",
        "Pragma": "no-cache",
        "Referer": "https://www.elrosado.com/",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:85.0) Gecko/20100101 Firefox/85.0",
    }
    base_url = "https://proveedores.elrosado.com/WebApi/Api/ListaPrecio/consultaListaPreciosgeneral/?tipoListag=1&rucg=&regInicial="

    # -- # Database connection # -- #

    db_url = Variable.get('db_url')
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()


    # -- # Drop and/or Create Table # -- #

    cur.execute("""DROP TABLE IF EXISTS productPrices""")
    conn.commit()

    cur.execute("""CREATE TABLE productPrices (
    id SERIAL PRIMARY KEY,
    code text,
    description text,
    price float,
    publicationDate date
    )""")
    conn.commit()


    # -- # Fill Table # -- #

    sql_insert = ("""
    INSERT INTO productPrices (code, description, price, publicationDate)
    VALUES (%s, %s, %s, %s)
    """)

    pags = np.arange(0,62304,100)
    print("{} pages".format(len(pags)-1))

    num_file = 1
    for idx, num in enumerate(pags[:-1]):
        print("Read products: {}".format(pags[idx+1]))
        url = base_url + str(pags[idx]+1) + "&RegFinal=" + str(pags[idx+1])
        r = requests.get(url, headers=headers)
        data = r.json()['root'][0]

        for row in data:
            row_data = []
            row_data.append(row['codigo'])
            row_data.append(row['descripcion'])
            row_data.append(str(row['precio']))
            row_data.append(str(row['fechaPublicacion']))
            cur.execute(sql_insert, row_data)

        if pags[idx+1] == 200*num_file :
            print('Commit...')
            conn.commit()
            break

    conn.close()
dag = DAG(
    'ExtractLoad',
    start_date=datetime.datetime.now(),
    schedule_interval='@daily'
)

start_operator = DummyOperator(
  task_id='Begin_execution',
  dag=dag
)

pullData_task = PythonOperator(
    task_id = 'pullData',
    python_callable=pullData,
    dag=dag
)


end_operator = DummyOperator(
  task_id='Stop_execution',
  dag=dag
)

start_operator >> pullData_task >> end_operator