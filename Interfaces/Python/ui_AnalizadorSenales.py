################################################################################
## Analizador de Señales Fisiológicas  
##
## Copyright (C) 2025  Luis Enrique Nava Garcia
##
## Contact Email: navaluisfisbio@ciencias.unam.mx
##
## Created by: Qt User Interface Compiler version 5.15.2  -*- coding: utf-8 -*-
################################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap, QIcon, QMovie, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
import atexit
from matplotlib import cm
from matplotlib.animation import FuncAnimation, FFMpegFileWriter, FFMpegWriter, PillowWriter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pyedflib import highlevel
mpl.use('Qt5Agg')

class Lienzo(FigureCanvasQTAgg):
    """Clase que contiene el diseño y configuración inicial del lienzo para las gráficas."""
    # El código de esta clase fue modificado de Fitzpatrick, M. (05 de febrero de 2024). Plotting with Matplotlib. Create PyQt5 plots with the popular Python plotting library. PythonGUIs. https://www.pythonguis.com/tutorials/plotting-matplotlib/
    
    def __init__(self, contenedor = None, ancho = 740, alto = 400, dpi = 100):
        """
        Diseño y configuración del lienzo.
        
        Parámetros
        ----------   
        contenedor** : Parent del widget. No se modifica.

        ancho** : entero
            Ancho en pixeles del lienzo.

        alto** : entero
            Alto en pixeles del lienzo.

        dpi** : entero
            Dots per inch del lienzo.

        visible** : bool
            Determina si el lienzo es visible o no.
        """

        # Diseño del lienzo.
        self.figura = plt.figure(figsize=(ancho/dpi, alto/dpi), dpi=dpi, visible=False)
        super(Lienzo, self).__init__(self.figura)

