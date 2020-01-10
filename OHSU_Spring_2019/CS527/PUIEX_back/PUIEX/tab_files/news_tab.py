from rest_calls.IEX_wrap import api
from rest_calls.IEX_wrap import get_news
from rest_calls.IEX_wrap import dict_2_HTML, list_o_dict_2_HTML

def news_chart(GUI):
    try:
        sym = GUI.ui.news_sym.text()
        num = GUI.ui.num_stories.value()

        list_o_dict = get_news(GUI.user, sym, num)
        html = list_o_dict_2_HTML(list_o_dict)
        print(html)
        GUI.ui.news_browser.setHtml(html)
    except Exception as e:
        print(e)
