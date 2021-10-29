#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os, gettext, webbrowser

APPANME = 'aidm'
LOCALE = os.path.abspath('locale')

gettext.bindtextdomain(APPANME, LOCALE)
gettext.textdomain(APPANME)
_ = gettext.gettext


def loadAppImage(self, load):
    file = QFileDialog.getOpenFileName(self, 'Open AppImage file', os.path.expanduser('~/'), 'AppImage (*.AppImage *.Appimage *.appImage *.appimage)', options=QFileDialog.DontUseNativeDialog)
    load.setText(file[0])


def loadLogo(self, load):
    file = QFileDialog.getOpenFileName(self, _('Open Image file'), os.path.expanduser('~/'), 'Images (*.jpg *.jpeg *.svg *.png)', options=QFileDialog.DontUseNativeDialog)
    load.setText(file[0])


def createShortcut(self, name, desc, categ, file, image):
    prefix_appImage = '.AppImage', '.Appimage', '.appImage', '.appimage'

    prefix_images = '.jpg', '.jpeg', '.svg', '.png'

    categories = {'AudioVideo': _('AudioVideo'), 'Development': _('Development'), 'Education': _('Education'), 'Game': _('Game'), 'Graphics': _('Graphics'), 'Network': _('Network'), 'Office': _('Office'), 'Science': _('Science'), 'Settings': _('Settings'), 'System': _('System'), 'Utility': _('Utility')}

    if name.text() == '' or desc.text() == '' or categ.currentText() == '' or file.text() == '' or image.text() == '':
        QMessageBox.information(self, _('Information'), _('Fill all fields before click on create shortcut button.'), QMessageBox.StandardButton(1))

    elif not str(file.text()).endswith(tuple(prefix_appImage)):
        QMessageBox.information(self, _('Information'), _('You need to choose a valid .AppImage file.'), QMessageBox.StandardButton(1))

    elif not str(image.text()).endswith(tuple(prefix_images)):
        QMessageBox.information(self, _('Information'), _('You need to choose a valid image file.'), QMessageBox.StandardButton(1))

    else:
        categ_ = ''
        for k, v in categories.items():
            if categ.currentText() == v:
                categ_ = k
        saveDesktop = open(os.path.expanduser(f'~/.local/share/applications/{name.text()}.desktop'), 'w')
        saveDesktop.write("#!/usr/bin/env xdg-open\n")
        saveDesktop.write("[Desktop Entry]\n")
        saveDesktop.write("Version=1.0\n")
        saveDesktop.write("Type=Application\n")
        saveDesktop.write("Terminal=false\n")
        saveDesktop.write(f"Name={name.text()}\n")
        saveDesktop.write(f"GenericName={name.text()}\n")
        saveDesktop.write(f"Comment={desc.text()}\n")
        saveDesktop.write(f"Icon={image.text()}\n")
        saveDesktop.write(f'Exec="{file.text()}"\n')
        saveDesktop.write(f"Categories=Qt;{categ_};\n")
        saveDesktop.write(f"Keywords={name.text()}")
        saveDesktop.close()

        #localpath = os.path.expanduser('~/.local/share/applications')
        #os.system(f'mv {name}.desktop {localpath}')

        QMessageBox.information(self, _('Information'), _('Desktop AppImage shortcut created successfully. Now your application can be found in application menu.'), QMessageBox.StandardButton(1))

        clearFields(name, desc, categ, file, image)


def clearFields(name, desc, categ, file, image):
    name.setText('')
    desc.setText('')
    categ.setCurrentIndex(0)
    file.setText('')
    image.setText('')


def aboutAidm():
    popup = QDialog()
    popup.setWindowTitle(_('About AIDM'))
    popup.setFixedSize(500, 590)

    bg_img = QPixmap('icons/aidm.png')
    lb_bg = QLabel('', popup)
    lb_bg.setGeometry(100, 0, 500, 285)
    lb_bg.setPixmap(bg_img)

    version = QLabel('v0.2', popup)
    version.setGeometry(250, 300, 100, 30)

    gh = QCommandLinkButton(_('Source Code'), popup)
    gh.setGeometry(202, 320, 110, 30)
    gh.setStyleSheet('color: blue; border: None;')
    gh.setCursor(QCursor(Qt.PointingHandCursor))
    gh.clicked.connect(lambda: webbrowser.open('https://github.com/Alexsussa/AIDM'))

    license_ = QLabel(_('License MIT'), popup)
    license_.setGeometry(233, 340, 120, 30)

    copying = open('COPYING', 'r').read()
    license_txt = QTextEdit(popup)
    license_txt.setGeometry(5, 370, 490, 210)
    license_txt.setText(copying)
    license_txt.setReadOnly(True)

    popup.exec_()
    #sys.exit(popup.exec_())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    #aboutAidm()
    sys.exit(app.exec_())
