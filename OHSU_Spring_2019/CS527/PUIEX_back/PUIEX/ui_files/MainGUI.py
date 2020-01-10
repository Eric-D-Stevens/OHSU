import sys

from rest_calls.IEX_wrap import *
from tab_files.user_tab import set_user
from tab_files.daily_tab import day_chart
from tab_files.news_tab import news_chart

from PyQt5.QtWidgets import *
from ui_files.Python_IEX_GUI import Ui_Python_IEX_GUI
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt
from datetime import datetime


plt.style.use('seaborn')

class MainGUI(QMainWindow, Ui_Python_IEX_GUI):

    def __init__(self):
        super(MainGUI, self).__init__()

        # USER INFO
        self.user = None
        # set up ui from designer
        self.ui = Ui_Python_IEX_GUI()
        self.ui.setupUi(self)

        # init date
        self.ui.date_in.setDate(datetime.today())

        # set up connections

        self.ui.connect_button.clicked.connect(self.set_user)

        self.ui.get_btn.clicked.connect(self.day_chart)

        self.ui.news_button.clicked.connect(self.news_chart)

        self.addToolBar(NavigationToolbar(self.ui.MplGraph.canvas, self.ui.MplGraph))

        self.ui.tabWidget.setCurrentIndex(0)



    def set_user(self):
        set_user(self)

    def day_chart(self):
        if self.user:
            day_chart(self)
        else:
            print('NO USER DECLAREDKJ')

    def news_chart(self):
        try:
            if self.user:
                news_chart(self)
        except Exception as e:
            print(e)



    def test_btn(self):


        p_token = 'pk_23b0ae9746c642de9500a533c740e06a'
        Api = api(p_token)
        sym = self.ui.sym_in.text()
        day = Api.get_day(sym)

        self.ui.MplGraph.canvas.axes.clear()
        self.ui.MplGraph.canvas.axes.plot(day['highs'], 'g')
        self.ui.MplGraph.canvas.axes.plot(day['lows'], 'r')
        self.ui.MplGraph.canvas.axes.legend(('high', 'low'), loc='upper right')
        self.ui.MplGraph.canvas.axes.set_title(sym)
        self.ui.MplGraph.canvas.draw()





app = QApplication(sys.argv)
widget = MainGUI()
widget.show()
sys.exit(app.exec_())