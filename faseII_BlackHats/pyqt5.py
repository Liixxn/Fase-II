import datetime
import io
import sys
import time
import folium

import pandas as pd
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox, QComboBox, QSplashScreen

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.uic.properties import QtGui, QtWidgets
from matplotlib.backends.backend_qt import MainWindow

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import learning_curve
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import data


# import data
import aemet_predictions

import os

from datetime import date


from home_ui import Ui_MainWindow
import popup_ui

lassoLastDame = ""
rfLastDam = ""
dTreeDam = ""


# Clase principal de la aplicacion
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Carga de las diferentes ventanas

        self.ui = Ui_MainWindow()

        # pop up
        self.Second_MainWindow = QtWidgets.QDialog()


        self.ui.setupUi(self)





        # Inicializacion de los elementos
        ventanaPrincipal = self.ui


        ventanaPrincipal.stackedWidget.setCurrentIndex(0)
        ventanaPrincipal.btnHome.setChecked(True)

        # Se inicializan los botones del menu lateral
        ventanaPrincipal.btnHome.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnRandomForest.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnLasso.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnDecisionTree.clicked.connect(self.toogleButton)


        ventanaPrincipal.btnLassoHome.clicked.connect(self.toogleButtonHome)
        ventanaPrincipal.btnRandomForestHome.clicked.connect(self.toogleButtonHome)
        ventanaPrincipal.btnDecisionTreeHome.clicked.connect(self.toogleButtonHome)

        ventanaPrincipal.comboBoxRf.currentTextChanged.connect(self.displayDataRf)
        ventanaPrincipal.comboBoxDt.currentTextChanged.connect(self.displayDataDecisionTree)
        ventanaPrincipal.comboBoxLasso.currentTextChanged.connect(self.displayDataLasso)

        # botones para el random forest
        ventanaPrincipal.btnHoy.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btnManiana.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn2dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn3dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn4dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn5dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn6dias.clicked.connect(self.displayDataRf)
        #ventanaPrincipal.comboBoxRt.currentIndexChanged.connect(self.displayDataRf)

        # botones para el lasso
        ventanaPrincipal.btnHoy2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btnManiana2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn2dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn3dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn4dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn5dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn6dias2.clicked.connect(self.displayDataLasso)

        # botones para el Decision Tree
        ventanaPrincipal.btnHoy3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btnManiana3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn2dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn3dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn4dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn5dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn6dias3.clicked.connect(self.displayDataDecisionTree)



        #######################################################################################
        # lasso map
        layoutLasso = QVBoxLayout()
        ventanaPrincipal.mapaLasso.setLayout(layoutLasso)
        self.create_map(layoutLasso)

        # random forest map
        layoutRf = QVBoxLayout()
        ventanaPrincipal.mapaRf.setLayout(layoutRf)
        self.create_map(layoutRf)

        # Decision tree map
        layoutDt = QVBoxLayout()
        ventanaPrincipal.mapaDt.setLayout(layoutDt)
        self.create_map(layoutDt)


    def create_map(self, layout):
        coordinate = (40.416775, -3.703790)
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=6,
            location=coordinate
        )

        dams_df = pd.read_csv("data/damLocation.csv", sep=',')

        for i in range(0, (dams_df['Central'].size) - 1):
            print(dams_df['Coordenadas'][i])
            coordinates = dams_df['Coordenadas'][i].replace(',', '').split()

            # Se ingresa el contenido en el popup
            iframe = folium.IFrame('Nombre de la central: ' + (dams_df["Central"][i]) + '\n\n Ubicación: ' + (
                dams_df["Ubicación"][i]) + '\n\n Potencia instalada: ' + (dams_df["Potencia instalada"][i]))

            # se inicializa el pop up y su tamaño
            popup = folium.Popup(iframe, min_width=200, max_width=200)

            folium.Marker(location=[coordinates[0], coordinates[1]],
                          icon=folium.Icon(color='blue', icon='tint'), popup=popup).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)

        # elementos = m._children
        #
        # marcadores = []
        # for elemento in elementos.values():
        #     if isinstance(elemento, folium.Marker):
        #         marcadores.append(elemento)
        # for marcador in marcadores:
        #     print("Marcador encontrado en ubicación: ", marcador.location)

        ###################################################################################################



    ######################################################################################################
    # Funcion para mostrar los errores
    def mensaje_error(self, mensaje):
        QMessageBox.critical(
            self,
            "Error",
            mensaje,
            buttons=QMessageBox.Discard,
            defaultButton=QMessageBox.Discard,
        )

    ######################################################################################################
    # Function to change the page
    def toogleButton(self):

        if str(self.sender().objectName()).__contains__("Home"):
            self.ui.stackedWidget.setCurrentIndex(0)

        if str(self.sender().objectName()).__contains__("RandomForest"):
            self.ui.stackedWidget.setCurrentIndex(1)

        if str(self.sender().objectName()).__contains__("Lasso"):
            self.ui.stackedWidget.setCurrentIndex(2)

        if str(self.sender().objectName()).__contains__("DecisionTree"):
            self.ui.stackedWidget.setCurrentIndex(3)

    #################################################################################################333333

    def toogleButtonHome(self):

        if str(self.sender().objectName()).__contains__("Lasso"):
            self.ui.btnLasso.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(1)

        if str(self.sender().objectName()).__contains__("RandomForest"):
            self.ui.btnRandomForest.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(2)

        if str(self.sender().objectName()).__contains__("DecisionTree"):
            self.ui.btnDecisionTree.setChecked(True)
            self.ui.stackedWidget.setCurrentIndex(3)




    def displayDataRf(self):

        embalse = self.ui.comboBoxRf.currentText()


        if self.ui.btnHoy.isChecked():
            try:
                self.btn_checked_random_forest(0, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btnManiana.isChecked():
            try:
                self.btn_checked_random_forest(1, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn2dias.isChecked():
            try:
                self.btn_checked_random_forest(2, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn3dias.isChecked():
            try:
                self.btn_checked_random_forest(3, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn4dias.isChecked():
            try:
                self.btn_checked_random_forest(4, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn5dias.isChecked():
            try:
                self.btn_checked_random_forest(5, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn6dias.isChecked():
            try:
                self.btn_checked_random_forest(6, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")


    ###########################################################################################

    def displayDataDecisionTree(self):
        embalse = self.ui.comboBoxDt.currentText()
        print(embalse)

        if self.ui.btnHoy3.isChecked():
            try:
                self.btn_checked_decision_tree(0, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error(e)

        if self.ui.btnManiana3.isChecked():
            try:
                self.btn_checked_decision_tree(1, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn2dias3.isChecked():
            try:
                self.btn_checked_decision_tree(2, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn3dias3.isChecked():
            try:
                self.btn_checked_decision_tree(3, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn4dias3.isChecked():
            try:
                self.btn_checked_decision_tree(4, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn5dias3.isChecked():
            try:
                self.btn_checked_decision_tree(5, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn6dias3.isChecked():
            try:
                self.btn_checked_decision_tree(6, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")



    def displayDataLasso(self):

        embalse = self.ui.comboBoxLasso.currentText()
        print(embalse+"    "lassoLastDame)

        if lassoLastDame != embalse:
            embalsePredictions = data.generate_model(2, embalse)
            lassoLastDame = embalse

        if self.ui.btnHoy2.isChecked():
            try:
                self.btn_checked_lasso(0, aemet_predictions.select_municipality(embalse))
                self.ui.txtReservaActualLasso.setText(str(embalsePredictions[0]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")
        if self.ui.btnManiana2.isChecked():
            try:
                self.btn_checked_lasso(1, aemet_predictions.select_municipality(embalse))
                self.ui.txtReservaActualLasso.setText(str(embalsePredictions[1]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn2dias2.isChecked():
            try:
                self.btn_checked_lasso(2, aemet_predictions.select_municipality(embalse))
                self.ui.txtReservaActualLasso.setText(str(embalsePredictions[2]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn3dias2.isChecked():
            try:
                self.btn_checked_lasso(3, aemet_predictions.select_municipality(embalse))
                self.ui.txtReservaActualLasso.setText(str(embalsePredictions[3]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn4dias2.isChecked():
            try:
                self.btn_checked_lasso(4, aemet_predictions.select_municipality(embalse))
                self.ui.txtReservaActualLasso.setText(str(embalsePredictions[4]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn5dias2.isChecked():
            try:
                self.btn_checked_lasso(5, aemet_predictions.select_municipality(embalse))
                self.ui.txtReservaActualLasso.setText(str(embalsePredictions[5]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn6dias2.isChecked():
            try:
                self.btn_checked_lasso(6, aemet_predictions.select_municipality(embalse))
                self.ui.txtReservaActualLasso.setText(str(embalsePredictions[6]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")



    def btn_checked_random_forest(self, day, data):
        unixToDatetime = datetime.datetime.fromtimestamp(data.at[day, "date"]).date()  # Unix Time
        velMed = round(data.at[day, "velmedia"], 2)

        self.ui.fechaRf.setText(str(unixToDatetime))
        self.ui.txtTmaxRf.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminRf.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaRf.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionRf.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaRf.setText(str(velMed))
        self.ui.txtRachaRf.setText(str(data.at[day, "racha"]))
        self.ui.txtSolRf.setText(str(data.at[day, "sol"]))


    def btn_checked_lasso(self, day, data):
        unixToDatetime = datetime.datetime.fromtimestamp(data.at[day, "date"]).date() # Unix Time
        velMed = round(data.at[day, "velmedia"], 2)

        self.ui.fechaLasso.setText(str(unixToDatetime))
        self.ui.txtTmaxLasso.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminLasso.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaLasso.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionLasso.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaLasso.setText(str(data.at[day, "velmedia"]))
        self.ui.txtRachaLasso.setText(str(data.at[day, "racha"]))
        self.ui.txtSolLasso.setText(str(data.at[day, "sol"]))



        
    def btn_checked_decision_tree(self, day, data):
        print(data.dtypes)
        unixToDatetime = datetime.datetime.fromtimestamp(data.at[day, "date"]).date()  # Unix Time
        velMed = round(data.at[day,"velmedia"], 2)

        self.ui.fechaDt.setText(str(unixToDatetime))
        self.ui.txtTmaxDt.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminDt.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaDt.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionDt.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaDt.setText(str(velMed))
        self.ui.txtRachaDt.setText(str(data.at[day, "racha"]))
        self.ui.txtSolDt.setText(str(data.at[day, "sol"]))


    ##############################################################################################3333

    # Funcion que cierra la aplicacion y las ventanas que esten abiertas
    def closeEvent(self, event):
        try:
            self.Second_MainWindow.close()
            event.accept()
        except Exception as e:
            print(e)



##################################################################################33333
# Main de la aplicacion
if __name__ == "__main__":
    app = QApplication(['', '--no-sandbox'])

    pixmap = QPixmap("imgs/BlackHats-logo.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()

    # Data gathering
    url = 'https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/bd-embalses_tcm30-538779.zip'

    # data.zip_download(url, './bbdd_embalses.zip')
    #
    # data.fileFromZip('bbdd_embalses.zip', 'BD-Embalses.mdb')
    #
    # data.bbddToCsv('./BD-Embalses.mdb', 'T_Datos Embalses 1988-2023', 'embalses.csv')

    # Hoja de estilos
    style_file = QFile("index.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())
