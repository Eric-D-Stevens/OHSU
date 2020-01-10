import requests as r
import json
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

class api():

    def __init__(self, p_token, s_token=None):

        # set tokens
        self.p_token = p_token
        self.s_token = s_token
        self.base_url = 'https://cloud.iexapis.com/stable'

        # test connection, rais error if token is bad
        test_dict = {'token':self.p_token, 'symbols':'appl'}
        test = r.get(self.base_url+'/tops', test_dict)
        if not test.ok:
            raise ValueError("Bad Publishable Token.")

    def get_day(self, symbol):
        param_dict = {'token':self.p_token,'filter': 'date,volume,open,close,high,low'}
        str_ext = '/stock/{}/chart/1d'.format(symbol)
        intraday = r.get(self.base_url+str_ext, param_dict)
        print(intraday)
        print(intraday.url)
        print(json.dumps(intraday.json(), indent=4))
        js = intraday.json()
        date = [day['date'] for day in js]
        open = [day['open'] for day in js]
        close = [day['close'] for day in js]
        high = [day['high'] for day in js]
        low = [day['low'] for day in js]
        return {'dates': date,
                'opens': open,
                'closes': close,
                'highs': high,
                'lows': low}


def main():
    p_token = 'pk_23b0ae9746c642de9500a533c740e06a'
    Api = api(p_token)
    month = Api.get_day('spy')
    print(month['closes'])
    plt.plot(month['closes'])
    plt.show()


if __name__ == "__main__":
    main()
