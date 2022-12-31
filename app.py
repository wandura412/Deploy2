# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 18:14:00 2021

@author: Dasitha Wanduragala
"""
import pandas as pd
import dash
from dash import dcc
from dash import html
#from dash.dependencies import Input, Output
import plotly.express as px
import json




app = dash.Dash(__name__)

url="https://covid.ourworldindata.org/data/owid-covid-data.xlsx"
#C:\Users\Dasitha Wanduragala\Desktop\Data science\HNDDS\Visualization\Assignment\owid-covid-data.xlsx
df=pd.read_excel(url)


dfw= df[df['location']== 'World']
Q1 = ['total_cases', 'new_cases', 'new_deaths', 'total_deaths']
Q3 = ['Sri Lanka', 'India','Bangladesh','South Africa','United States','Australia','Indonesia']
df['Test_to_detection'] = df['new_tests'] / df['new_cases']
dft=df[df['Test_to_detection'].notna()]

#
unique_continents = df['continent'].unique()

#SAAC
dfsac = df[df.location.isin(['Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Maldives', 'Nepal', 'Pakistan','Sri Lanka'])].groupby(['date'], as_index=False).sum().assign(location='SAC')  


#RoW
df2=df[~df['location'].isin(['Sri Lanka'])]
dfw1=df2[df2['location']== 'World']
dfw1['location'] = dfw1['location'].replace({'World': 'RoW'})

#Asia
dfasia=df[df['location']=='Asia']

#SL
dfsl=df[df['location']=='Sri Lanka']

#Combined
df_combined =pd.concat([dfsac,dfw1,dfasia,dfsl])


fig = px.line( x =dfw['date'], y = dfw['total_deaths'])
fig2 = px.line( x =dfw['date'], y = dfw[dfw['location']=='Sri Lanka']['total_deaths'])
fig3 = px.line( x =df['date'], y = df['Test_to_detection'])
fig4=px.scatter(x=df[df['location']=='Sri Lanka']['new_tests'] , y=df[df['location']=='Sri Lanka']['new_cases'])
fig5 = px.line( x=df['date'], y = df['reproduction_rate'],color=df['location'])




app.layout = html.Div([     
   html.H1("Covid-19 Dashboard", className='header1', id='head_id',
            style={'textAlign': 'center', 
                   'color':'#34495e'}),
        
        html.Div([
            
            
            
            #Part 01
            html.H3("1. Line chart that tracks worldwide changes ", className='header1', id='head1',
            style={'textAlign': 'left', 
                   'color':'#8A2BE2'}),
             
            dcc.Graph(id='line', figure=fig),
            html.Br(),
            
            html.Div([          
                           
            html.Label(['Select Case Type'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div([
            dcc.Dropdown(
                id='drop1',  
                options=[ {'label': 'Total Cases', 'value': 'total_cases'},
                          {'label': 'New Cases', 'value': 'new_cases'},
                          {'label': 'New Deaths', 'value': 'new_deaths'},
                          {'label': 'Total Deaths', 'value': 'total_deaths'}])],
                style=dict(width='50%')),
            
           
            html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.DatePickerRange(
                        id='dtpick',
                        min_date_allowed=df['date'].min(),                       
                        max_date_allowed=df['date'].max(),
                        style=dict(width='50%')),
            
            
            ],style={'display': 'flex', 'flex-direction': 'row'}),
            
           
            #Part 02
            
            html.Div([
            html.H3("2. Multiple  Line chart to showing the Variation of several factors", className='header2', id='head2',
            style={'textAlign': 'left', 
                   'color':'#6495ED'}),
            dcc.Graph(id='line2',figure=fig2,style=dict(width='100%')),
    
            html.Br(),  
     
            html.Div([
            html.Label(['Select Case Type'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div([
            dcc.Dropdown(
                id='drop01',  
                options=[ {'label': 'Total Cases', 'value': 'total_cases'},
                          {'label': 'New Cases', 'value': 'new_cases'},
                          {'label': 'New Deaths', 'value': 'new_deaths'},
                          {'label': 'Total Deaths', 'value': 'total_deaths'}]
                
                 )],style=dict(width='25%')),
    
           html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
           dcc.DatePickerRange(
                        id='dtpick01',
                        min_date_allowed=df['date'].min(),                       
                        max_date_allowed=df['date'].max(),style=dict(width='25%')),
    
           html.Label(['Select Location'], style={'font-weight': 'bold', "text-align": "center"}),
           dcc.Checklist(id='chk',
                  options=[
                          {'label': 'Rest of the world', 'value': 'RoW'},
                          {'label': 'Asia', 'value': 'Asia'},
                          {'label': 'SAAC', 'value': 'SAC'}
                                                               ],style=dict(width='25%')),
    
           html.Label(['Select Aggregation Method'], style={'font-weight': 'bold', "text-align": "center"}),
           html.Div([
              dcc.Dropdown(
                id='drop02',  
                options=[ {'label': 'Daily', 'value': 'd'},
                          {'label': 'Weekly Average', 'value': 'w'},
                          {'label': 'Monthly Average', 'value': 'm'},
                          {'label': '7 Day rolling Average', 'value': '7'},
                          {'label': '14 Day rolling Average', 'value': '14'}])],style=dict(width='25%'))]
                          ,style={'display': 'flex', 'flex-direction': 'row'}),
    
            
            ],style={'margin-top': '5vw'}),
            
            
            
            
            
            
            
            
            
            #Part 03
            html.Div([
            html.H3("3. Line chart to showing the daily test_to_detection ratio", className='header3', id='head3',
            style={'textAlign': 'left', 
                   'color':'#8B008B'}),
            
            dcc.Graph(id='line3', figure=fig3),
            html.Br(),
            
            html.Div([
            html.Label(['Select Case Type'], style={'font-weight': 'bold', "text-align": "center"}),
            
            html.Div([
            dcc.Dropdown(
                id='drpdwn3',  
                options=[{'label': i, 'value': i} for i in Q3])],              
                style=dict(width='50%')),
            
                
            html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div([
            dcc.DatePickerRange(
                        id='dtpick3',
                        min_date_allowed='2020-04-21',                       
                        max_date_allowed=dft['date'].max(),
                        initial_visible_month='2020-04-21',
                        start_date_placeholder_text ='2020-04-21',
                        end_date_placeholder_text='2020-05-21')] ,style=dict(width='50%')),            
           
            
            ],style={'display': 'flex', 'flex-direction': 'row'})
            
            ],style={'margin-top': '5vw'}),
            
            
            
            
            
            
            
            #part 04
            html.Div([
            html.H3("4. A scatter plot to show the relationship between Tests and new cases only for Sri Lanka", className='header4', id='head4',
            style={'textAlign': 'left', 
                   'color':'#483D8B'}),
            dcc.Graph(id='scatter',figure=fig4),
         
            html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div([
            dcc.DatePickerRange(
                        id='dtpick4',
                        min_date_allowed='2020-03-01',                       
                        max_date_allowed=dft['date'].max(),
                        initial_visible_month='2020-04-21',
                        start_date_placeholder_text ='2020-03-01',
                        end_date_placeholder_text='2020-05-21',style=dict(width='25%')),
            
            html.Label(['Correlation: '], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div(id='corr_val'),],style={'display': 'flex', 'flex-direction': 'row'})
            
            
           
            
           ],style={'margin-top': '5vw'}),
            
            #Part 05
            html.Div([
            html.H3("5. Variation of Reproduction Rate Worldwide", className='header5', id='head5',
            style={'textAlign': 'left', 
                   'color':'#4B0082'}), 
            html.Div([
            html.Label(['Pick Required Dates'], style={'font-weight': 'bold', "text-align": "center"}),
            html.Div([
            dcc.DatePickerRange(
                        id='dtpick5',
                        min_date_allowed='2020-03-29',                       
                        max_date_allowed=dft['date'].max(),
                        initial_visible_month='2020-04-21',
                        start_date_placeholder_text ='2020-03-29',
                        end_date_placeholder_text='2020-05-21',style=dict(width='25%'))]),
            
            html.Label(['Select Continent'], style={'font-weight': 'bold', "text-align": "center"}),
            
            html.Div([
            dcc.Dropdown(
                id='drpdwn5',  
                options=[{'label': i, 'value': i} for i in unique_continents])],              
                style=dict(width='25%'))],style={'display': 'flex', 'flex-direction': 'row'}),
            
             dcc.Graph(id='line5',figure=fig5),
              html.Div([
                        html.P('R0, pronounced “R naught,” is a mathematical term that indicates how contagious an infectious disease is. It’s also referred to as the reproduction number. As an infection is transmitted to new people, it reproduces itself', style={'textAlign': 'left', 
                   'color':'#34495e'}),
                     
                        html.P("R0 tells you the average number of people who will contract a contagious disease from one person with that disease. It specifically applies to a population of people who were previously free of infection and haven’t been vaccinated."
                                ,style={'textAlign': 'left', 
                             'color':'#34495e'})
    ])
            
         ],style={'margin-top': '5vw'})
                        
                        
            
          ]),
        html.H4("Created by #COHNDDS201p-006", className='headerlast', id='head_id_last',
            style={'textAlign': 'center', 
                   'color':'#34495e'}),
        
        ])

@app.callback(
    dash.dependencies.Output('line', 'figure'),
    [dash.dependencies.Input('dtpick', 'start_date')],
    [dash.dependencies.Input('dtpick', 'end_date')],
    [dash.dependencies.Input('drop1', 'value')])

def Q1(start_date,end_date,value):
    
    u = (value and start_date and end_date)
    if u is None:
        fig = px.line(dfw,x =dfw['date'], y = dfw['new_cases'],title='Worldwide Summary of variables')
        fig.update_layout(xaxis_title="Date",
                           yaxis_title= "New Cases")
        return fig
    else:
        dfd=dfw[(dfw['date']>start_date) & (dfw['date'] < end_date)]
        fig=px.line(dfd,x=dfd['date'], y= dfd[value])
        fig.update_layout(xaxis_title="Date",
                           yaxis_title= "Number of {}".format(value),
                           title='Worldwide Summary of {} '.format(value))
        return fig
    
@app.callback(
    dash.dependencies.Output('line2', 'figure'),
    [dash.dependencies.Input('dtpick01', 'start_date')],
    [dash.dependencies.Input('dtpick01', 'end_date')],
    [dash.dependencies.Input('chk', 'value')],
    [dash.dependencies.Input('drop01', 'value')],
    [dash.dependencies.Input('drop02', 'value')])

def Q2 (std,end,chkval,drpval,drpval2):
    

    u=(std and end and chkval and drpval and drpval2)

    
    if u is None:
        fig2 = px.line(x =df[df['location']== 'Sri Lanka']['date'],
                       y = df[df['location']== 'Sri Lanka']['total_deaths'],
                       title='World Wide Changes')
        fig2.update_layout(
        xaxis_title="Date",
        yaxis_title= "Total Number of Deaths")
        
        return fig2
    
    else:
        dfd=df_combined[(df_combined['date']>std) & (df_combined['date'] < end)]
        dfgrp=dfd[['date','location','total_cases', 'new_cases', 'new_deaths', 'total_deaths']]
        dfgrp['date'] = pd.to_datetime(dfgrp['date'])
        drpval2_str=str(drpval2)
        if drpval2_str == 'm' or drpval2_str== 'w' or drpval2_str== 'd' :
            dfgrp=dfgrp.groupby([
                           pd.Grouper(key='date', freq=drpval2),
                           pd.Grouper('location')]).mean().reset_index()
            
            
        else:
            drpval2_int=int(drpval2)
            dfgrp[['total_cases', 'new_cases', 'new_deaths', 'total_deaths']]=dfgrp[['total_cases', 'new_cases', 'new_deaths', 'total_deaths']].rolling(drpval2_int).mean()
            
        
        
            
    fig2 = px.line(dfgrp, x=dfgrp[dfgrp['location']== 'Sri Lanka']['date'], y=dfgrp[dfgrp['location']=='Sri Lanka'][drpval])
    for i in chkval:
        fig2.add_scatter(x=dfgrp[dfgrp['location']== i]['date'] ,y=dfgrp[dfgrp['location']==i][drpval],name=i )
            
    
    fig2.update_layout(
        title="World Wide Changes",
        xaxis_title="Date",
        yaxis_title= drpval,
        legend_title="Location")
    return fig2


@app.callback(
    dash.dependencies.Output('line3', 'figure'),
    [dash.dependencies.Input('drpdwn3', 'value')],
    [dash.dependencies.Input('dtpick3', 'start_date')],
    [dash.dependencies.Input('dtpick3', 'end_date')])

def location_filter (location,std,end):
    
    u=(location and std and end)
    
    if u is None:
        fig3 = px.line( x =df['date'], y = df['Test_to_detection'],
                        title='Test to Detection Ratios Worldwide',
                        color=df['location'])
        fig3.update_layout(
               xaxis_title="Date",
               yaxis_title= "Test to Detection ratio",
               legend_title="Location")
        
        return fig3
    
    else:
         dfl=dft[dft['location']== location]
         dfd=dfl[(dfl['date']>std) & (dfl['date'] < end)]
         fig3 = px.line(dfd, x =dfd[dfd['location']==location]['date'], 
                             y = dfd[dfd['location']==location]['Test_to_detection'],
                            title='Test to detection Ratio')
         fig3.update_layout(
               title="Test to Detection Ratios Worldwide",
               xaxis_title="Date",
               yaxis_title= "Test to Detection ratio of {} ".format(location),
               legend_title="Location")
         return fig3


@app.callback(
    dash.dependencies.Output('scatter', 'figure'),
    [dash.dependencies.Input('dtpick4', 'start_date')],
    [dash.dependencies.Input('dtpick4', 'end_date')])
    
def date_filter (std,end):
    
    u=( std and end)
    
    if u is None:
        fig4 = px.scatter(x =df[df['location']=='Sri Lanka']['new_tests'], 
                          y = df[df['location']=='Sri Lanka']['new_cases'],
                          title='New tests vs New Cases')  
        fig4.update_layout(
               xaxis_title="Date",
               yaxis_title= "Ratio")
                          
        return fig4
    
    else:
        dfd=df[(df['date']>std) & (df['date'] < end)]
        fig4 = px.scatter(dfd,x =dfd[dfd['location']=='Sri Lanka']['new_tests'], y = dfd[dfd['location']=='Sri Lanka']['new_cases'],
               title='New tests vs New Cases')  
        fig4.update_layout(
               xaxis_title="Date",
               yaxis_title= "Ratio")
               
             
        return fig4
    

@app.callback(
    dash.dependencies.Output('corr_val', 'children'),
    [dash.dependencies.Input('dtpick4', 'start_date')],
    [dash.dependencies.Input('dtpick4', 'end_date')])
    
def date_filter2 (std,end):
    
    
    u=( std and end)
    
    if u is None:
                      
        return 'Please Select Data'
    
    else:  
        dfd=df[(df['date']>std) & (df['date'] < end)]
        c=dfd['new_tests'].corr(dfd['new_cases'])              
        return u'  {} '.format(c)
        
@app.callback(
    dash.dependencies.Output('line5', 'figure'),
    [dash.dependencies.Input('drpdwn5', 'value')],
    [dash.dependencies.Input('dtpick5', 'start_date')],
    [dash.dependencies.Input('dtpick5', 'end_date')])        
        
def continent_filter (continent,std,end):
    
    u=(continent and std and end)
    
    if u is None:
        fig5 = px.line(df, x =df['date'], y = df['reproduction_rate'],
               hover_name=df['location'],
               title='Reproduction Rate Variation',
               color=df['location'])
        fig5.update_layout(xaxis_title="Date",
                           yaxis_title= "Reproduction Rate",
                           legend_title="Location")
        
        return fig5
    
    else:
         dfl=df[df['continent']== continent]
         dfd=dfl[(dfl['date']>std) & (dfl['date'] < end)]
         fig5 = px.line(dfd, x =dfd[dfd['continent']==continent]['date'], y = dfd[dfd['continent']==continent]['reproduction_rate'],
                        hover_name=dfd['location'],
                        color=dfd['location'],
                        title='Reproduction Rate Variation')
         fig5.update_layout(xaxis_title="Date",
                           yaxis_title= "Reproduction Rate of {}".format(continent),
                           legend_title="Location")
         return fig5        

    


    
    
    



if __name__ == '__main__':
    app.run_server(port=8070, debug=False)