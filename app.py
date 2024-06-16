from dotenv import load_dotenv
from src.api_openai.openai_conection import call_api
from src.db_verify import checking_data
from src.transforming import transforming
from dash.dependencies import Input, Output, State
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dash import dcc, html
import pandas as pd
import dash, time
load_dotenv()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
date_range = pd.date_range(start=datetime.now()-relativedelta(months=36),end=datetime.now())
app.layout = html.Div([
    dcc.Input(id='email', type='email', placeholder='Ingrese su correo'),
    dcc.Input(id='client', type='text', placeholder='Ingrese el monitor'),
    dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date_range.min(),
            max_date_allowed=date_range.max(),
            start_date=date_range.max()-relativedelta(months=1),
            end_date=date_range.max()),
    html.Div(id='text_info'),
    html.Div(id='title_output'),
    html.Div(id='dash_output'),
], style={'width':'100%', 'text-align':'center'})
@app.callback(
    Output('text_info', 'children'),
    Output('title_output', 'children'),
    Output('dash_output', 'children'),
    Input('email', 'value'),
    Input('client', 'value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_output(email, client, start_date, end_date): 
    if email and client:
        start_time = time.time()
        if email in ['info@info.com']:
            device_name, data = checking_data(client)
            start_date = pd.Timestamp(start_date).to_pydatetime().date()
            end_date = pd.Timestamp(end_date).to_pydatetime().date()
            html_content = call_api({'Monitor': device_name, 
                                'Data': data.describe().to_json(orient='records')}
            )
            with open(f'docs/{device_name}_informe.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            title_output, dash_output = transforming(cliente=device_name, start_date=start_date, end_date=end_date, data=data)
            execution_time = round(time.time() - start_time, 2)
            return f'Tiempo de ejecución: {execution_time}s', title_output, dash_output
        else:
            return 'Acceso denegado, verifica que sea un correo válido.', None, None
    else:
        return 'Tiempo promedio estimado en generar informe: 8s', None, None
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8051)