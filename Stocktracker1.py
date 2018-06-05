import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime
import pandas as pd
import dash_table_experiments as dt
import plotly
import json
import plotly.graph_objs as go
import copy
import math
import numpy as np
import glob
import os



app = dash.Dash()

#adding Nasdaq list to the stock picker dropdown
nsdq = pd.read_csv('data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

# Retrieving saved DATA

list_of_files = glob.glob('sample_files/*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
#print(latest_file)
def cleanup(list_of_files):
    for file in list_of_files:
        if file == latest_file:
            pass
        else:
            os.remove(file)

cleanup(list_of_files)

#list_of_target_files = glob.glob('targets/*.csv') # * means all if need specific format then *.csv
#latest_target_file = max(list_of_target_files, key=os.path.getctime)
#print(latest_target_file)
#saved_targets= pd.read_csv(latest_target_file)
#current_target = saved_targets.target[0]
#print(current_target)


DF_SIMPLE = pd.read_csv(latest_file)
#newcompany = pd.DataFrame({
#'Balance':[0],
#'Name':['Add'],
#'Shares':[0],
#'Ticker':['Add'],
#'balance':[0],
##'close':[0]
#})
#DF_SIMPLE = DF_SIMPLE.append(newcompany)




app.layout = html.Div([
    # Row 1: Header and Intro text

    html.Div([
        html.Img(src="https://static.seekingalpha.com/uploads/2018/1/7/48200183-15153603846257193_origin.jpg",
                style={
                    'height': '50px',
                    'float': 'right',
                    'position': 'relative',
                    'top':'0px',
                    'bottom': '0px',
                    'left': '0px'
                },
                ),
        html.H2('Dash',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '20px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '4.0rem',
                    'color': '#4D637F'
                }),

        html.H2('Investment Report',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '37px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '4.0rem',
                    'color': '#4D637F'
                }),
    ], className='container', style={'padding':'0px','position': 'relative', 'right': '5px', 'width':'100%', 'color':'#fff'}),


html.P('This report reviews the current price of the FANG (Facebook, Amazon, Netflix and Google) stocks', style={
    'position': 'relative',
    'top': '20px',
    'bottom': '20px',
    'left': '20px',
    'font-family': 'Dosis',
    'display': 'block',
    'font-size': '1.5rem',
    'color': '#4D637F'
}),


    html.Div([
    html.Div([


 html.Div([
        html.H4('Add a stock symbol:', style={
            'position': 'relative',
            'top': '0px',
            'left': '27px',
            'font-family': 'Dosis',
            'display': 'inline',
            'font-size': '2.0rem',
            'color': '#4D637F'
        }),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value=['FB', 'GOOG', 'AMZN', 'NFLX'],
            multi=True
        )
    ], style={
        'position': 'relative',
        'top': '0px',
        'left': '27px',
        'font-family': 'Dosis',
        'display': 'inline',
        'font-size': '2.0rem',
        'color': '#4D637F'
    }),
    html.Div([
        html.H3('Select start and end dates:',style={
            'position': 'relative',
            'top': '0px',
            'left': '20px',
            'font-family': 'Dosis',
            'display': 'inline',
            'font-size': '2.0rem',
            'color': '#4D637F'
        }),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2018, 1, 1),
            end_date=datetime.today()
        )
    ], style={
        'position': 'relative',
        'top': '0px',
        'left': '27px',
        'font-family': 'Dosis',
        'display': 'inline',
        'font-size': '2.0rem',
        'color': '#4D637F'
    }),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '27px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '1.5rem',
                'color': '#4D637F'
            }),
    ]),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
    ],className="four columns", style={'display':'inline-block',  'verticalAlign':'top', 'width':'40%'}),
 html.Div([

         html.H4('Add your investment goal', style={
             'position': 'relative',
             'top': '0px',
             'left': '20px',
             'font-family': 'Dosis',
             'display': 'inline',
             'font-size': '2.0rem',
             'color': '#4D637F'
         }),
         html.Br(),
         dcc.Input(
         placeholder='Enter a value...',
         type='text',
         value=1000000,
         id='goal',
         style={'position': 'relative','left':'20px'},

         ),
         html.Button('Update goal', id='button', style={'position': 'relative','left':'30px'}),
                    dcc.Graph(
                        id = "Goal",
                        style={'position': 'relative'}

                    )
], className="six columns", style={'display':'inline-block',  'width':'50%'}),

    ], className="row", style={'top':'10px'}),


    html.Div([
    html.H4('Portfolio - update shares to get current balance',style={
        'position': 'relative',
        'top': '0px',
        'left': '27px',
        'font-family': 'Dosis',
        'display': 'block',
        'font-size': '2.0rem',
        'color': '#4D637F'
    }),
            html.Div(
            children=dt.DataTable(
                rows=DF_SIMPLE.to_dict('records'),
                columns=['Name', 'Ticker','Shares', 'Balance'],
                editable=True,
                id='table'

            ),
            className='six columns',
        ),
        #html.Pre(id='output1', className='six columns'),

    html.Div([
        #html.Pre(id='update_graph', className='two columns'),
        html.Div(
            dcc.Graph(
                id='new graph',
                style={
                    'overflow-x': 'wordwrap'
                }
            ),
            className='six columns'
        )
    ], className='row'),

    html.Pre(id='output1', className='six columns'),
],)
    ], className='container')








