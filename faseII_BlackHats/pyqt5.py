import datetime
import io
import sys
import time
import folium

import pandas as pd
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox, QComboBox, QSplashScreen, QDialog

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt import MainWindow
from pyqt_translucent_full_loading_screen_thread import LoadingThread, LoadingTranslucentScreen

import data
import aemet_predictions

import home_ui
import popup_ui

lassoLastDame = ""
rfLastDam = ""
dTreeDam = ""
embalsePredictions = []
embalsePredictionsRf = []
embalsePredictionsDt = []
cap_total = 0
provincia = ""

predictionLasso = dict()



# Clase principal de la aplicacion
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Carga de las diferentes ventanas

        self.ui = home_ui.Ui_MainWindow()




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

        ventanaPrincipal.btnCalcular.clicked.connect(self.calculateWaterLeft)

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
        # ventanaPrincipal.comboBoxRt.currentIndexChanged.connect(self.displayDataRf)

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
        self.create_map(layoutLasso, 40.416775, -3.703790, 6)

        # random forest map
        layoutRf = QVBoxLayout()
        ventanaPrincipal.mapaRf.setLayout(layoutRf)
        self.create_map(layoutRf, 40.416775, -3.703790, 6)

        # Decision tree map
        layoutDt = QVBoxLayout()
        ventanaPrincipal.mapaDt.setLayout(layoutDt)
        self.create_map(layoutDt, 40.416775, -3.703790, 6)

    def __startLoadingThread(self):
        self.__loadingTranslucentScreen = LoadingTranslucentScreen(parent=self,
                                                                   description_text='Waiting')
        self.__loadingTranslucentScreen.setDescriptionLabelDirection('Right')
        self.__thread = LoadingThread(loading_screen=self.__loadingTranslucentScreen)
        # for second result
        # self.__thread = MyThread(loading_screen=self.__loadingTranslucentScreen)
        self.__thread.start()

    def create_map(self, layout, x, y, zoom):
        coordinate = (x, y)
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=zoom,
            location=coordinate
        )

        dams_df = pd.read_csv("data/damLocation.csv", sep=',')

        for i in range(0, (dams_df['Central'].size) - 1):
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
        return layout
        # elementos = m._children
        #
        # marcadores = []
        # for elemento in elementos.values():
        #     if isinstance(elemento, folium.Marker):
        #         marcadores.append(elemento)
        # for marcador in marcadores:
        #     print("Marcador encontrado en ubicación: ", marcador.location)

        ###################################################################################################

    def zoom_map(self, central, layout_central):
        """# dams_df = pd.read_csv("data/damLocation.csv", sep=',')
        print(central)
        #self.m.zoom_start = 10
        print(self.ui.mapaLasso.layout().itemAt(0).widget().show())"""
        layout_map = QVBoxLayout()
        self.ui.mapaLasso.setLayout(layout_map)
        self.create_map(layout_map, 40.416775, -3.703790, 12)

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

    def openSecondWindow(self, texto, fecha, central):

        self.secondWindow = SecondWindow(texto, fecha, central)
        self.secondWindow.show()


    ######################################################################################################
    # Function to change the page
    def toogleButton(self):
        global lassoLastDame
        global dTreeDam
        global rfLastDam
        global embalsePredictions

        if str(self.sender().objectName()).__contains__("Home"):
            self.ui.stackedWidget.setCurrentIndex(0)

        if str(self.sender().objectName()).__contains__("RandomForest"):
            self.ui.stackedWidget.setCurrentIndex(1)
            lassoLastDame = ""
            dTreeDam = ""
            embalsePredictions = []

        if str(self.sender().objectName()).__contains__("Lasso"):
            self.ui.stackedWidget.setCurrentIndex(2)
            dTreeDam = ""
            rfLastDam = ""
            embalsePredictions = []

        if str(self.sender().objectName()).__contains__("DecisionTree"):
            self.ui.stackedWidget.setCurrentIndex(3)
            lassoLastDame = ""
            rfLastDam = ""
            embalsePredictions = []

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

        if ((self.ui.btnHoy.isChecked()) or (self.ui.btnManiana.isChecked()) or (self.ui.btn2dias.isChecked()) or
                (self.ui.btn3dias.isChecked()) or (self.ui.btn4dias.isChecked()) or (self.ui.btn5dias.isChecked())
                or (self.ui.btn6dias.isChecked())):

            embalse = self.ui.comboBoxRf.currentText()
            """self.zoom_map(embalse, self.ui.mapaRf)"""
            global rfLastDam
            global cap_total
            global embalsePredictionsRf
            global provincia
            if rfLastDam != embalse:

                embalsePredictionsRf, cap_total, provincia = data.generate_model(2, embalse)
                embalsePredictionsRf = [round(elem, 2) for elem in embalsePredictionsRf]
                rfLastDam = embalse

            if self.ui.btnHoy.isChecked():
                try:
                    self.btn_checked_random_forest(0, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualRf.setText(str(embalsePredictionsRf[0]))
                    self.checkPredictionRandomForest(embalsePredictionsRf[0])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btnManiana.isChecked():
                try:
                    self.btn_checked_random_forest(1, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualRf.setText(str(embalsePredictionsRf[1]))
                    self.checkPredictionRandomForest(embalsePredictionsRf[1])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn2dias.isChecked():
                try:
                    self.btn_checked_random_forest(2, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualRf.setText(str(embalsePredictionsRf[2]))
                    self.checkPredictionRandomForest(embalsePredictionsRf[2])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn3dias.isChecked():
                try:
                    self.btn_checked_random_forest(3, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualRf.setText(str(embalsePredictionsRf[3]))
                    self.checkPredictionRandomForest(embalsePredictionsRf[3])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn4dias.isChecked():
                try:
                    self.btn_checked_random_forest(4, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualRf.setText(str(embalsePredictionsRf[4]))
                    self.checkPredictionRandomForest(embalsePredictionsRf[4])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn5dias.isChecked():
                try:
                    self.btn_checked_random_forest(5, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualRf.setText(str(embalsePredictionsRf[5]))
                    self.checkPredictionRandomForest(embalsePredictionsRf[5])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn6dias.isChecked():
                try:
                    self.btn_checked_random_forest(6, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualRf.setText(str(embalsePredictionsRf[6]))
                    self.checkPredictionRandomForest(embalsePredictionsRf[6])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")
        else:
            self.mensaje_error("No se ha seleccionado una fecha para mostrar los datos")

    ###########################################################################################

    def displayDataDecisionTree(self):

        if ((self.ui.btnHoy3.isChecked()) or (self.ui.btnManiana3.isChecked()) or (self.ui.btn2dias3.isChecked()) or
                (self.ui.btn3dias3.isChecked()) or (self.ui.btn4dias3.isChecked()) or (self.ui.btn5dias3.isChecked())
                or (self.ui.btn6dias3.isChecked())):


            embalse = self.ui.comboBoxDt.currentText()
            print(embalse)
            global dTreeDam
            global cap_total
            global embalsePredictionsDt
            global provincia
            if dTreeDam != embalse:
                embalsePredictionsDt, cap_total, provincia = data.generate_model(2, embalse)
                embalsePredictionsDt = [round(elem, 2) for elem in embalsePredictionsDt]
                dTreeDam = embalse

            if self.ui.btnHoy3.isChecked():
                try:
                    self.btn_checked_decision_tree(0, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualDt.setText(str(embalsePredictionsDt[0]))
                    self.checkPredictionDecisionTree(embalsePredictionsDt[0])
                except Exception as e:
                    self.mensaje_error(e)

            if self.ui.btnManiana3.isChecked():
                try:
                    self.btn_checked_decision_tree(1, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualDt.setText(str(embalsePredictionsDt[1]))
                    self.checkPredictionDecisionTree(embalsePredictionsDt[1])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn2dias3.isChecked():
                try:
                    self.btn_checked_decision_tree(2, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualDt.setText(str(embalsePredictionsDt[2]))
                    self.checkPredictionDecisionTree(embalsePredictionsDt[2])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn3dias3.isChecked():
                try:
                    self.btn_checked_decision_tree(3, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualDt.setText(str(embalsePredictionsDt[3]))
                    self.checkPredictionDecisionTree(embalsePredictionsDt[3])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn4dias3.isChecked():
                try:
                    self.btn_checked_decision_tree(4, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualDt.setText(str(embalsePredictionsDt[4]))
                    self.checkPredictionDecisionTree(embalsePredictionsDt[4])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn5dias3.isChecked():
                try:
                    self.btn_checked_decision_tree(5, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualDt.setText(str(embalsePredictionsDt[5]))
                    self.checkPredictionDecisionTree(embalsePredictionsDt[5])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn6dias3.isChecked():
                try:
                    self.btn_checked_decision_tree(6, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualDt.setText(str(embalsePredictionsDt[6]))
                    self.checkPredictionDecisionTree(embalsePredictionsDt[6])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

        else:
            self.mensaje_error("No se ha seleccionado una fecha para mostrar los datos")

    ###########################################################################################

    def displayDataLasso(self):

        if ((self.ui.btnHoy2.isChecked()) or (self.ui.btnManiana2.isChecked()) or (self.ui.btn2dias2.isChecked()) or
                (self.ui.btn3dias2.isChecked()) or (self.ui.btn4dias2.isChecked()) or (self.ui.btn5dias2.isChecked())
                or (self.ui.btn6dias2.isChecked())):

            embalse = self.ui.comboBoxLasso.currentText()

            global lassoLastDame
            global embalsePredictions
            global cap_total
            global provincia

            contador = 0

            if lassoLastDame != embalse:
                embalsePredictions, cap_total, provincia = data.generate_model(2, embalse)
                embalsePredictions = [round(elem, 2) for elem in embalsePredictions]
                lassoLastDame = embalse

            if self.ui.btnHoy2.isChecked():
                try:
                    self.btn_checked_lasso(0, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualLasso.setText(str(embalsePredictions[0]))
                    self.checkPredictionLasso(embalsePredictions[0])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")
            if self.ui.btnManiana2.isChecked():
                try:
                    self.btn_checked_lasso(1, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualLasso.setText(str(embalsePredictions[1]))
                    self.checkPredictionLasso(embalsePredictions[1])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn2dias2.isChecked():
                try:
                    self.btn_checked_lasso(2, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualLasso.setText(str(embalsePredictions[2]))
                    self.checkPredictionLasso(embalsePredictions[2])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn3dias2.isChecked():
                try:
                    self.btn_checked_lasso(3, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualLasso.setText(str(embalsePredictions[3]))
                    self.checkPredictionLasso(embalsePredictions[3])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn4dias2.isChecked():
                try:
                    self.btn_checked_lasso(4, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualLasso.setText(str(embalsePredictions[4]))
                    self.checkPredictionLasso(embalsePredictions[4])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn5dias2.isChecked():
                try:
                    self.btn_checked_lasso(5, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualLasso.setText(str(embalsePredictions[5]))
                    self.checkPredictionLasso(embalsePredictions[5])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")

            if self.ui.btn6dias2.isChecked():
                try:
                    self.btn_checked_lasso(6, aemet_predictions.select_municipality(embalse), cap_total, provincia)
                    self.ui.txtReservaActualLasso.setText(str(embalsePredictions[6]))
                    self.checkPredictionLasso(embalsePredictions[6])
                except Exception as e:
                    self.mensaje_error("No hay datos para la fecha seleccionada")
        else:
            self.mensaje_error("No se ha seleccionado una fecha para mostrar los datos")


    def checkPredictionLasso(self, embalsePredictions):
        if embalsePredictions >= 90:
            self.ui.boardReservaLasso.setStyleSheet(
                "background-color: #e9c46a;border-radius: 10px;margin: 5px 10px;")


            texto = "La reserva del embalse " + self.ui.comboBoxLasso.currentText() + " se encuentra al " + str(embalsePredictions) + "%."

            fecha = "Fecha de la alerta: " + str(self.ui.fechaLasso.text())

            central = "Alerta para la central: " + self.ui.comboBoxLasso.currentText()
            try:
                self.openSecondWindow(texto, fecha, central)
            except Exception as e:
                print(e)



        elif embalsePredictions < 30:
            self.ui.boardReservaLasso.setStyleSheet("background-color: #e9c46a;border-radius: 10px;margin: 5px 10px;")

            texto = "La reserva del embalse " + self.ui.comboBoxLasso.currentText() + " se encuentra al " + str(
                embalsePredictions) + "%. Con un nivel más bajo, la presa llegará a su límite inferior."

            fecha = "Fecha de la alerta: " + str(self.ui.fechaLasso.text())

            central = "Alerta para la central: " + self.ui.comboBoxLasso.currentText()
            try:
                self.openSecondWindow(texto, fecha, central)
            except Exception as e:
                print(e)


        else:
            self.ui.boardReservaLasso.setStyleSheet(
                "background-color: #01A982;border-radius: 10px;margin: 5px 10px;")

    def checkPredictionRandomForest(self, embalsePredictionsRf):

        if embalsePredictionsRf >= 90:
            self.ui.boardReservaRf.setStyleSheet(
                "background-color: #e9c46a;border-radius: 10px;margin: 5px 10px;")

            texto = "La reserva del embalse " + self.ui.comboBoxRf.currentText() + " se encuentra al " + str(
                embalsePredictionsRf) + "%."

            fecha = "Fecha de la alerta: " + str(self.ui.fechaRf.text())

            central = "Alerta para la central: " + self.ui.comboBoxRf.currentText()
            try:
                self.openSecondWindow(texto, fecha, central)
            except Exception as e:
                print(e)



        elif embalsePredictionsRf < 30:
            self.ui.boardReservaRf.setStyleSheet("background-color: #e9c46a;border-radius: 10px;margin: 5px 10px;")

            texto = "La reserva del embalse " + self.ui.comboBoxRf.currentText() + " se encuentra al " + str(
                embalsePredictionsRf) + "%. Con un nivel más bajo, la presa llegará a su límite inferior."

            fecha = "Fecha de la alerta: " + str(self.ui.fechaRf.text())

            central = "Alerta para la central: " + self.ui.comboBoxRf.currentText()
            try:
                self.openSecondWindow(texto, fecha, central)
            except Exception as e:
                print(e)


        else:
            self.ui.boardReservaRf.setStyleSheet(
                "background-color: #01A982;border-radius: 10px;margin: 5px 10px;")

    def checkPredictionDecisionTree(self, embalsePredictionsDt):

        if embalsePredictionsDt >= 90:
            self.ui.boardReservaDt.setStyleSheet(
                "background-color: #e9c46a;border-radius: 10px;margin: 5px 10px;")

            texto = "La reserva del embalse " + self.ui.comboBoxDt.currentText() + " se encuentra al " + str(
                embalsePredictionsDt) + "%."

            fecha = "Fecha de la alerta: " + str(self.ui.fechaDt.text())

            central = "Alerta para la central: " + self.ui.comboBoxDt.currentText()
            try:
                self.openSecondWindow(texto, fecha, central)
            except Exception as e:
                print(e)



        elif embalsePredictionsDt < 30:
            self.ui.boardReservaDt.setStyleSheet("background-color: #e9c46a;border-radius: 10px;margin: 5px 10px;")

            texto = "La reserva del embalse " + self.ui.comboBoxDt.currentText() + " se encuentra al " + str(
                embalsePredictionsDt) + "%. Con un nivel más bajo, la presa llegará a su límite inferior."

            fecha = "Fecha de la alerta: " + str(self.ui.fechaDt.text())

            central = "Alerta para la central: " + self.ui.comboBoxDt.currentText()
            try:
                self.openSecondWindow(texto, fecha, central)
            except Exception as e:
                print(e)


        else:
            self.ui.boardReservaDt.setStyleSheet(
                "background-color: #01A982;border-radius: 10px;margin: 5px 10px;")



    ####################################################################################################

    # Function to calculate the water left in the dam

    def calculateWaterLeft(self):

        # check in which tab we are
        if self.ui.btnHome.isChecked():
            self.mensaje_error("No se han creado las predicciones para el embalse")

        if self.ui.btnLasso.isChecked():
            minDemand = self.ui.spinBoxDemanda.text().replace(',','.')

            minDemand = float(minDemand)

            if minDemand != float(0):
                # check if dam predictions is full
                if len(embalsePredictions) == 0:
                    self.mensaje_error("No se han creado las predicciones para el embalse")
                else:

                    agua_total = self.ui.txtCapacidadEmbalseLasso.text()

                    agua_restante = self.pop_up_agua_restante(agua_total, self.ui.txtReservaActualLasso.text())

                    if agua_restante > 0:
                        texto = "La reserva del embalse " + self.ui.comboBoxLasso.currentText() + " tendria " + str(
                            agua_restante) + " hectometros cúbicos de agua"
                    elif agua_restante < 0:
                        texto = "La reserva del embalse " + self.ui.comboBoxLasso.currentText() + " NO tendría agua " \
                                                                                                  "suficiente para esta demanda. \n Quedaría vacía"
                    fecha = ""

                    central = "Central " + self.ui.comboBoxLasso.currentText()

                    self.openSecondWindow(texto, fecha, central)

            else:
                self.mensaje_error("No se ha introducido ninguna cantidad de demanda")


        if self.ui.btnRandomForest.isChecked():

            minDemand = self.ui.spinBoxDemanda.text().replace(',', '.')

            minDemand = float(minDemand)

            if minDemand != float(0):
                # check if dam predictions is full
                if len(embalsePredictionsRf) == 0:
                    self.mensaje_error("No se han creado las predicciones para el embalse")
                else:

                    agua_total = self.ui.txtCapacidadEmbalseRf.text()

                    agua_restante = self.pop_up_agua_restante(agua_total, self.ui.txtReservaActualRf.text())
                    if agua_restante > 0:
                        texto = "La reserva del embalse " + self.ui.comboBoxRf.currentText() + " tendria " + str(agua_restante) + " hectometros cúbicos de agua"
                    elif agua_restante < 0:
                        texto = "La reserva del embalse " + self.ui.comboBoxRf.currentText() + " NO tendría agua " \
                                                                                               "suficiente para esta demanda. \n Quedaría vacía"

                    fecha = ""

                    central = "Central " + self.ui.comboBoxRf.currentText()

                    self.openSecondWindow(texto, fecha, central)

            else:
                self.mensaje_error("No se ha introducido ninguna cantidad de demanda")


        if self.ui.btnDecisionTree.isChecked():

            minDemand = self.ui.spinBoxDemanda.text().replace(',', '.')

            minDemand = float(minDemand)

            if minDemand != float(0):
                # check if dam predictions is full
                if len(embalsePredictionsDt) == 0:
                    self.mensaje_error("No se han creado las predicciones para el embalse")

                else:
                    agua_total = self.ui.txtCapacidadEmbalseDt.text()
                    # calculate the % of water left
                    agua_restante = self.pop_up_agua_restante(agua_total, self.ui.txtReservaActualDt.text())

                    if agua_restante > 0:
                        texto = "La reserva del embalse " + self.ui.comboBoxDt.currentText() + " tendria " + str(
                            agua_restante) + " hectometros cúbicos de agua"
                    elif agua_restante < 0:
                        texto = "La reserva del embalse " + self.ui.comboBoxDt.currentText() + " NO tendría agua " \
                                                                                               "suficiente para esta demanda. \n Quedaría vacía"

                    fecha = ""

                    central = "Central " + self.ui.comboBoxDt.currentText()

                    self.openSecondWindow(texto, fecha, central)

            else:
                self.mensaje_error("No se ha introducido ninguna cantidad de demanda")


    def pop_up_agua_restante(self, agua_total, prediction):
        agua_actual = (float(agua_total) * float(prediction)) / 100
        agua_texto = self.ui.spinBoxDemanda.text()
        agua_restante = agua_actual - float(agua_texto.replace(',', '.'))
        agua_restante = round(agua_restante, 2)


        return agua_restante


    def pop_up_agua_restante(self, agua_total, prediction):
        agua_actual = (float(agua_total) * float(prediction)) / 100
        agua_texto = self.ui.spinBoxDemanda.text()
        agua_restante = agua_actual - float(agua_texto.replace(',', '.'))
        agua_restante = round(agua_restante, 2)


        return agua_restante

    def btn_checked_random_forest(self, day, data, cap_total, provincia):
        unixToDatetime = datetime.datetime.fromtimestamp(data.at[day, "date"]).date()  # Unix Time
        velMed = round(data.at[day, "velmedia"], 2)
        racha = round(data.at[day, "racha"], 2)

        self.ui.fechaRf.setText(str(unixToDatetime))
        self.ui.txtTmaxRf.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminRf.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaRf.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionRf.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaRf.setText(str(velMed))
        self.ui.txtRachaRf.setText(str(racha))
        self.ui.txtSolRf.setText(str(data.at[day, "sol"]))
        self.ui.txtProvinciaRf.setText(str(provincia))
        self.ui.txtCapacidadEmbalseRf.setText(str(cap_total))

    def btn_checked_lasso(self, day, data, cap_total, provincia):
        unixToDatetime = datetime.datetime.fromtimestamp(data.at[day, "date"]).date()  # Unix Time
        velMed = round(data.at[day, "velmedia"], 2)
        racha = round(data.at[day, "racha"], 2)

        self.ui.fechaLasso.setText(str(unixToDatetime))
        self.ui.txtTmaxLasso.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminLasso.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaLasso.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionLasso.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaLasso.setText((str(velMed)))
        self.ui.txtRachaLasso.setText(str(racha))
        self.ui.txtSolLasso.setText(str(data.at[day, "sol"]))
        self.ui.txtProvinciaLasso.setText(str(provincia))
        self.ui.txtCapacidadEmbalseLasso.setText(str(cap_total))

    def btn_checked_decision_tree(self, day, data, cap_total, provincia):
        print(data.dtypes)
        unixToDatetime = datetime.datetime.fromtimestamp(data.at[day, "date"]).date()  # Unix Time
        velMed = round(data.at[day, "velmedia"], 2)
        racha = round(data.at[day, "racha"], 2)

        self.ui.fechaDt.setText(str(unixToDatetime))
        self.ui.txtTmaxDt.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminDt.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaDt.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionDt.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaDt.setText(str(velMed))
        self.ui.txtRachaDt.setText(str(racha))
        self.ui.txtSolDt.setText(str(data.at[day, "sol"]))
        self.ui.txtProvinciaDt.setText(str(provincia))
        self.ui.txtCapacidadEmbalseDt.setText(str(cap_total))

    ##############################################################################################3333

    # Funcion que cierra la aplicacion y las ventanas que esten abiertas
    def closeEvent(self, event):
        try:
            event.accept()
        except Exception as e:
            print(e)





class SecondWindow(QDialog):
    def __init__(self, label_text, label_fecha, label_central):
        super().__init__()


        self.ui = popup_ui.Ui_Dialog()

        self.ui.setupUi(self)

        self.ui.alertMessage.setText(label_text)
        self.ui.fechaAlert.setText(label_fecha)
        self.ui.nombreCentral.setText(label_central)


    def closeEvent(self, event):
        try:
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
