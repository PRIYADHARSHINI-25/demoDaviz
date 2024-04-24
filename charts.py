from flask import render_template
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
# from highcharts_core.options.series.line import LineSeries
from highcharts_core.options.series.bar import BarSeries
import json

import pandas as pd
from io import StringIO

def preproces(data):
    data_str=data.decode('utf-8-sig')
    data_io=StringIO(data_str)

    df=pd.read_csv(data_io)
    charts=chart(df)
    return(charts)

def chart(df):
    mychart=Chart.from_pandas(df,
                              property_map={'x':'Name',
                                            'y':'Class'},
                              series_type='bar',
                              chart_kwargs = {'container': 'target_div',
                                              'variable_name': 'myChart'
  })
    chart=mychart.to_js_literal()
    return(chart)
