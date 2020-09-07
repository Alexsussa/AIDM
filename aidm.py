#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__author__ = 'Alex Pinheiro'
__version__ = '0.1'
__link__ = 'https://github.com/Alexsussa/AIDM'

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys

pid = os.getpid()
pidfile = '/tmp/aidm.pid'
if not os.path.isfile(pidfile):
    os.system(f'touch {pidfile}')
    os.system(f'echo {pid} >> {pidfile}')
else:
    sys.exit(-1)


class AppImageDesktopMaker(Gtk.Window):
    def __init__(self):
        self.aichooser = builder.get_object('appimagechooser')
        self.logochooser = builder.get_object('logochooser')
        self.txtnome = builder.get_object('txtnome')
        self.txtdescr = builder.get_object('txtdescr')
        self.txtappimage = builder.get_object('txtappimage')
        self.txtlogo = builder.get_object('txtlogo')
        self.loading = builder.get_object('spinner')
        self.aviso = builder.get_object('aviso')
        self.lbaviso = builder.get_object('lbaviso')
        self.sobre = builder.get_object('sobre')

        self.sobre.connect('response', lambda d, r: d.hide())

    def on_btnappimage_clicked(self, button):
        self.aichooser.show()

    def on_btncancel_clicked(self, button):
        self.aichooser.hide()

    def on_btnabrir_clicked(self, button):
        if self.txtappimage.get_text() == '':
            self.txtappimage.set_text(text=self.aichooser.get_filename())
            self.aichooser.hide()
        else:
            self.txtappimage.set_text(text='')
            self.txtappimage.set_text(text=self.aichooser.get_filename())
            self.aichooser.hide()

    def on_btnlogo_clicked(self, button):
        self.logochooser.show()

    def on_cancelarlogo_clicked(self, button):
        self.logochooser.hide()

    def on_abrirlogo_clicked(self, button):
        if self.txtlogo.get_text() == '':
            self.txtlogo.set_text(text=self.logochooser.get_filename())
            self.logochooser.hide()
        else:
            self.txtlogo.set_text(text='')
            self.txtlogo.set_text(text=self.logochooser.get_filename())
            self.logochooser.hide()

    def on_btncriar_clicked(self, button):
        nome = self.txtnome.get_text()
        descr = self.txtdescr.get_text()
        app = self.txtappimage.get_text()
        img = self.txtlogo.get_text()
        if nome == '' or descr == '' or app == '' or img == '':
            self.lbaviso.set_text('Nenhum campo pode estar vázio')
            self.aviso.show()
        else:
            self.loading.start()
            os.system(f'touch {tuple(nome)}.desktop')
            abrir = open(f'{nome}.desktop', mode='w')
            abrir.write('[Desktop Entry]\n')
            abrir.write('Version=1.0\n')
            abrir.write(f'Type=Application\n')
            abrir.write(f'Terminal=false\n')
            abrir.write(f'Icon={img}\n')
            abrir.write(f'Name={nome}\n')
            abrir.write(f'Exec="{app}"\n')
            abrir.write(f'Comment={descr}\n')
            os.system(f'chmod +x *.desktop')
            os.system(f'mv *.desktop ~/.local/share/applications')
            self.lbaviso.set_text('Atalho Desktop criado com sucesso.\n'
                                  'Agora poderá encontrá-lo no menu de aplicações.')
            self.aviso.show()

    def on_btnok_clicked(self, button):
        self.aviso.hide()
        self.loading.stop()

    def on_btnsobre_clicked(self, button):
        self.sobre.show()

    def on_aidm_destroy(self, window):
        Gtk.main_quit()
        os.system(f'rm {pidfile}')


builder = Gtk.Builder()
builder.add_from_file('ui.ui')
builder.connect_signals(AppImageDesktopMaker())
janela = builder.get_object('aidm')
janela.show_all()
Gtk.main()
