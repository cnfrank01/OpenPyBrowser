import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys

default_web_page = QUrl("https://www.baidu.com")
default_search = "https://www.baidu.com/#ie=baidu&wd=[url]"
default_font = QFont()
default_font.setFamily("SimHei")


class MainBrowser(QMainWindow):  # T
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Open Browser')
        self.setWindowIcon(QIcon('icons/logo.png'))
        self.resize(800, 500)
        self.show()
        self.setStyleSheet("""
QMainWindow{
    background:qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 rgb(225,235,255),stop:1 rgb(235,225,255));
}
QTabBar::tab
{
    min-width:100px;
    color: black;
    background-color:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1,stop: 0.3 rgb(235,245,255),stop:0.6 rgb(225,235,247),stop:1 rgb(220,234,245));
    border-top: 1px solid;
    margin-left: 0px;
    margin-right: 0px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    padding:5px;
}
 
QTabBar::tab:!selected:first
{   
    margin-top: 5px;
    border-top : 1px;
    border-left: 1px;
    border-right: 1px solid;
    border-color:rgb(200,200,200);
    border-top-left-radius: 5px;
    border-top-right-radius: 0px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}
QTabBar::tab:!selected:last
{   
    margin-top: 5px;
    border-top : 1px;
    border-left: 1px;
    border-right: 1px solid;
    border-color:rgb(200,200,200);
    border-top-left-radius: 0px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}
QTabBar::tab:!selected
{   
    margin-top: 5px;
    border-top : 1px;
    border-left: 1px;
    border-right: 1px solid;
    border-color:rgb(200,200,200);
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}
 
QTabBar::tab:selected
{   
    background-color:qlineargradient(x1: 0.5, y1: 0, x2: 0.5, y2: 1,stop: 0 rgb(240,230,255),stop: 0.7 rgb(237,250,255),stop:1 rgb(255,255,255));
    color: black;
    border-left: 1px;
    border-right: 1px solid;
    margin-left: 0px;
    margin-right: 0px;
    font-size:14px;
    border-color:rgb(160,180,215);
}
QTabBar::close-button{
    border-image:url(./icons/stop.png);
}
QTabBar QToolButton::right-arrow {
    image: url(icons/tab_right.png);  
    margin-left:2px;
}  
QTabBar QToolButton::left-arrow {
    image: url(icons/tab_left.png);  
    margin-right:2px;
}  
QTabBar{
    background:transparent;
}  
QLineEdit{
    border:0px;
    padding:5px;
    margin:0px;
	margin-left:5px;
	margin-right:5px;
	background:transparent;
	font-size:14px;
    border-bottom: 2px solid qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 rgb(255,205,255),stop: 0.7 rgb(177,197,255),stop:1 rgb(195,215,255));
    }
QToolBar{
    border:0;
    background-color:transparent;
}""")

        self.urlbar = QLineEdit()
        self.urlbar.setFont(default_font)
        self.urlbar.setMinimumHeight(28)

        self.urlbar.returnPressed.connect(self.navigate_to_url)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabShape(QTabWidget.Rounded)
        self.tabs.setFont(default_font)

        self.tabs.setTabsClosable(True)

        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.add_new_tab(default_web_page, '百度一下，你就知道')
        self.setCentralWidget(self.tabs)
        new_tab_action = QAction(QIcon('icons/add_page.png'), 'New Page', self)
        new_tab_action.triggered.connect(self.add_new_tab)

        navigation_bar = QToolBar('Navigation')

        navigation_bar.setIconSize(QSize(24, 24))
        navigation_bar.setMovable(False)
        self.addToolBar(navigation_bar)

        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        forward_button = QAction(QIcon('icons/front.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/stop.png'), 'Stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'Reload', self)
        new_button = QAction(QIcon('icons/add_page.png'), 'Add Page', self)
        back_button.triggered.connect(self.tabs.currentWidget().back)
        forward_button.triggered.connect(self.tabs.currentWidget().forward)
        stop_button.triggered.connect(self.tabs.currentWidget().stop)
        reload_button.triggered.connect(self.tabs.currentWidget().reload)
        new_button.triggered.connect(self.add_new_tab_default)

        navigation_bar.addAction(back_button)
        navigation_bar.addAction(forward_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)
        navigation_bar.addSeparator()
        navigation_bar.addAction(new_button)

        self.tabs.currentWidget().page().profile().downloadRequested.connect(self.downloadRequested)

    def downloadRequested(self, item):
        self.set
        item.accept()

    def navigate_to_url(self):
        if (self.urlbar.text().find('.') == -1):
            current_url = QUrl(default_search.replace("[url]", self.urlbar.text()))
        else:
            current_url = QUrl(self.urlbar.text())
            if current_url.scheme() == '':
                current_url.setScheme('http')
        self.tabs.currentWidget().load(current_url)

    def renew_urlbar(self, url, browser=None):

        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(url.toString())
        self.urlbar.setCursorPosition(0)
        self.browser.loadFinished.connect(
            lambda _, i=self.tabs.currentIndex(), browser=self.browser: self.tabs.setTabText(i,
                                                                                             self.browser.page().title()))

    def add_new_tab_by_webview(self, webview, label='Blank'):

        self.browser = webview

        i = self.tabs.addTab(self.browser, label)
        self.tabs.setCurrentIndex(i)
        self.browser.urlChanged.connect(lambda qurl, browser=self.browser: self.renew_urlbar(qurl, self.browser))
        self.browser.setFont(default_font)

        self.browser.loadFinished.connect(
            lambda _, i=i, browser=self.browser: self.tabs.setTabText(i, self.browser.page().title()))

    def add_new_tab_default(self):
        if (self.tabs.currentWidget().url() == QUrl.fromLocalFile(os.path.abspath('.') + "/main.html")):
            self.urlbar.setText(default_web_page.url())
            self.navigate_to_url()
            return
        self.browser = WebEngineView(self)
        self.browser.load(QUrl(default_web_page))

        i = self.tabs.addTab(self.browser, "Default")
        self.tabs.setCurrentIndex(i)
        self.browser.urlChanged.connect(lambda qurl, browser=self.browser: self.renew_urlbar(qurl, self.browser))
        self.browser.setFont(default_font)
        self.browser.loadFinished.connect(
            lambda _, i=i, browser=self.browser: self.tabs.setTabText(i, self.browser.page().title()))

    def add_new_tab(self, qurl=QUrl(''), label='Blank'):

        self.browser = WebEngineView(self)
        self.browser.load(qurl)

        i = self.tabs.addTab(self.browser, label)
        self.tabs.setCurrentIndex(i)
        self.browser.urlChanged.connect(lambda qurl, browser=self.browser: self.renew_urlbar(qurl, self.browser))
        self.browser.setFont(default_font)
        self.browser.loadFinished.connect(
            lambda _, i=i, browser=self.browser: self.tabs.setTabText(i, self.browser.page().title()))

    def tab_open(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.renew_urlbar(qurl, self.tabs.currentWidget())

    def close_current_tab(self, i):

        if self.tabs.count() < 2:
            if self.tabs.currentWidget().url() == QUrl.fromLocalFile(os.path.abspath('.') + "/main.html"):
                quit()
            else:
                self.add_new_tab(QUrl.fromLocalFile(os.path.abspath('.') + "/main.html"))
        self.tabs.removeTab(i)


class WebEngineView(QWebEngineView):

    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.add_new_tab_by_webview(new_webview)
        return new_webview


if __name__ == '__main__':
    BrowserApp = QApplication(sys.argv)
    BrowserWin = MainBrowser()
    BrowserWin.show()
    BrowserApp.exec_()
