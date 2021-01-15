import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def getChart(
    cType='bar',
    xVals=[1,2,3,4],
    yVals=[1,2,3,4],
    color='#62B102',
    colors=['#1a5a78','#247ba3','#2e98c9','#1ca6e6','#0fb3ff'],
    cName='vals',
    fillColor='None',
    orient='None',
    xTitle='None',
    yTitle='None',
    cTitle='None',
    cMargin='None',
    autoSize=True,
    pull='None',
    titleColor='black',
    titleFontSize=22,
    cLegends='False',
    showLegend=True,
    cFill=False,
    cFillColor='#0fb3ff',
    spline=False,
    textPosition='auto',
    textSize=15,
    hole=0):

    if cType=='bar':
        fig = go.Figure(
        data=[
            go.Bar(
                marker_color=color,
                name=cName,
                x=xVals,
                y=yVals,
                orientation='v' if orient=='None' else 'h',
            )

        ],
        layout=go.Layout(
            xaxis=dict(
                title="" if xTitle=='None' else xTitle,
                titlefont=dict(
                    size=16,
                )
            ),
            yaxis=dict(
                title="" if yTitle=='None' else yTitle,
                titlefont=dict(
                    size=16,
                )
            ),
            margin=dict() if cMargin=='None' else cMargin,
        )
        )
        fig.update_layout(
            title="" if cTitle=='None' else cTitle,
            title_font_size=20,
            title_font_color=titleColor,
            autosize=autoSize,
            paper_bgcolor='white',
            plot_bgcolor='white',
        )
        return fig
    elif cType=='pie':
        fig = go.Figure(
        data=[
            go.Pie(
                hole=hole,
                labels=xVals,
                values=yVals,
                name=cName,
                pull=None if pull=='None' else pull,
                marker_colors=colors
            )],
            
        )
        fig.update_layout(
        margin=dict() if cMargin=='None' else cMargin,
        title_font_color=titleColor,
        title='' if cTitle=='None' else cTitle,
        title_font_size=titleFontSize,
        autosize=autoSize,
        showlegend=showLegend,
        # legend=dict() if cLegends=='None' else cLegends, 
        )

        fig.update_traces(
            textposition="" if textPosition=='None' else textPosition, 
            textfont_size=textSize)
        return fig
    elif cType=='line':
        fig=go.Figure(
            go.Line(
                x=xVals,
                y=yVals,
                marker_color=color,
                name=cName,
                fill=cFill,
                fillcolor=cFillColor,
                line=dict(shape='spline', smoothing=1) if spline else dict(),

            ),
            layout=go.Layout(
            xaxis=dict(
                title="" if xTitle=='None' else xTitle,
                titlefont=dict(
                    size=16,
                )
            ),
            margin=dict() if cMargin=='None' else cMargin,
            yaxis=dict(
                title="" if yTitle=='None' else yTitle,
                titlefont=dict(
                    size=16,
                )
            )
        )
        )
        fig.update_layout(
        margin=dict() if cMargin=='None' else cMargin,
        title_font_color=titleColor,
        title='' if cTitle=='None' else cTitle,
        title_font_size=titleFontSize,
        autosize=autoSize,
        legend=dict() if cLegends=='None' else cLegends, 
        )
        return fig

     