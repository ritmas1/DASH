

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash_table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#PLEASE CHANGE HERE THE PATH TO FILE df_dashboard.xlsx ON YOUR PC

path='/Users/margaritavenediktova/Desktop/tasks/df_dashboard.xlsx'


df= pd.read_excel(path)
df=df.drop(columns={'Unnamed: 0'})


available_payers = df['payer'].unique()
available_service= df['service_category'].unique()
available_claims= df['claim_specialty'].unique()

app.layout = app.layout = html.Div([
    html.Div([

        html.Div([ html.Label(['Payer']),dcc.Dropdown(
                id='filter_payer',
                options=[{'label': i, 'value': i} for i in available_payers],
                value='Payer F', 
                multi=True)
                
            ],   
        style={'width': '30%'}),
            
        html.Div([html.Label(['Service Category']),
            dcc.Dropdown(
                id='filter_service',
                options=[{'label': i, 'value': i} for i in available_service],
                value='AncillaryFFS',
                multi=True)
        ], style={'width': '30%'}),
        html.Div([html.Label(['Claim']),
            dcc.Dropdown(
                id='filter-claim',
                options=[{'label': i, 'value': i} for i in available_claims],
                value='pathology',
                multi=True)
        ], style={'width': '30%'}),
     
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '5px 5px'
    }),
        html.Div([

            html.Div([
                dcc.Graph(
                    id='scatter'
                )
            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
            
            html.Div([
                dash_table.DataTable(
                    id='table',
                    data=df.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    fixed_rows={'headers': True},
                    style_table={'height': 350}
                    )
                ],style={'width': '49%', 'float': 'right','display': 'inline-block', 'padding': '0 20'})
            ]),
    
    html.Div(dcc.Slider(
        id='year--slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].max(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
     
    
])
    
        
@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('filter_payer', 'value'),
     dash.dependencies.Input('filter_service', 'value'),
     dash.dependencies.Input('filter-claim', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(payer,service, claim,year_value):
    
    dff=df[df['year'] == year_value]
    
    if type(payer)==str:
        payer=[payer]
    if type(service)==str:
        service=[service] 
    if type(claim)==str:
        claim=[claim]
        
    
    fig = px.scatter(x=dff['month'].unique(),
            y=dff[(dff['payer'].isin(payer))&
                 (dff['service_category'].isin(service))&
                 (dff['claim_specialty'].isin(claim))].groupby(['month']).sum()['paid_amount'])
    fig.update_xaxes(title='Month')

    fig.update_yaxes(title='Paid Amount')
    
    return fig


@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('filter_payer', 'value'),
     dash.dependencies.Input('filter_service', 'value'),
     dash.dependencies.Input('filter-claim', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_table(payer,service, claim,year_value):
    
    if type(payer)==str:
        payer=[payer]
    if type(service)==str:
        service=[service] 
    if type(claim)==str:
        claim=[claim]
        
    y=df[(df['payer'].isin(payer))&
          (df['service_category'].isin(service))&
                 (df['claim_specialty'].isin(claim))&
                 (df['year']==year_value)]
    return y.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)

