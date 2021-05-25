import plotly.graph_objects as go
import math

def plotly_bullet(probability):
    if probability < 0.00001:
        graph_start = 0
        upper_cutoff = 0.00001
        lower_cutoff = 0
    elif probability < 0.01:
        graph_start = 0.2
        upper_cutoff = 0.01
        lower_cutoff = 0.00001
    elif probability < 0.1:
        graph_start = 0.4
        upper_cutoff = 0.1
        lower_cutoff = 0.01
    elif probability < 5:
        graph_start = 0.6
        upper_cutoff = 5
        lower_cutoff = 0.1
    else:
        graph_start = 0.8
        upper_cutoff = 100
        lower_cutoff = 5
    scaled = (probability - lower_cutoff) / (upper_cutoff - lower_cutoff)
    log_scaled = math.log((1+scaled), 2)
    bullet_value = graph_start + (0.2 * log_scaled)


        
    fig = go.Figure(go.Indicator(
        mode = "gauge",
        value = bullet_value,
        #title = {'text': "Risk Level", 'font': {"size": 12,'color':'black'}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'shape': "bullet",
                 'bgcolor': 'white',
                  'bar': {'color': "black"},
                 'axis':{'range': [None, 1],
                          'tickmode':'array',
                         'tickvals':[0.2,0.4,0.6, 0.8,1],
                         'ticktext':['0.00001%','0.01%','0.1%','5%','100%'],
                         'tickfont':{'color':'black'}},
                'steps': [
                {'range': [0, 0.2], 'color': '#2FCC71', 'name':'Very Low Risk'},
                {'range': [0.2, 0.4], 'color': '#1F8449', 'name':'Low Risk'},
                {'range': [0.4, 0.6], 'color': '#F4D03F', 'name':'Medium Risk'},
                {'range': [0.6, 0.8], 'color': '#F5B041', 'name':'High Risk'},
                {'range': [0.8, 1], 'color': '#C03A2B', 'name':'Very High Risk'}],}
    ))
    fig.update_layout({'plot_bgcolor':'white',
                       'paper_bgcolor':'white'})
    fig.add_annotation(
        x=0.9,
        y=0.9,
        xanchor='center',
        yanchor='middle',
        text="Very High Risk",
        hovertext='Hover',
        showarrow=False,
        font=dict(
                    color="black",
                    size=14
                )
    )
    fig.add_annotation(
        x=0.7,
        y=0.9,
        xanchor='center',
        yanchor='middle',
        text="High Risk",
        showarrow=False,
        font=dict(
                    color="black",
                    size=14
                )
    )
    fig.add_annotation(
        # The arrow head will be 25% along the x axis, starting from the left
        x=0.5,
        y=0.9,
        xanchor='center',
        yanchor='middle',
        text="Medium Risk",
        showarrow=False,
        font=dict(
                    color="black",
                    size=14
                )
    )
    fig.add_annotation(
        x=0.5,
        y=1.8,
        xanchor='center',
        yanchor='middle',
        text=f"Individual Risk Level: {probability:.4f}%",
        showarrow=False,
        font=dict(
                    color="black",
                    size=20
                )
    )    
    fig.add_annotation(
        x=0.3,
        y=0.9,
        xanchor='center',
        yanchor='middle',
        text="Low Risk",
        showarrow=False,
        font=dict(
                    color="black",
                    size=14
                )
    )
    fig.add_annotation(
        x=0.1,
        y=0.9,
        xanchor='center',
        yanchor='middle',
        text="Very Low Risk",
        showarrow=False,
        font=dict(
                    color="black",
                    size=14
                )
    )
    return fig
