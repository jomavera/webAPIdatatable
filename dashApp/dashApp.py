import os
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import psycopg2

app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )
server = app.server

# -- # Database connection # -- #
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cur = conn.cursor()


# -- # Pull data # -- #
sql = """
SELECT *
FROM productPrices
"""
df = pd.read_sql(sql, con=conn)

conn.close()

mrkd_text = '''
Data taken from [Web API](https://www.elrosado.com/Home/ListPreComisariatoInternaG). 
'''

# -- # Dash app layout # -- #
app.layout = html.Div(
    [
        html.H2([
            'Mi Comisariato prices'
        ],style={'text-align':'center'}),
        html.Div([
            dcc.Markdown(children=mrkd_text)
        ],style={'text-align':'left'}),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_current=0,
                page_size=20,
                page_action='custom',

                filter_action='custom',
                filter_query='')
        ])
    ],className='container')


# -- # Callback functions # -- #

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                return name, operator_type[0].strip(), value

    return [None] * 3

@app.callback(
    Output('table', "data"),
    Input('table', "page_current"),
    Input('table', "page_size"),
    Input('table', "filter_query"))
def update_table(page_current, page_size, filter):
    print(filter)
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)