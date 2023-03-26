import datetime
import io
import sys
import time
import folium

import pandas as pd
from PyQt5.QtCore import QFile, QTextStream

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox, QComboBox

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


# import data
import aemet_predictions

import os

from datetime import date


from home_ui import Ui_MainWindow


# Clase principal de la aplicacion
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Carga de las diferentes ventanas

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



        # Inicializacion de los elementos
        ventanaPrincipal = self.ui

        """comboBoxDt = QComboBox(self)

        embalses = ["Central de Aldeadávila", "Central José María de Oriol", "Central de Villarino", "Central de Cortes-La Muela",
                    "Central de Saucelle", "Cedillo", "Estany-Gento Sallente", "Central de Tajo de la Encantada",
                    "Central de Aguayo", "Mequinenza", "Mora de Luna"]

        comboBoxDt.addItems(embalses)
        comboBoxDt.currentIndexChanged.connect(self.displayDataDecisionTree)"""

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



        # botones para el random forest
        ventanaPrincipal.btnHoy.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btnManiana.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn2dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn3dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn4dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn5dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn6dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn7dias.clicked.connect(self.displayDataRf)
        #ventanaPrincipal.comboBoxRt.currentIndexChanged.connect(self.displayDataRf)

        # botones para el lasso
        ventanaPrincipal.btnHoy2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btnManiana2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn2dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn3dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn4dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn5dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn6dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn7dias2.clicked.connect(self.displayDataLasso)

        # botones para el Decision Tree
        ventanaPrincipal.btnHoy3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btnManiana3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn2dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn3dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn4dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn5dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn6dias3.clicked.connect(self.displayDataDecisionTree)
        ventanaPrincipal.btn7dias3.clicked.connect(self.displayDataDecisionTree)



        #######################################################################################
        # Mapa del Lasso
        layoutLasso = QVBoxLayout()
        ventanaPrincipal.mapaLasso.setLayout(layoutLasso)

        coordinate = (40.416775, -3.703790)
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=6,
            location=coordinate
        )

        dams_df = pd.read_csv("data/damLocation.csv", sep=',')

        for i in range(0, (dams_df['Central'].size) - 1):
            # print(dams_df['Coordenadas'][i])
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
        layoutLasso.addWidget(webView)

        ########################################################################################

        # Mapa del random forest
        layout = QVBoxLayout()
        ventanaPrincipal.mapaRf.setLayout(layout)

        coordinate = (40.416775, -3.703790)
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=6,
            location=coordinate
        )

        dams_df = pd.read_csv("data/damLocation.csv", sep=',')

        for i in range(0, (dams_df['Central'].size) - 1):
            # print(dams_df['Coordenadas'][i])
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



        ###############################################################################################

        # Mapa del random decision tree
        layout = QVBoxLayout()
        ventanaPrincipal.mapaDt.setLayout(layout)

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

        # Mapa del random decision tree
        layout = QVBoxLayout()
        ventanaPrincipal.mapaDt.setLayout(layout)

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






    def data_preprocessing(self):
        # Load NAO data
        nao_data = pd.read_csv("https://ftp.cpc.ncep.noaa.gov/cwlinks/norm.daily.aao.cdas.z700.19790101_current.csv")

        x = pd.to_datetime(nao_data[["year", "month", "day"]]).values

        # Data Preprocessing
        aemet_data = pd.read_csv('./data/aemet_data.csv', sep=',')
        """aemet_data = aemet_data.drop(['indicativo', 'nombre', 'provincia', 'altitud', 'horatmax', 'horaracha',
                                      'horatmin', 'horaPresMax', 'horaPresMin', 'presMax', 'presMin'], axis=1)

        aemet_data['tmed'] = aemet_data['tmed'].replace(',', '.', regex=True)
        aemet_data['prec'] = aemet_data['prec'].replace(',', '.', regex=True)
        aemet_data['velmedia'] = aemet_data['velmedia'].replace(',', '.', regex=True)
        aemet_data['racha'] = aemet_data['racha'].replace(',', '.', regex=True)
        aemet_data['sol'] = aemet_data['sol'].replace(',', '.', regex=True)
        aemet_data['tmax'] = aemet_data['tmax'].replace(',', '.', regex=True)
        aemet_data['tmin'] = aemet_data['tmin'].replace(',', '.', regex=True)

        # Replace Ip values with 0
        aemet_data = aemet_data.replace('Ip', 0, inplace=False, regex=False, limit=None)

        # Convert data types to float
        aemet_data['tmed'] = aemet_data['tmed'].astype(float)
        aemet_data['prec'] = aemet_data['prec'].astype(float)
        aemet_data['velmedia'] = aemet_data['velmedia'].astype(float)
        aemet_data['racha'] = aemet_data['racha'].astype(float)
        aemet_data['sol'] = aemet_data['sol'].astype(float)
        aemet_data['tmax'] = aemet_data['tmax'].astype(float)
        aemet_data['tmin'] = aemet_data['tmin'].astype(float)"""
        aemet_data['fecha'] = pd.to_datetime(aemet_data['fecha'])

        # Obtain nao data from 1988
        nao_data = nao_data[nao_data['year'] > 1988]

        #
        fechas_date = pd.to_datetime(nao_data[["year", "month", "day"]]).values
        nao_data['Fecha'] = fechas_date

        # Obtain dam data from file
        df_embalses = pd.read_csv('embalses.csv', sep=";")

        # Obtain dam data from Mequinenza dam
        df_embalse_mequinenza = df_embalses[df_embalses["EMBALSE_NOMBRE"] == "Mequinenza"]

        df_embalse_mequinenza['FECHA'] = pd.to_datetime(df_embalse_mequinenza['FECHA'])

        # Merge mequinenza dataframe with nao dataframe
        df_embalses_nao = pd.merge(df_embalse_mequinenza, nao_data, left_on='FECHA', right_on='Fecha')
        # Merge mequinenza dataframe and nao dataframe with aemet dataframe
        df_embalses_nao_aemet = pd.merge(df_embalses_nao, aemet_data, left_on='Fecha', right_on='fecha')
        # Drop the columns that are not needed
        df_embalses_nao_aemet = df_embalses_nao_aemet.drop(
            ['FECHA', 'Fecha', 'year', 'month', 'day', 'AMBITO_NOMBRE', 'EMBALSE_NOMBRE', 'ELECTRICO_FLAG'], axis=1)

        # Transform date to unix type
        dates = []
        for i in range(0, df_embalses_nao_aemet['fecha'].size):
            dates.append(time.mktime(df_embalses_nao_aemet['fecha'][i].timetuple()))

        # Fill NaN values with 0
        df_embalses_nao_aemet = df_embalses_nao_aemet.fillna(0)
        df_embalses_nao_aemet['fecha'] = dates

        df_embalses_nao_aemet['AGUA_TOTAL'] = df_embalses_nao_aemet['AGUA_TOTAL'].str.replace(',', '.').astype(float)
        df_embalses_nao_aemet['AGUA_ACTUAL'] = df_embalses_nao_aemet['AGUA_ACTUAL'].str.replace(',', '.').astype(float)

        # Calculate the percentage of water in the dam
        df_embalses_nao_aemet["Target"] = df_embalses_nao_aemet.apply(
            lambda row: row["AGUA_ACTUAL"] / row["AGUA_TOTAL"], axis=1)

        df_embalses_nao_aemet = df_embalses_nao_aemet.drop(['AGUA_TOTAL', 'AGUA_ACTUAL'], axis=1)

        # Establish the target
        X = df_embalses_nao_aemet.drop('Target', axis=1)
        Y = df_embalses_nao_aemet['Target']
        # Split the data into training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Create an object of the model Random Forest with 100 trees
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        # Train the model on training data
        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_test)
        # Obtain the R2 score
        r2 = r2_score(y_test, y_pred)
        print(r2)


    def displayDataRf(self):

        embalse = self.comboBoxRf.currentText()


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

        #print(self.MainWindow)
        embalse = self.ui.comboBoxLasso.currentText()
        print(embalse)
        if self.ui.btnHoy2.isChecked():
            try:
                self.btn_checked_lasso(0, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error(e)

        if self.ui.btnManiana2.isChecked():
            try:
                self.btn_checked_lasso(1, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn2dias2.isChecked():
            try:
                self.btn_checked_lasso(2, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn3dias2.isChecked():
            try:
                self.btn_checked_lasso(3, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn4dias2.isChecked():
            try:
                self.btn_checked_lasso(4, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn5dias2.isChecked():
            try:
                self.btn_checked_lasso(5, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn6dias2.isChecked():
            try:
                self.btn_checked_lasso(6, aemet_predictions.select_municipality(embalse))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn7dias2.isChecked():
            try:
                self.btn_checked_lasso(7, aemet_predictions.select_municipality(embalse))

            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")


    def btn_checked_random_forest(self, day, data):
        self.ui.fechaRf.setText(str(data.at[day, "date"]))
        self.ui.txtTmaxRf.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminRf.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaRf.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionRf.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaRf.setText(str(data.at[day, "velmedia"]))
        self.ui.txtRachaRf.setText(str(data.at[day, "racha"]))
        self.ui.txtSolRf.setText(str(data.at[day, "sol"]))


    def btn_checked_lasso(self, day, data):
        self.ui.fechaLasso.setText(str(data.at[day, "date"]))
        self.ui.txtTmaxLasso.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminLasso.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaLasso.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionLasso.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaLasso.setText(str(data.at[day, "velmedia"]))
        self.ui.txtRachaLasso.setText(str(data.at[day, "racha"]))
        self.ui.txtSolLasso.setText(str(data.at[day, "sol"]))

        
    def btn_checked_decision_tree(self, day, data):
        print(data.dtypes)
        self.ui.fechaDt.setText(str(data.at[day, "date"]))
        self.ui.txtTmaxDt.setText(str(data.at[day, "tmax"]))
        self.ui.txtTminDt.setText(str(data.at[day, "tmin"]))
        self.ui.txtTmediaDt.setText(str(data.at[day, "tmed"]))
        self.ui.txtPrecipitacionDt.setText(str(data.at[day, "prec"]))
        self.ui.txtVelMediaDt.setText(str(data.at[day, "velmedia"]))
        self.ui.txtRachaDt.setText(str(data.at[day, "racha"]))
        self.ui.txtSolDt.setText(str(data.at[day, "sol"]))


    ##############################################################################################3333

    # Funcion que cierra la aplicacion y las ventanas que esten abiertas
    def closeEvent(self, event):
        try:
            event.accept()
        except Exception as e:
            print(e)



##################################################################################33333
# Main de la aplicacion
if __name__ == "__main__":
    app = QApplication(['', '--no-sandbox'])

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

    sys.exit(app.exec_())
