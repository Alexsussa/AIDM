#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from common import *
import os, sys, gettext

APPANME = 'aidm'
LOCALE = os.path.abspath('/usr/share/locale')

gettext.bindtextdomain(APPANME, LOCALE)
gettext.textdomain(APPANME)
_ = gettext.gettext


class AIDM(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.font = QFont('Helvetica', 11)

        self.lbName = QLabel(_('Name'), self.central)
        self.lbName.setFont(self.font)
        self.lbName.setGeometry(20, 30, 50, 30)

        self.name_txt = QLineEdit(self.central)
        self.name_txt.setPlaceholderText(_('Type a name to application...'))
        self.name_txt.setFont(self.font)
        self.name_txt.setGeometry(70, 30, 200, 30)

        self.lbDescription = QLabel(_('Description'), self.central)
        self.lbDescription.setFont(self.font)
        self.lbDescription.setGeometry(280, 30, 100, 30)
        
        self.description_txt = QLineEdit(self.central)
        self.description_txt.setPlaceholderText(_('Type some description...'))
        self.description_txt.setFont(self.font)
        self.description_txt.setGeometry(370, 30, 300, 30)

        categories = {'AudioVideo': _('AudioVideo'), 'Development': _('Development'), 'Education': _('Education'), 'Game': _('Game'), 'Graphics': _('Graphics'), 'Network': _('Network'), 'Office': _('Office'), 'Science': _('Science'), 'Settings': _('Settings'), 'System': _('System'), 'Utility': _('Utility')}

        self.categories = QLabel(_('Categories'), self.central)
        self.categories.setFont(self.font)
        self.categories.setGeometry(20, 70, 100, 30)

        self.categories_txt = QComboBox(self.central)
        self.categories_txt.setFont(self.font)
        self.categories_txt.setGeometry(105, 70, 150, 30)
        self.categories_txt.addItems(sorted(categories.values()))

        self.appImage_txt = QLineEdit(self.central)
        self.appImage_txt.setPlaceholderText(_('Select an AppImage application...'))
        self.appImage_txt.setFont(self.font)
        self.appImage_txt.setGeometry(260, 70, 280, 30)

        self.appImage_btn = QPushButton('AppImage', self.central)
        self.appImage_btn.setFont(self.font)
        self.appImage_btn.setGeometry(550, 70, 120, 30)
        self.appImage_btn.clicked.connect(lambda: loadAppImage(self, self.appImage_txt))

        self.logo_txt = QLineEdit(self.central)
        self.logo_txt.setPlaceholderText(_('Select an image to set as application logo...'))
        self.logo_txt.setFont(self.font)
        self.logo_txt.setGeometry(105, 110, 435, 30)

        self.logo_btn = QPushButton(_('Logo'), self.central)
        self.logo_btn.setFont(self.font)
        self.logo_btn.setGeometry(550, 110, 120, 30)
        self.logo_btn.clicked.connect(lambda: loadLogo(self, self.logo_txt))

        self.bgImage = QPixmap('/usr/share/icons/hicolor/256x256/apps/aidm_bg.png')
        self.background = QLabel(self.central)
        self.background.setGeometry(130, 160, 500, 285)
        self.background.setPixmap(self.bgImage)

        self.createSc_btn = QPushButton(_('Create Shortcut'), self.central)
        self.createSc_btn.setFont(self.font)
        self.createSc_btn.setGeometry(270, 480, 150, 30)
        self.createSc_btn.clicked.connect(lambda: createShortcut(self, self.name_txt, self.description_txt, self.categories_txt, self.appImage_txt, self.logo_txt))

        self.about_btn = QPushButton(_('About'), self.central)
        self.about_btn.setGeometry(2, 545, 50, 30)
        self.about_btn.setObjectName('aboutButton')
        self.about_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.about_btn.clicked.connect(aboutAidm)

        self.lbversion = QLabel(_('Version 0.3'), self.central)
        self.lbversion.setGeometry(625, 545, 100, 30)
        self.lbversion.setObjectName('lbVersion')
        self.lbversion.setToolTip(_('Press Ctrl+J to change to dark theme'))

        # Keyboard shortcuts
        about_sc = QShortcut('Ctrl+S', self.about_btn)
        about_sc.activated.connect(aboutAidm)

        clear_sc = QShortcut('Ctrl+L', self)
        clear_sc.activated.connect(lambda: clearFields(self.name_txt, self.description_txt, self.categories_txt, self.appImage_txt, self.logo_txt))

        # Functions that need to be running at start
        self.checkTheme()

        # Keyboard shortcuts
        ct = QShortcut('Ctrl+J', self)
        ct.activated.connect(lambda: [self.changeTheme(), self.checkTheme()])


    def checkTheme(self):
        import json
        configPath = os.path.abspath(os.path.expanduser('~/.config/aidm/'))
        if not os.path.exists(configPath):
            os.makedirs(configPath)
            with open(f'{configPath}/config.json', 'w') as file:
                json.dump({'current theme': 'default'}, file, indent=4)
        with open(os.path.expanduser('~/.config/aidm/config.json'), 'r') as configFileRead:
            loadJson = json.loads(configFileRead.read())
            configFileRead.close()
            currentTheme = loadJson['current theme']
            theme = ''
            if currentTheme == 'default':
                theme = 'default.css'
            else:
                theme = 'dark.css'
            app.setStyleSheet(open(f'/usr/share/aidm/themes/{theme}', 'r').read())

    
    def changeTheme(self):
        import json
        configPath = os.path.abspath(os.path.expanduser('~/.config/aidm/'))
        configFile = os.path.join(f'{configPath}/' + 'config.json')
        with open(f'{configFile}', 'r') as configFileRead:
            loadJson = json.loads(configFileRead.read())
            configFileRead.close()
            currentTheme = loadJson['current theme']

        with open(f'{configFile}', 'w') as configFileWrite:
            themeToSave = ''
            if currentTheme == 'default':
                themeToSave = {'current theme': 'dark'}
            else:
                themeToSave = {'current theme': 'default'}
            json.dump(themeToSave, configFileWrite, indent=4)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('/usr/share/aidm/themes/default.css', 'r').read())
    translator = QTranslator()
    locale_ = QLocale().system().name()
    #library = QLibraryInfo.location(QLibraryInfo.LibraryLocation.TranslationsPath)
    library = os.path.abspath('/usr/share/aidm/translations')
    translator.load('qt_' + locale_, library)
    window = AIDM()
    window.setWindowTitle('AppImage Desktop Maker')
    window.setWindowIcon(QIcon('/usr/share/icons/hicolor/256x256/apps/aidm.png'))
    window.setFixedSize(700, 580)
    window.show()
    app.installTranslator(translator)
    sys.exit(app.exec_())
