# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django import template
from django.template import loader



@login_required(login_url="/login/")
def index(request):
    return render(request,'dashboard/index.html')

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('dashboard/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('dashboard/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('dashboard/page-500.html')
        return HttpResponse(html_template.render(context, request))



# Pandas function to get the csv value
from collections import OrderedDict
from apps.dashboard.fusioncharts import FusionCharts
import pandas as pd

path = "./common/util/DataFile/company_list_state_classified.csv"
path2 = "./common/util/DataFile/df_companies_state.csv"
df = pd.read_csv(path, index_col=None)

df_companies_state = df.groupby("company_state").agg(
    total_companies=("company_state", "count")).reset_index()

df_companies_state = df_companies_state.sort_values(
    by=['total_companies'], ascending=False)
    
# Pandas function to modify csv value to generate map data
## For mapn chart
df_companies_state_id = pd.read_csv(path2, index_col=None)

df_companies_state_id["id"] = df_companies_state_id["id"].apply(lambda x : "00" + str(x) if x < 10 else "0" + str(x))
df_companies_state_id["total_companies"] = df_companies_state_id["total_companies"].apply(lambda x : str(x))
df_companies_state_id["value_label"] = "1"

x = [id for id in df_companies_state_id["id"]]
x2 =  [value for value in df_companies_state_id["total_companies"]]
x3 = [value for value in df_companies_state_id["value_label"]]

mapArray = list(map(list,zip(x,x2,x3)))

@login_required(login_url="/login/")
def dashboard(request):

    # Chart 1
    dataSource = OrderedDict()
    chartConfig = OrderedDict()

    chartConfig["caption"] = "Malaysia's state with total companies"
    chartConfig["subCaption"] = "Source from Jobstreet"
    chartConfig["xAxisName"] = "State"
    chartConfig["yAxisName"] = "Companies"

    chartConfig["theme"] = "fusion"

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    for state, value in zip(df_companies_state["company_state"], df_companies_state["total_companies"]):
        dataSource["data"].append({"label": state, "value": value})

    # Chart 2
    dataSourceMap = OrderedDict()

    mapConfig = OrderedDict()
    mapConfig["animation"] = "0"
    mapConfig["usehovercolor"] = "1"
    mapConfig["showlegend"] = "1"
    mapConfig["legendposition"] = "BOTTOM"
    mapConfig["legendborderalpha"] = "0"
    mapConfig["legendbordercolor"] = "#ffffff"
    mapConfig["legendallowdrag"] = "0"
    mapConfig["legendshadow"] = "0"
    mapConfig["caption"] = "Malaysia's state with total companies"
    mapConfig["subCaption"] = "Source from Jobstreet"
    mapConfig["connectorcolor"] = "000000"
    mapConfig["fillalpha"] = "80"
    mapConfig["hovercolor"] = "CCCCCC"
    mapConfig["theme"] = "fusion"

    colorDataObj = {
        "minvalue": "0",
        "code": "#FFE0B2",
        "gradient": "1",
        "color": [{
            "minValue": "0",
            "maxValue": "1000",
            "code": "#6497b1"
        }, {
            "minValue": "1000",
            "maxValue": "2000",
            "code": "#005b96"
        }, {
            "minValue": "2000",
            "maxValue": "3000",
            "code": "#03396c"
        }, {
            "minValue": "3000",
            "maxValue": "4000",
            "code": "#011f4b"
        }
        ]
    }

    dataSourceMap["chart"] = mapConfig
    dataSourceMap["colorrange"] = colorDataObj
    dataSourceMap["data"] = []

    # Map data array
    mapDataArray = mapArray

    for i in range(len(mapDataArray)):
      dataSourceMap["data"].append({
          "id": mapDataArray[i][0],
          "value": mapDataArray[i][1],
          "showLabel": mapDataArray[i][2]
      })


    column2D = FusionCharts("column2d", "myFirstChart", "800",
                            "600", "myFirstchart-container", "json", dataSource)
    fusionMap = FusionCharts("maps/malaysia", "myFirstMap", "800",
                            "600", "mySecondchart-container", "json", dataSourceMap)

    return render(request, 'dashboard/dashboard.html', {
        'output': column2D.render(),    
        'output2': fusionMap.render(),
    })