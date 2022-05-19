import subprocess
import sys
import webbrowser
import requests
import getpass
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import chromedriver_autoinstaller
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore


def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        chromedriver_autoinstaller.install()
        super(Login, self).__init__(parent)
        self.textDomain = QtWidgets.QLineEdit(self)
        self.textDomain.setPlaceholderText("비즈니스 계정")
        self.logo = QtWidgets.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap(resource_path("img/clair_logo.png")))
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.textName = QtWidgets.QLineEdit(self)
        self.textName.setPlaceholderText("ID")
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setPlaceholderText("Password")
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.setWindowTitle("Clair - reomoteView")
        self.setFixedWidth(400)
        self.setFixedHeight(300)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.logo)
        layout.addWidget(self.textDomain)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        '''
        리모트뷰 자동로그인
        '''

        # j_domain 대표아이디
        # j_username 아이디
        # j_password 비밀번호

        options = webdriver.ChromeOptions()
        options.add_argument('--start-fullscreen')


        # browser size
        # opstions.add_argument('window-size=800,600')

        user_domain = self.textDomain.text()
        user_id = self.textName.text()
        user_pw = self.textPass.text()

        # driver path
        driver = webdriver.Chrome(options=options)

        # connect browser with url
        driver.get('https://www.rview.com/ko/')

        # connect time
        driver.implicitly_wait(3)

        driver.find_element_by_id('j_domain').send_keys(user_domain)
        driver.find_element_by_id('j_username').send_keys(user_id)
        driver.find_element_by_id('j_password').send_keys(user_pw)
        driver.find_element_by_id('submit-btn').submit()

        driver.implicitly_wait(5)

        driver.find_element_by_id('dialog-close').click()

        driver.implicitly_wait(30)

        pc_list = driver.find_elements_by_class_name('c-rpas__item')

        for i in range(len(pc_list)):
            if pc_list[i].find_element_by_class_name('rpa__title').text == '클레어':
                print("execute remotepc")
                pc_list[i].find_element_by_class_name('rpa-box__opener').click()
                driver.implicitly_wait(5)
                list = pc_list[i].find_elements_by_class_name('ui-vertical-menu__item')
                for j in range(len(list)):
                  if list[j].text == "웹뷰어 제어":
                    print("success!!")
                    list[j].click()
                    print(driver.window_handles)
                    time.sleep(1.5)
                    break
                break

        print(driver.window_handles)
        driver.switch_to.window(driver.window_handles[-1])

        driver.find_element_by_name('id').send_keys(user_id)
        driver.find_element_by_name('password').send_keys(user_pw)
        driver.find_element_by_xpath('//*[@id="root"]/div/div/button[1]').click()

        while True:
          pass

            

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())