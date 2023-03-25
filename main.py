import datetime
import io
import sys
import time

import folium
import numpy as np
import pandas as pd
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QMessageBox
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
from zipfile import ZipFile
import pypyodbc
import pandas as pd
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


        ventanaPrincipal.stackedWidget.setCurrentIndex(0)
        ventanaPrincipal.btnHome.setChecked(True)


        # Se inicializan los botones del menu lateral
        ventanaPrincipal.btnHome.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnRandomForest.clicked.connect(self.toogleButton)
        ventanaPrincipal.btnLasso.clicked.connect(self.toogleButton)

        # botones para el random forest
        ventanaPrincipal.btnHoy.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btnManiana.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn2dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn3dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn4dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn5dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn6dias.clicked.connect(self.displayDataRf)
        ventanaPrincipal.btn7dias.clicked.connect(self.displayDataRf)


        # botones para el lasso

        ventanaPrincipal.btnHoy2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btnManiana2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn2dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn3dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn4dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn5dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn6dias2.clicked.connect(self.displayDataLasso)
        ventanaPrincipal.btn7dias2.clicked.connect(self.displayDataLasso)


        # ventanaPrincipal.btnHoy.setChecked(True)
        # ventanaPrincipal.btnHoy2.setChecked(True)




        # Mapa del Lasso
        layoutLasso = QVBoxLayout()
        ventanaPrincipal.mapaLasso.setLayout(layoutLasso)

        coordinate = (40.416775, -3.703790)
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=6,
            location=coordinate
        )

        dams_df = pd.read_csv("damLocation.csv", sep=',')

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

        dams_df = pd.read_csv("damLocation.csv", sep=',')

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

        elementos = m._children

        marcadores = []
        for elemento in elementos.values():
            if isinstance(elemento, folium.Marker):
                marcadores.append(elemento)
        for marcador in marcadores:
            print("Marcador encontrado en ubicación: ", marcador.location)






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

    #################################################################################################333333


    # Downloads the zip from the url
    def zip_download(url, save_path, chunk_size=128):
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)


    # Get the file .mdb from the zip
    def fileFromZip(ziptoread, fileToOpen):
        with ZipFile(ziptoread, 'r') as zip:
            # printing all the files of the zip file
            zip.printdir()

            # extracting all the files
            print('Extracting all the files now...')
            zip.extract(fileToOpen)
            print('Done!')


    # converts the .mdb file to a csv
    def bbddToCsv(bbddfile, tableName, csvName):
        pypyodbc.lowercase = False
        conn = pypyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + bbddfile + ';')

        # Open Cursor and execute SQL
        cur = conn.cursor()
        # Obtain all the information from the table
        query = "SELECT * FROM [" + tableName + "];"
        cur.execute(query)
        # Save the data into a dataframe
        df = pd.read_sql(query, conn)
        # Transform dataframe to csv
        df.to_csv("embalses.csv", index=False, sep=";")

        # Close connections
        cur.close()
        conn.close()


    '''
    url = 'https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/bd-embalses_tcm30-538779.zip'
    
    zip_download(url, './bbdd_embalses.zip')
    
    fileFromZip('bbdd_embalses.zip', 'BD-Embalses.mdb')
    
    bbddToCsv('./BD-Embalses.mdb','T_Datos Embalses 1988-2023','embalses.csv')
    '''


    def get_aemetData(self):

        # AEMET data
        idema = '9771C'
        all_data = []
        api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtdHJnb21lejAwQGdtYWlsLmNvbSIsImp0aSI6IjEzODdkM2VkLWFkODItNGYxYy1iNThlLWU3Mzg3MjM4OWExOSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjY2NjAxMTM4LCJ1c2VySWQiOiIxMzg3ZDNlZC1hZDgyLTRmMWMtYjU4ZS1lNzM4NzIzODlhMTkiLCJyb2xlIjoiIn0.jZclNltVxWR1_zn4MN-8xzTYNhpIyWK_70altWc-aks'
        for year in range(1988, 2024):
            url = requests.get(
                    'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/' + str(
                        year) + '-01-01T00:00:00UTC/fechafin/' + str(year) + '-12-31T23:59:59UTC/estacion/' + idema,
                    params={'api_key': api_key}).json()

            datos = url['datos']

            datos_response = requests.get(datos, headers={'api_key': api_key}, params={'api_key': api_key})

            time.sleep(1.5)

            datos_data = datos_response.json()
            print(datos_data)

            df = pd.DataFrame(datos_data)
            name = 'aemet_' + str(year) + '.csv'
            df.to_csv( name, index=False)
            data= pd.read_csv(name)
            all_data.append(data)
            os.remove(name)


        dataframe = pd.concat(all_data, axis = 0)
        dataframe.to_csv("aemet_data.csv", index=False, encoding='utf-8-sig')


    def data_preprocessing(self):
        # Load NAO data
        nao_data = pd.read_csv("https://ftp.cpc.ncep.noaa.gov/cwlinks/norm.daily.aao.cdas.z700.19790101_current.csv")

        x = pd.to_datetime(nao_data[["year", "month", "day"]]).values

        # Data Preprocessing

        aemet_data = pd.read_csv("aemet_data.csv")
        aemet_data = aemet_data.drop(['indicativo', 'nombre', 'provincia', 'altitud', 'horatmax', 'horaracha',
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
        aemet_data['tmin'] = aemet_data['tmin'].astype(float)
        aemet_data['fecha'] = pd.to_datetime(aemet_data['fecha'])

        # Obtain nao data from 1988
        nao_data = nao_data[nao_data['year']>1988]

        #
        fechas_date = pd.to_datetime(nao_data[["year", "month", "day"]]).values
        nao_data['Fecha'] = fechas_date

        # Obtain dam data from file
        df_embalses = pd.read_csv('embalses.csv', sep=";")

        # Obtain dam data from Mequinenza dam
        df_embalse_mequinenza = df_embalses[df_embalses["EMBALSE_NOMBRE"]=="Mequinenza"]

        df_embalse_mequinenza['FECHA'] = pd.to_datetime(df_embalse_mequinenza['FECHA'])

        # Merge mequinenza dataframe with nao dataframe
        df_embalses_nao = pd.merge(df_embalse_mequinenza, nao_data, left_on='FECHA', right_on='Fecha')
        # Merge mequinenza dataframe and nao dataframe with aemet dataframe
        df_embalses_nao_aemet = pd.merge(df_embalses_nao, aemet_data, left_on='Fecha', right_on='fecha')
        # Drop the columns that are not needed
        df_embalses_nao_aemet = df_embalses_nao_aemet.drop(['FECHA','Fecha','year', 'month', 'day', 'AMBITO_NOMBRE', 'EMBALSE_NOMBRE', 'ELECTRICO_FLAG'], axis=1)

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
        df_embalses_nao_aemet["Target"] = df_embalses_nao_aemet.apply(lambda row: row["AGUA_ACTUAL"]/row["AGUA_TOTAL"], axis=1)

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



    #
    # # Prediction Data
    #
    # url_aemet_prediction = requests.get("https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria"
    #                                     "/50165")
    # datos = url_aemet_prediction['datos']
    #
    #
    # datos_response = requests.get(datos, headers={'api_key': api_key}, params={'api_key': api_key})
    #
    # datos_data = datos_response.json()
    # print(datos_data)
    #
    # centrales_municipios = dict[{'Central': 'Aldeadávila', 'ID': '37014'}, {'Central': 'Alcántara', 'ID': '10008'}, {'Central': 'Almendra', 'ID': '37364'}, {'Central': 'La Muela', 'ID': '46099'}, {'Central': 'Saucelle', 'ID': '37302'}, {'Central': 'Cedillo', 'ID': '10062'}, {'Central': 'Sallente', 'ID': '25227'}, {'Central': 'Conde Guadalhorce', 'ID': '29012'}, {'Central': 'Alsa', 'ID': '39070'}, {'Central': 'MEQUINENZA', 'ID': '50165'}, {'Central': 'Barrios de Luna', 'ID': '24012'}]



    def displayDataRf(self):

        df_aemet = pd.read_csv('aemet_data.csv', sep=",")

        df_aemet = df_aemet.drop(['indicativo', 'nombre', 'provincia', 'altitud', 'horatmax', 'horaracha',
                                  'horatmin', 'horaPresMax', 'horaPresMin', 'presMax', 'presMin'], axis=1)

        df_aemet['tmed'] = df_aemet['tmed'].replace(',', '.', regex=True)
        df_aemet['prec'] = df_aemet['prec'].replace(',', '.', regex=True)
        df_aemet['velmedia'] = df_aemet['velmedia'].replace(',', '.', regex=True)
        df_aemet['racha'] = df_aemet['racha'].replace(',', '.', regex=True)
        df_aemet['sol'] = df_aemet['sol'].replace(',', '.', regex=True)
        df_aemet['tmax'] = df_aemet['tmax'].replace(',', '.', regex=True)
        df_aemet['tmin'] = df_aemet['tmin'].replace(',', '.', regex=True)

        df_aemet = df_aemet.replace('Ip', 0, inplace=False, regex=False, limit=None)

        df_aemet['tmed'] = df_aemet['tmed'].astype(float)
        df_aemet['prec'] = df_aemet['prec'].astype(float)
        df_aemet['velmedia'] = df_aemet['velmedia'].astype(float)
        df_aemet['racha'] = df_aemet['racha'].astype(float)
        df_aemet['sol'] = df_aemet['sol'].astype(float)
        df_aemet['tmax'] = df_aemet['tmax'].astype(float)
        df_aemet['tmin'] = df_aemet['tmin'].astype(float)
        df_aemet['fecha'] = pd.to_datetime(df_aemet['fecha'])

        # se obtiene la fecha actual y se obtienen los datos de la semana actual
        current_date = datetime.datetime.now()
        fecha = datetime.datetime(current_date.year, current_date.month, current_date.day)

        fechas_menores = df_aemet.loc[df_aemet['fecha'] >= fecha]
        fechas_seleccionadas = fechas_menores.head(8)

        fechas = fechas_seleccionadas['fecha'].tolist()
        tmpMedias = fechas_seleccionadas['tmed'].tolist()
        precipitaciones = fechas_seleccionadas['prec'].tolist()
        tmpMin = fechas_seleccionadas['tmin'].tolist()
        tmpMax = fechas_seleccionadas['tmax'].tolist()
        direcciones = fechas_seleccionadas['dir'].tolist()
        velocidadMedia = fechas_seleccionadas['velmedia'].tolist()
        rachas = fechas_seleccionadas['racha'].tolist()
        sols = fechas_seleccionadas['sol'].tolist()

        if self.ui.btnHoy.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[0]))

                self.ui.txtTmaxRf.setText(str(tmpMax[0]))
                self.ui.txtTminRf.setText(str(tmpMin[0]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[0]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[0]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[0]))
                self.ui.txtRachaRf.setText(str(rachas[0]))

                self.ui.txtSolRf.setText(str(sols[0]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btnManiana.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[1]))

                self.ui.txtTmaxRf.setText(str(tmpMax[1]))
                self.ui.txtTminRf.setText(str(tmpMin[1]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[1]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[1]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[1]))
                self.ui.txtRachaRf.setText(str(rachas[1]))

                self.ui.txtSolRf.setText(str(sols[1]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn2dias.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[2]))

                self.ui.txtTmaxRf.setText(str(tmpMax[2]))
                self.ui.txtTminRf.setText(str(tmpMin[2]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[2]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[2]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[2]))
                self.ui.txtRachaRf.setText(str(rachas[2]))

                self.ui.txtSolRf.setText(str(sols[2]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn3dias.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[3]))

                self.ui.txtTmaxRf.setText(str(tmpMax[3]))
                self.ui.txtTminRf.setText(str(tmpMin[3]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[3]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[3]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[3]))
                self.ui.txtRachaRf.setText(str(rachas[3]))

                self.ui.txtSolRf.setText(str(sols[3]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn4dias.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[4]))

                self.ui.txtTmaxRf.setText(str(tmpMax[4]))
                self.ui.txtTminRf.setText(str(tmpMin[4]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[4]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[4]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[4]))
                self.ui.txtRachaRf.setText(str(rachas[4]))

                self.ui.txtSolRf.setText(str(sols[4]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn5dias.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[5]))

                self.ui.txtTmaxRf.setText(str(tmpMax[5]))
                self.ui.txtTminRf.setText(str(tmpMin[5]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[5]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[5]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[5]))
                self.ui.txtRachaRf.setText(str(rachas[5]))

                self.ui.txtSolRf.setText(str(sols[5]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn6dias.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[6]))

                self.ui.txtTmaxRf.setText(str(tmpMax[6]))
                self.ui.txtTminRf.setText(str(tmpMin[6]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[6]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[6]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[6]))
                self.ui.txtRachaRf.setText(str(rachas[6]))

                self.ui.txtSolRf.setText(str(sols[6]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn7dias.isChecked():
            try:
                self.ui.fechaRf.setText(str(fechas[7]))

                self.ui.txtTmaxRf.setText(str(tmpMax[7]))
                self.ui.txtTminRf.setText(str(tmpMin[7]))
                self.ui.txtTmediaRf.setText(str(tmpMedias[7]))

                self.ui.txtPrecipitacionRf.setText(str(precipitaciones[7]))
                self.ui.txtVelMediaRf.setText(str(velocidadMedia[7]))
                self.ui.txtRachaRf.setText(str(rachas[7]))

                self.ui.txtSolRf.setText(str(sols[7]))

            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")


    ###########################################################################################

    def displayDataLasso(self):

        df_aemet = pd.read_csv('aemet_data.csv', sep=",")

        df_aemet = df_aemet.drop(['indicativo', 'nombre', 'provincia', 'altitud', 'horatmax', 'horaracha',
                                  'horatmin', 'horaPresMax', 'horaPresMin', 'presMax', 'presMin'], axis=1)

        df_aemet['tmed'] = df_aemet['tmed'].replace(',', '.', regex=True)
        df_aemet['prec'] = df_aemet['prec'].replace(',', '.', regex=True)
        df_aemet['velmedia'] = df_aemet['velmedia'].replace(',', '.', regex=True)
        df_aemet['racha'] = df_aemet['racha'].replace(',', '.', regex=True)
        df_aemet['sol'] = df_aemet['sol'].replace(',', '.', regex=True)
        df_aemet['tmax'] = df_aemet['tmax'].replace(',', '.', regex=True)
        df_aemet['tmin'] = df_aemet['tmin'].replace(',', '.', regex=True)

        df_aemet = df_aemet.replace('Ip', 0, inplace=False, regex=False, limit=None)

        df_aemet['tmed'] = df_aemet['tmed'].astype(float)
        df_aemet['prec'] = df_aemet['prec'].astype(float)
        df_aemet['velmedia'] = df_aemet['velmedia'].astype(float)
        df_aemet['racha'] = df_aemet['racha'].astype(float)
        df_aemet['sol'] = df_aemet['sol'].astype(float)
        df_aemet['tmax'] = df_aemet['tmax'].astype(float)
        df_aemet['tmin'] = df_aemet['tmin'].astype(float)
        df_aemet['fecha'] = pd.to_datetime(df_aemet['fecha'])

        # se obtiene la fecha actual y se obtienen los datos de la semana actual
        current_date = datetime.datetime.now()
        fecha = datetime.datetime(current_date.year, current_date.month, current_date.day)

        fechas_menores = df_aemet.loc[df_aemet['fecha'] >= fecha]
        fechas_seleccionadas = fechas_menores.head(8)

        fechas = fechas_seleccionadas['fecha'].tolist()
        tmpMedias = fechas_seleccionadas['tmed'].tolist()
        precipitaciones = fechas_seleccionadas['prec'].tolist()
        tmpMin = fechas_seleccionadas['tmin'].tolist()
        tmpMax = fechas_seleccionadas['tmax'].tolist()
        direcciones = fechas_seleccionadas['dir'].tolist()
        velocidadMedia = fechas_seleccionadas['velmedia'].tolist()
        rachas = fechas_seleccionadas['racha'].tolist()
        sols = fechas_seleccionadas['sol'].tolist()

        if self.ui.btnHoy2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[0]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[0]))
                self.ui.txtTminLasso.setText(str(tmpMin[0]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[0]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[0]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[0]))
                self.ui.txtRachaLasso.setText(str(rachas[0]))

                self.ui.txtSolLasso.setText(str(sols[0]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btnManiana2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[1]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[1]))
                self.ui.txtTminLasso.setText(str(tmpMin[1]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[1]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[1]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[1]))
                self.ui.txtRachaLasso.setText(str(rachas[1]))

                self.ui.txtSolLasso.setText(str(sols[1]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn2dias2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[2]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[2]))
                self.ui.txtTminLasso.setText(str(tmpMin[2]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[2]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[2]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[2]))
                self.ui.txtRachaLasso.setText(str(rachas[2]))

                self.ui.txtSolLasso.setText(str(sols[2]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn3dias2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[3]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[3]))
                self.ui.txtTminLasso.setText(str(tmpMin[3]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[3]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[3]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[3]))
                self.ui.txtRachaLasso.setText(str(rachas[3]))

                self.ui.txtSolLasso.setText(str(sols[3]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn4dias2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[4]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[4]))
                self.ui.txtTminLasso.setText(str(tmpMin[4]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[4]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[4]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[4]))
                self.ui.txtRachaLasso.setText(str(rachas[4]))

                self.ui.txtSolLasso.setText(str(sols[4]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn5dias2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[5]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[5]))
                self.ui.txtTminLasso.setText(str(tmpMin[5]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[5]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[5]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[5]))
                self.ui.txtRachaLasso.setText(str(rachas[5]))

                self.ui.txtSolLasso.setText(str(sols[5]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn6dias2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[6]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[6]))
                self.ui.txtTminLasso.setText(str(tmpMin[6]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[6]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[6]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[6]))
                self.ui.txtRachaLasso.setText(str(rachas[6]))

                self.ui.txtSolLasso.setText(str(sols[6]))
            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")

        if self.ui.btn7dias2.isChecked():
            try:
                self.ui.fechaLasso.setText(str(fechas[7]))

                self.ui.txtTmaxLasso.setText(str(tmpMax[7]))
                self.ui.txtTminLasso.setText(str(tmpMin[7]))
                self.ui.txtTmediaLasso.setText(str(tmpMedias[7]))

                self.ui.txtPrecipitacionLasso.setText(str(precipitaciones[7]))
                self.ui.txtVelMediaLasso.setText(str(velocidadMedia[7]))
                self.ui.txtRachaLasso.setText(str(rachas[7]))

                self.ui.txtSolLasso.setText(str(sols[7]))

            except Exception as e:
                self.mensaje_error("No hay datos para la fecha seleccionada")













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
    app = QApplication(sys.argv)


    # Hoja de estilos
    style_file = QFile("index.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    # Establecer un logo a la ventana
    #window.setWindowIcon(QtGui.QIcon(r"ETEN_png.png"))
    window.show()

    sys.exit(app.exec_())