class Ui_MainWindow(QMainWindow):
    def __init__(self, ventana):
        """
        Inicializa la pantalla principal y la aplicación.
        
        Parámetros
        ----------
        **ventana** : QMainWindow
            Ventana principal.
        """

        super(self.__class__, self).__init__(ventana)
        self.VentanaPrincipal = ventana

        # Creación de la ventana principal.
        self.setupUi(self.VentanaPrincipal)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 840)
        MainWindow.setWindowTitle("Analizador de Senales")
        MainWindow.setMaximumSize(QSize(1280, 840))
        MainWindow.setStyleSheet(u"background-color: rgb(234, 237, 239)\n")
        # Algunos aspectos a utilizar de manera repetida.
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.horizontal = QHBoxLayout(self.centralwidget)
        self.horizontal.setSpacing(20)
        self.horizontal.setContentsMargins(20,20,20,20)
        self.horizontal.setStretch(0, 220)
        self.horizontal.setStretch(0, 990)

        frame_1 = QFrame()
        frame_1.setSizePolicy(sizePolicy)
        frame_1.setMinimumSize(QSize(220, 820))
        frame_1.setMaximumSize(QSize(220, 820))
        frame_1.setStyleSheet("color: rgb(11, 61, 98); background-color: rgb(234, 237, 239)")
        frame_1.setFrameShape(QFrame.StyledPanel)
        frame_1.setFrameShadow(QFrame.Raised)
        self.horizontal.addWidget(frame_1)

        self.vertical1 = QVBoxLayout(frame_1)
        self.vertical1.setSpacing(10)
        self.vertical1.setContentsMargins(10, 0, 10, 0)
        self.vertical1.setStretch(0, 130)
        self.vertical1.setStretch(1, 50)
        self.vertical1.setStretch(2, 580)

        self.frame = QFrame(frame_1)
        self.frame.setContentsMargins(0,0,0,0)
        self.frame.setMaximumSize(QSize(200, 130))
        self.frame.setMinimumSize(QSize(200, 130))
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 161, 100))
        self.frame.setStyleSheet(u"border: 1px solid rgb(0,0,0);\n background-color: rgb(245, 245, 245)")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(20)

        self.vertical2 = QVBoxLayout(self.frame)
        self.vertical2.setSpacing(10)
        self.vertical2.setObjectName(u"verticalLayout")
        self.vertical2.setContentsMargins(0, 0, 0, 10)

        self.label = QLabel()
        self.label.setMaximumSize(QSize(198, 30))
        self.label.setMinimumSize(QSize(198, 30))
        self.label.setObjectName(u"label")
        self.label.setStyleSheet("background-color: rgb(209, 209, 209); border: 0px transparent black")
        self.label.setGeometry(QRect(0, 0, 161, 20))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.vertical2.addWidget(self.label)

        self.radioButton = QRadioButton()
        self.radioButton.setMaximumSize(QSize(190, 30))
        self.radioButton.setMinimumSize(QSize(190, 30))
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(10, 30, 80, 18))
        self.radioButton.setStyleSheet(u"border: 0px transparent black;")
        self.radioButton.setChecked(True)
        self.vertical2.addWidget(self.radioButton)
        self.radioButton_2 = QRadioButton()
        self.radioButton_2.setMaximumSize(QSize(190, 30))
        self.radioButton_2.setMinimumSize(QSize(190, 30))
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(10, 50, 80, 18))
        self.radioButton_2.setStyleSheet(u"border: 0px transparent black;")
        self.vertical2.addWidget(self.radioButton_2)
        self.radioButton_3 = QRadioButton()
        self.radioButton_3.setMaximumSize(QSize(190, 30))
        self.radioButton_3.setMinimumSize(QSize(190, 30))
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(10, 70, 80, 18))
        self.radioButton_3.setStyleSheet(u"border: 0px transparent black;")

        self.tipo = QButtonGroup()
        self.tipo.addButton(self.radioButton, 1)
        self.tipo.addButton(self.radioButton_2, 2)
        self.tipo.addButton(self.radioButton_3, 3)
        self.tipo.setExclusive(True)

        self.vertical2.addWidget(self.radioButton_3)
        self.vertical1.addWidget(self.frame, 0)

        self.Importar = QPushButton(frame_1)
        self.Importar.setMaximumSize(QSize(150, 50))
        self.Importar.setMinimumSize(QSize(150, 50))
        self.Importar.setObjectName(u"pushButton")
        self.Importar.setGeometry(QRect(50, 118, 75, 23))
        self.Importar.clicked.connect(self.importarArchivo)
        self.Importar.setStyleSheet(u"background-color: rgb(245, 245, 245);\n border-radius: 5px;\n border: 1px solid rgb(0,0,0);")
        self.vertical1.addWidget(self.Importar, 1, alignment=Qt.AlignHCenter)

        self.frame_2 = QFrame(frame_1)
        self.frame_2.setContentsMargins(0,0,0,0)
        self.frame_2.setMaximumSize(QSize(200, 500))
        self.frame_2.setMinimumSize(QSize(200, 500))
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 149, 161, 321))
        self.frame_2.setStyleSheet(u"background-color: rgb(245, 245, 245);\n"
"border: 1px solid rgb(0,0,0);")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 10)
        
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setMaximumSize(QSize(198, 30))
        self.label_2.setMinimumSize(QSize(198, 30))
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet("background-color: rgb(209, 209, 209); border: 0px transparent black")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.label_2)
        
        self.listWidget = QListWidget()
        self.listWidget.setMinimumSize(QSize(175, 340))
        self.listWidget.setMaximumSize(QSize(175, 340))
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setStyleSheet(u"background-color: rgb(255, 255, 255)")
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.verticalLayout.addWidget(self.listWidget, alignment=Qt.AlignHCenter)

        self.pushButton_3 = QPushButton()
        self.pushButton_3.setMaximumSize(QSize(150, 40))
        self.pushButton_3.setMinimumSize(QSize(150, 40))
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setStyleSheet(u"background-color: rgb(245, 245, 245);\n border-radius: 5px;\n border: 1px solid rgb(0,0,0);")

        self.verticalLayout.addWidget(self.pushButton_3, alignment=Qt.AlignHCenter)

        self.pushButton_2 = QPushButton()
        self.pushButton_2.setMaximumSize(QSize(150, 40))
        self.pushButton_2.setMinimumSize(QSize(150, 40))
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"background-color: rgb(245, 245, 245);\n border-radius: 5px;\n border: 1px solid rgb(0,0,0);")
        self.verticalLayout.addWidget(self.pushButton_2, alignment=Qt.AlignHCenter)
        self.vertical1.addWidget(self.frame_2, 2)

        # ---------------------------------------------------------

        self.frame3 = QFrame()
        self.frame3.setSizePolicy(sizePolicy)
        self.frame3.setMinimumSize(QSize(950, 820))
        self.frame3.setMaximumSize(QSize(950, 820))
        self.frame3.setStyleSheet("color: rgb(11, 61, 98); background-color: rgb(234, 237, 239)")
        self.frame3.setFrameShape(QFrame.StyledPanel)
        self.frame3.setFrameShadow(QFrame.Raised)
        self.horizontal.addWidget(self.frame3)

        self.vertical4 = QVBoxLayout(self.frame3)
        self.vertical4.setSpacing(10)
        self.vertical4.setContentsMargins(10, 0, 10, 0)
        self.vertical4.setStretch(0, 520)
        self.vertical4.setStretch(1, 280)

        self.frame_4 = QFrame()
        self.frame_4.setMinimumSize(QSize(930, 520))
        self.frame_4.setMaximumSize(QSize(930, 520))
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(200, 9, 651, 251))
        self.frame_4.setStyleSheet(u"background-color: rgb(245, 245, 245);\n"
"border: 1px solid rgb(0,0,0);")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.vertical5 = QVBoxLayout(self.frame_4)
        self.vertical5.setSpacing(10)
        self.vertical5.setObjectName(u"vertical5")
        self.vertical5.setContentsMargins(0, 0, 0, 10)

        self.label_4 = QLabel()
        self.label_4.setMaximumSize(QSize(928, 30))
        self.label_4.setMinimumSize(QSize(928, 30))
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet("background-color: rgb(209, 209, 209); border: 0px transparent black")
        self.label_4.setGeometry(QRect(0, 0, 651, 20))
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.vertical5.addWidget(self.label_4)

        self.horizontal3 = QHBoxLayout()
        self.horizontal3.setSpacing(20)
        self.horizontal3.setObjectName(u"horizontal3")
        self.horizontal3.setContentsMargins(10, 10, 10, 10)

        self.listWidget_2 = QListWidget()
        self.listWidget_2.setMinimumSize(QSize(120, 280))
        self.listWidget_2.setMaximumSize(QSize(120, 280))
        QListWidgetItem(self.listWidget_2)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setGeometry(QRect(10, 70, 91, 131))
        self.listWidget_2.setStyleSheet(u"background-color: rgb(255, 255, 255)")
        self.listWidget_2.currentItemChanged.connect(self.changeChannel)
        self.horizontal3.addWidget(self.listWidget_2, alignment=Qt.AlignVCenter)

        self.vertical7 = QVBoxLayout()
        self.vertical7.setSpacing(0)
        self.vertical7.setObjectName(u"horizontal3")
        self.vertical7.setContentsMargins(0, 0, 0, 0)

        self.Grafica = Lienzo(self)
        self.Grafica.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        class BarraHerramientasPersonalizada(NavigationToolbar):
            """Clase que contiene la barra de herramientas personalizada."""
            # Eliminación de los botones de "configuración de subgráficas" y "edición de ejes, curvas y parámetros de imagen".
            NavigationToolbar.toolitems.pop(-3)
            NavigationToolbar.toolitems.pop(-3)
        self.BarraHerramientas = BarraHerramientasPersonalizada(self.Grafica, VentanaInicial)
        self.BarraHerramientas.setStyleSheet(u"background-color:rgb(255, 255, 255); color:rgb(11, 61, 98); margin:0px; padding:5px; border: 0px transparent black")
        self.BarraHerramientas.setMinimumSize(QSize(740, 40))
        self.BarraHerramientas.setMaximumSize(QSize(740, 50))
        self.BarraHerramientas.setVisible(False)
        self.BarraHerramientas.update()
        self.vertical7.addWidget(self.BarraHerramientas, alignment=Qt.AlignHCenter)
        self.vertical7.addWidget(self.Grafica, alignment=Qt.AlignHCenter)

        self.horizontal3.addLayout(self.vertical7)

        self.vertical5.addLayout(self.horizontal3)
        self.vertical4.addWidget(self.frame_4)

        """
        self.frame_6 = QFrame()
        self.frame_6.setMinimumSize(QSize(930, 280))
        self.frame_6.setMaximumSize(QSize(930, 280))
        self.frame_6.setObjectName(u"frame_4")
        self.frame_6.setGeometry(QRect(200, 9, 651, 251))
        self.frame_6.setStyleSheet(u"background-color: rgb(245, 245, 245);\n"
"border: 1px solid rgb(0,0,0);")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        """
        self.horizontal4 = QHBoxLayout()
        self.horizontal4.setSpacing(20)
        self.horizontal4.setObjectName(u"horizontal4")
        self.horizontal4.setContentsMargins(0, 10, 0, 10)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setMaximumSize(QSize(340, 260))
        self.tableWidget.setMinimumSize(QSize(340, 260))
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setBackground(QColor(245, 245, 245));
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(200, 271, 241, 201))
        self.tableWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(0,0,0);")
        self.tableWidget.setFrameShape(QFrame.Panel)
        self.tableWidget.setFrameShadow(QFrame.Plain)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.horizontal4.addWidget(self.tableWidget, alignment=Qt.AlignVCenter)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setMaximumSize(QSize(570, 260))
        self.frame_3.setMinimumSize(QSize(570, 260))
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(450, 270, 401, 201))
        self.frame_3.setStyleSheet(u"background-color: rgb(245, 245, 245);\n"
"border: 1px solid rgb(0,0,0);")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.vertical6 = QVBoxLayout(self.frame_3)
        self.vertical6.setSpacing(10)
        self.vertical6.setObjectName(u"vertical6")
        self.vertical6.setContentsMargins(0, 0, 0, 10)

        self.label_3 = QLabel()
        self.label_3.setMaximumSize(QSize(568, 30))
        self.label_3.setMinimumSize(QSize(568, 30))
        self.label_3.setStyleSheet("background-color: rgb(209, 209, 209); border: 0px transparent black")
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 0, 401, 20))
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.vertical6.addWidget(self.label_3)

        self.frame_6 = QFrame()
        self.frame_6.setMaximumSize(QSize(568, 210))
        self.frame_6.setMinimumSize(QSize(568, 210))
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(450, 270, 401, 201))
        self.frame_6.setStyleSheet(u"background-color: rgb(245, 245, 245);\n"
"border: 0px solid rgb(0,0,0);")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.vertical6.addWidget(self.frame_6)

        self.horizontal4.addWidget(self.frame_3)
        self.vertical4.addLayout(self.horizontal4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def importarArchivo(self):
        a = 1;

    def changeChannel(self):
        a = 1

    def graficar(self, lienzo, label):
        a = 1


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Analizador de Se\u00f1ales", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Tipo de Se\u00f1al", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"ECG", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"EEG", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"EMG", None))
        self.Importar.setText(QCoreApplication.translate("MainWindow", u"Importar", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Obtenci\u00f3n de Par\u00e1metros", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"Frecuencia Card\u00edaca", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Intervalo R-R", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Amplitud", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Calcular", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Graficar", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Gr\u00e1fica", None))
        __sortingEnabled1 = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.listWidget_2.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Electrodo 1", None));
        self.listWidget_2.setSortingEnabled(__sortingEnabled1)
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Par\u00e1metro", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Valor", None));
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Procesamiento de la Se\u00f1al", None))

    # retranslateUi

# Ejecución de la aplicación
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    VentanaInicial = QMainWindow()
    ui = Ui_MainWindow(VentanaInicial)
    VentanaInicial.show()
    ret = app.exec_()

    # Limpieza archivos creados para la interpretaccion y cierre de ventanas secundarias 
    # en caso de un cierre inesperado de la aplicación.
    # atexit.register()
    
    sys.exit(ret) 