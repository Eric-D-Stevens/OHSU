from rest_calls.IEX_wrap import api
from rest_calls.IEX_wrap import get_account_metadata, dict_2_HTML
from PyQt5 import QtCore
_translate = QtCore.QCoreApplication.translate

def set_user(GUI):
    pk = GUI.ui.p_token.text()
    sk = GUI.ui.s_token.text()
    print(pk)
    print(sk)

    usr = None
    try:
        usr = api(p_token=pk, s_token=sk)
        meta_dict = get_account_metadata(usr)
        for key, val in meta_dict.items():
            print("{}:  {}".format(key, val))
        meta_html = dict_2_HTML(meta_dict)

        GUI.ui.connection_status.setStyleSheet('font: 75 18pt \"MS Shell Dlg 2\";\n; color: green')
        GUI.ui.connection_status.setText('CONNECTION SUCCESS')
        GUI.user = usr
        GUI.ui.connection_browser.setHtml(meta_html)

    except:
        print('EXCEPTION RAISED')
        GUI.ui.connection_status.setText('CONNECTION FAILED: bad token(s)')
        GUI.ui.connection_status.setStyleSheet('font: 75 18pt \"MS Shell Dlg 2\";\n; color: red')
        fail_string = "<h3>Please double check both of your tokens as the ..." \
                      "connection process will fail unless both tokens are correct</h3>"
        GUI.ui.connection_browser.setHtml(fail_string)




