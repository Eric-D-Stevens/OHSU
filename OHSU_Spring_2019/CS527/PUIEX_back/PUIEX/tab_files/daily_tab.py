import json
import requests as r


def day_chart(GUI):
    symbol = GUI.ui.sym_in.text()
    param_dict = {'token':GUI.user.p_token,'filter': 'date,volume,open,close,high,low'}
    str_ext = '/stock/{}/chart/1d'.format(symbol)
    intraday = r.get(GUI.user.base_url+str_ext, param_dict)
    print(intraday)
    print(intraday.url)
    print(json.dumps(intraday.json(), indent=4))
    js = intraday.json()
    date = [day['date'] for day in js]
    open = [day['open'] for day in js]
    close = [day['close'] for day in js]
    high = [day['high'] for day in js]
    low = [day['low'] for day in js]
    day = {'dates': date,
           'opens': open,
           'closes': close,
           'highs': high,
           'lows': low}

    GUI.ui.MplGraph.canvas.axes.clear()
    GUI.ui.MplGraph.canvas.axes.plot(day['highs'], 'g')
    GUI.ui.MplGraph.canvas.axes.plot(day['lows'], 'r')
    GUI.ui.MplGraph.canvas.axes.legend(('high', 'low'), loc='upper right')
    GUI.ui.MplGraph.canvas.axes.set_title(symbol)
    GUI.ui.MplGraph.canvas.draw()

