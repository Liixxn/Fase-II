import io
import sys
import time

import folium
import numpy as np
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
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



        layout = QVBoxLayout()
        ventanaPrincipal.mapa.setLayout(layout)

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


        # Se inicializan los botones del menu lateral
        self.ui.btnHome.clicked.connect(self.toogleButton)
        self.ui.btnRandomForest.clicked.connect(self.toogleButton)

















        ######################################################################################################
        # Funcion que despliega las paginas del menu lateral
        def toogleButton(self):
            if str(self.sender().objectName()).__contains__("Home"):
                self.ui.stackedWidget.setCurrentIndex(0)

            if str(self.sender().objectName()).__contains__("Random Forest"):
                self.ui.stackedWidget.setCurrentIndex(1)

            if str(self.sender().objectName()).__contains__("2 modelo"):
                self.ui.stackedWidget.setCurrentIndex(2)
            if str(self.sender().objectName()).__contains__("3 modelo"):
                self.ui.stackedWidget.setCurrentIndex(3)

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
    # style_file = QFile("index.qss")
    # style_file.open(QFile.ReadOnly | QFile.Text)
    # style_stream = QTextStream(style_file)
    # app.setStyleSheet(style_stream.readAll())

    window = MainWindow()
    # Establecer un logo a la ventana
    #window.setWindowIcon(QtGui.QIcon(r"ETEN_png.png"))
    window.show()

    sys.exit(app.exec_())