#Goal graph_objs

@app.callback(
    Output('Goal', 'figure'),
    [Input('button', 'n_clicks')],
    [State('table', 'rows'),
     State('goal', 'value')],

    )
def goal_graph(n_clicks,rows,goal):
    df1 = pd.DataFrame(rows)
    total = df1['Balance'].sum()
    #target = current_target
    target = int(goal)
    remainder = target - total
    #df2 = pd.DataFrame(columns=['target'])
    #df2 = df2.append([{'target':target}], ignore_index=True)
    #print(df2['target'])
    #filename=datetime.now().strftime("targets/%Y-%m-%d-%H-%M-%S-%f"+".csv")
    #df2.to_csv(filename,index=False)
    #print (total)
    #fig = {
        #'data': [{'x':['Balance'],
        #        'y':[total],
        #        'type':'bar'},
        #    ],

        #'layout': {'title':''}
    #}
    fig = {
      "data": [
        {
          "values": [total, remainder],
          "labels": [
            "Amt Saved",
            "Amt Remaining",

          ],
          "domain": {"x": [0, 1.0]},
          "name": "",
          "hoverinfo":"label+percent+name+value",
          "hole": .5,
          "type": "pie"
        },
    ],
      "layout": {
            "title":"Progress Report",
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "",
                    "x": 0.20,
                    "y": 0.5
                },

            ]
        }
    }
    return fig


#Code for line graph
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic,'iex',start,end)
        traces.append({'x':df.index, 'y': df.close, 'name':tic})
    fig = {
        'data': traces,
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig







#New Fig

@app.callback(
    Output('new graph', 'figure'),
    [Input('table', 'rows')],
    )
def update_figure(rows):
    dff = pd.DataFrame(rows)
    stock_ticker = (dff['Ticker'])
    shares = (dff['Shares'])
    start = datetime(2018, 5, 24)
    end = datetime.now()
    traces = []
    for tic in stock_ticker:
        if tic == "Add":
            pass
        else:
            df1 = web.DataReader(tic,'iex',start,end)
            traces.append({'x':tic, 'y': df1.close[-1], 'type':'bar', 'name':tic})
    df2 = pd.DataFrame(traces)
    dff['close']=df2.y
    dff.Shares = dff.Shares.astype(float)
    dff['balance']=dff['close']*dff['Shares']
    filename=datetime.now().strftime("sample_files/%Y-%m-%d-%H-%M-%S-%f"+".csv")
    dff.to_csv(filename,index=False)

    fig = {
        'data': [{'x':dff['Name'],
                'y':dff['balance'],
                 'marker' :dict(
        color=['rgba(209,185,154,0.8)', 'rgba(90, 38, 223,0.8)',
               'rgba(223, 90, 38,0.8)', 'rgba(222,45,38,0.8)',
               'rgba(38, 216, 223,0.8)','rgba(38, 223, 90,0.8)']),
                'type':'bar'},
                ],
        'layout': {'title':'Balance based on closing price'}
    }
    return fig

def getclose (ticker):
    start = datetime(2018, 5, 24)
    end = datetime.now()
    stock_data = web.DataReader(ticker,'iex',start,end)
    close = stock_data['close'][-1]
    return close

@app.callback(
    Output('table', 'rows'),
    [Input('table', 'row_update')],
    [State('table', 'rows')])
def update_rows(row_update, rows):
    row_copy = copy.deepcopy(rows)
    dff = pd.DataFrame(row_copy)
    if row_update:
        updated_row_index = row_update[0]['from_row']
        ticker = dff['Ticker'][updated_row_index]
        updated_value = list(row_update[0]['updated'].values())
        updated_value= updated_value[0]
        update_balance = getclose(ticker) * float(updated_value)
        update_balance = math.floor(update_balance)
        row_copy[updated_row_index]['Balance'] = update_balance
    return row_copy


#@app.callback(
#    Output('table1','rows'),
#    [Input('button', 'n_clicks')],
#    [State('output-container-button', 'children')])
#def addNewCo(n_clicks, newcompany):
#    print(newcompany)



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]


for css in external_css:
    app.css.append_css({"external_url": css})




if __name__ == '__main__':
    app.run_server(debug=True)
