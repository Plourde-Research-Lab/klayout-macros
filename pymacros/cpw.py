from PyQt4 import QtCore, QtGui, uic
import os.path
from os import listdir
import sys

from cpw_design import cpw

form_class = uic.loadUiType('CPW.ui')[0]


class MyWindowClass(QtGui.QDialog, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.update()

        self.materialInput.currentIndexChanged.connect(self.update)
        self.epsInput.editingFinished.connect(self.update)
        self.lengthInput.editingFinished.connect(self.update)
        self.wInput.editingFinished.connect(self.update)
        self.gInput.editingFinished.connect(self.update)
        self.hInput.editingFinished.connect(self.update)
        self.tInput.editingFinished.connect(self.update)

    def update(self):

        self.cpw = cpw(
            material=self.materialInput.currentText(),
            w=float(self.wInput.text()),
            s=float(self.gInput.text()),
            t=float(self.tInput.text()),
            h=float(self.hInput.text()),
            l=float(self.lengthInput.text()),
            e1=float(self.epsInput.text())
            )
        self.k0Label.setText("{:.3e}".format(self.cpw.k0()))
        self.llLabel.setText("{:.3e}".format(self.cpw.Ll()))
        self.clLabel.setText("{:.3e}".format(self.cpw.Cl()))
        self.z0Label.setText("{:.3e}".format(self.cpw.z0()))
        self.tcLabel.setText("{:.3e}".format(self.cpw.Tc))
        self.rhoLabel.setText("{:.3e}".format(self.cpw.rho))
        self.lambdaLabel.setText("{:.3e}".format(self.cpw.l0))
        self.lkLabel.setText("{:.3e}".format(self.cpw.Llk()))
        self.lLabel.setText("{:.3e}".format(self.cpw.L()))
        self.cLabel.setText("{:.3e}".format(self.cpw.C()))
        self.rLabel.setText("{:.3e}".format(self.cpw.R()))
        self.qintLabel.setText("{:.3e}".format(self.cpw.Qint()))
        self.w0Label.setText("{:.3e}".format(self.cpw.wn()))
        self.f0Label.setText("{:.3e}".format(self.cpw.fn()*1e-9))

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
