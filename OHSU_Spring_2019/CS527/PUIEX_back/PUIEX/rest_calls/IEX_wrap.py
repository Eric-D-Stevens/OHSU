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

def get_account_metadata(api):
    param_dict = {'token': api.s_token}
    meta = r.get('{}/account/metadata'.format(api.base_url), param_dict)
    if not meta.ok:
        raise ValueError("Bad Secret Token")
    return meta.json()


def get_news(api, sym, num=1):

    url = "{}/stock/{}/news/last/{}".format(api.base_url,sym,num)
    attrs = {'token':api.p_token}
    news = r.get(url, attrs)
    print(news.url)
    if not news.ok:
        print("EPIC FAIL")
        exit()
    return news.json()



def dict_2_HTML(d):
    html = ""
    for key, val in d.items():
        html += "<b>{}:</b> &nbsp; {}<br>".format(key, val)
    return html

def list_o_dict_2_HTML(lod):
    html = ""
    for d in lod:
        html += "<p>{}</p><hr>".format(dict_2_HTML(d))
    return html

def main():
    p_token = 'pk_23b0ae9746c642de9500a533c740e06a'
    s_token = 'sk_d10d4c0690a04714b60381eb680bfb5d'
    Api = api(p_token=p_token, s_token=s_token)
    nz = get_news(Api,'spy')
    print(nz)


if __name__ == "__main__":
    main()

