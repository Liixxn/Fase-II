import datetime
import json
import os
import time
from datetime import date, datetime, timedelta, time as date_time
import numpy as np
import requests
import pandas as pd
from zipfile import ZipFile
import pypyodbc
import aemet_predictions


from sklearn.tree import DecisionTreeRegressor
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


#############################################################################################
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
        # zip_ref.extract('otro_archivo.txt', 'archivos_extraidos/')
        zip.extract(fileToOpen, './data/')
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
    df.to_csv(csvName, index=False, sep=";")

    # Close connections
    cur.close()
    conn.close()


#############################################################################################


"""
Si recibe el nombre de una central hidroeléctrica, devuelve la central hidroelectrica 
para acceder al idema es dam['idema']
"""


def get_dam():
    # de el json Hidroelectricas.json tomar todos los nombres de las centrales hidroelectricas y el idema de cada una
    with open('./data/Hidroelectrica.json') as json_file:
        dict = json.load(json_file)
    return dict


"""
Si recibe el nombre de una central hidroeléctrica, devuelve la central hidroelectrica 
para acceder al idema es dam['idema']
"""


def search_dam_name(dam_name):
    # de el json Hidroelectricas.json tomar todos los nombres de las centrales hidroelectricas y el idema de cada una
    with open('Hidroelectricas.json') as json_file:
        dict = json.load(json_file)

    i = 0
    find = False
    while i < len(dict) and find == False:
        if dict[i]['Hidroeléctrica'] == dam_name:
            find = True
            dam = dict[i]
        i += 1

    print(dam['Hidroeléctrica'])
    return dam


"""
Si recibe el idema de una central hidroeléctrica, devuelve la central hidroelectrica 
para acceder al nombre es dam['Hidroeléctrica']

"""


def search_dam_idema(dam_idema):
    # del json Hidroelectricas.json tomar todos los nombres de las centrales hidroelectricas y el idema de cada una
    with open('Hidroelectricas.json') as json_file:
        dict = json.load(json_file)

    i = 0
    find = False
    while i < len(dict) and find == False:
        if dict[i]['Indicativo'] == dam_idema:
            find = True
            dam = dict[i]
        i += 1

    print(dam['Hidroeléctrica'])
    return dam


def updateData():
    # check if there is new info on the embalses DB
    zip_download(
        'https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/bd-embalses_tcm30-538779.zip',
        './data/bbdd_embalses.zip')
    fileFromZip('./data/bbdd_embalses.zip', 'BD-Embalses.mdb')
    bbddToCsv('./data/BD-Embalses.mdb', 'T_Datos Embalses 1988-2023', './data/embalses2.csv')
    file_old = os.path.getsize("./data/embalses.csv")
    file_new = os.path.getsize("./data/embalses2.csv")

    if os.path.exists("./data/embalses.csv"):
        # compare files size
        if file_new > file_old:
            os.remove("./data/embalses.csv")
            # rename new file from embalses2.csv to embalses.csv
            os.rename("./data/embalses2.csv", "./data/embalses.csv")

        else:
            # deleted new csv because didn't have new data
            os.remove("./data/embalses2.csv")
    else:
        os.remove("./data/embalses.csv")
        # rename new file name from embalses2.csv to embalses.csv
        os.rename("./data/embalses2.csv", "./data/embalses.csv")


def get_aemet_data_embalse(embalse, idema, last_date_dataframe, date_delta):
    # AEMET data
    df = pd.DataFrame()
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtdHJnb21lejAwQGdtYWlsLmNvbSIsImp0aSI6IjEzODdkM2VkLWFkODItNGYxYy1iNThlLWU3Mzg3MjM4OWExOSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjY2NjAxMTM4LCJ1c2VySWQiOiIxMzg3ZDNlZC1hZDgyLTRmMWMtYjU4ZS1lNzM4NzIzODlhMTkiLCJyb2xlIjoiIn0.jZclNltVxWR1_zn4MN-8xzTYNhpIyWK_70altWc-aks'

    if (date_delta > 1000):
        print("mayor de mil")
        print(embalse['Hidroeléctrica'])
        for year in range(1988, 2024, 3):
            try:
                url = requests.get(
                    'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/' + str(
                        year) + '-01-01T00:00:00UTC/fechafin/' + str(year + 3) + '-12-31T23:59:59UTC/estacion/' + idema,
                    params={'api_key': api_key}).json()
                datos = url['datos']

                datos_response = requests.get(datos, headers={'api_key': api_key}, params={'api_key': api_key})

                time.sleep(2)

                datos_data = datos_response.json()

                df_year = pd.DataFrame(datos_data)
                df = pd.concat([df, df_year], axis=0)
            except Exception as e:
                print(e)
    else:
        try:
            end_date = date.today()
            last_date_datetime = datetime.combine(last_date_dataframe, date_time.min)
            last_date_datetime = (last_date_datetime + timedelta(days=1)).date()
            url = requests.get(
                'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/' + str(
                    last_date_datetime) + 'T00:00:00UTC/fechafin/' + str(end_date) + 'T23:59:59UTC/estacion/' + idema,
                params={'api_key': api_key}).json()
            datos = url['datos']

            datos_response = requests.get(datos, headers={'api_key': api_key}, params={'api_key': api_key})

            time.sleep(2)

            datos_data = datos_response.json()
            df_year = pd.DataFrame(datos_data)
            df = pd.concat([df, df_year], axis=0)
        except:
            pass

    df['embalse'] = embalse
    df_aemet = pd.read_csv('./data/aemet_data.csv', sep=',')
    df_aemet = pd.concat([df_aemet, df], axis=0)
    df_aemet = df_aemet.sort_values(['embalse', 'fecha'], ascending=True)

    df_aemet = dataframe_preprocessing(df_aemet)

    df_aemet.to_csv("./data/aemet_data.csv", index=False, encoding='utf-8-sig', sep=',')


def update_aemet_data():
    """
    -Tener todos los idemas de las hidroeletricas
    -Comprobar si esta ese csv actualizado con la fecha de hoy
    -De no ser la fecha de hoy hacer una peticion a la api con la ultima fecha en el csv hasta hoy
    -unir esos datos con los datos que estan en el csv, cargarlos en el dataframe y agregarlos
    -guardar el csv
    """
    embalses = get_dam()
    for embalse in embalses:
        df_aemet = pd.read_csv('./data/aemet_data.csv', sep=',')
        df_embalse_alcantara = df_aemet[df_aemet["embalse"] == embalse['Hidroeléctrica']]

        if (len(df_embalse_alcantara) != 0):
            last_value = df_embalse_alcantara.iloc[-1]['fecha']
            today_date = date.today()
            if last_value != today_date:
                fecha = datetime.strptime(last_value, "%Y-%m-%d").date()
                diferencia_dias = (fecha - today_date).days
                # api request from the last day to today
                get_aemet_data_embalse(embalse['Hidroeléctrica'], embalse['Indicativo'], fecha, diferencia_dias)
        else:
            get_aemet_data_embalse(embalse['Hidroeléctrica'], embalse['Indicativo'], 0, 99999)


def dataframe_preprocessing(df_aemet):
    df_aemet = df_aemet.drop(['dir', 'altitud', 'horatmax', 'horaracha',
                              'horatmin', 'horaPresMax', 'horaPresMin', 'presMax', 'presMin'], axis=1)

    df_aemet['tmed'] = df_aemet['tmed'].replace(',', '.', regex=True)
    df_aemet['prec'] = df_aemet['prec'].replace(',', '.', regex=True)
    df_aemet['velmedia'] = df_aemet['velmedia'].replace(',', '.', regex=True)
    df_aemet['racha'] = df_aemet['racha'].replace(',', '.', regex=True)
    df_aemet['sol'] = df_aemet['sol'].replace(',', '.', regex=True)
    df_aemet['tmax'] = df_aemet['tmax'].replace(',', '.', regex=True)
    df_aemet['tmin'] = df_aemet['tmin'].replace(',', '.', regex=True)

    # Replace Ip values with 0
    df_aemet = df_aemet.replace('Ip', 0, inplace=False, regex=True, limit=None)
    df_aemet = df_aemet.replace('Varias', 0, inplace=False, regex=True, limit=None)
    df_aemet = df_aemet.replace('Acum', 0, inplace=False, regex=True, limit=None)
    aemet_data = df_aemet.replace('Ip', 0, inplace=False, regex=True, limit=None)

    # Convert data types to float
    aemet_data['tmed'] = aemet_data['tmed'].astype(float)
    aemet_data['prec'] = aemet_data['prec'].astype(float)
    aemet_data['velmedia'] = aemet_data['velmedia'].astype(float)
    aemet_data['racha'] = aemet_data['racha'].astype(float)
    aemet_data['sol'] = aemet_data['sol'].astype(float)
    aemet_data['tmax'] = aemet_data['tmax'].astype(float)
    aemet_data['tmin'] = aemet_data['tmin'].astype(float)
    aemet_data['fecha'] = pd.to_datetime(aemet_data['fecha'])




    return aemet_data



def predictions_preprocessing(df_embalse, historic_data, alias):

    historic_data = historic_data.loc[historic_data['embalse'] == alias]
    embalse = df_embalse[(df_embalse['EMBALSE_NOMBRE'] == alias)]
    embalse['AGUA_TOTAL'] = embalse['AGUA_TOTAL'].replace(',', '.', regex=True)
    embalse['AGUA_ACTUAL'] = embalse['AGUA_ACTUAL'].replace(',', '.', regex=True)
    embalse['AGUA_TOTAL'] = embalse['AGUA_TOTAL'].astype(float)
    embalse['AGUA_ACTUAL'] = embalse['AGUA_ACTUAL'].astype(float)
    embalse['TARGET'] = (embalse['AGUA_ACTUAL'] / embalse['AGUA_TOTAL']) * 100
    embalse['date'] = pd.to_datetime(embalse['FECHA'])
    agua_total = embalse.iloc[0]['AGUA_TOTAL']
    embalse = embalse.drop(['AGUA_TOTAL', 'AGUA_ACTUAL', 'AMBITO_NOMBRE', 'EMBALSE_NOMBRE', 'ELECTRICO_FLAG', 'FECHA'],
                            axis=1)


    historic_data['date'] = pd.to_datetime(historic_data['fecha'])
    nao_data = pd.read_csv("https://ftp.cpc.ncep.noaa.gov/cwlinks/norm.daily.aao.cdas.z700.19790101_current.csv")

    nao_date = pd.to_datetime(nao_data[["year", "month", "day"]]).values
    nao_data["date"] = nao_date
    nao_data = nao_data.drop(['year', 'month', 'day'], axis=1)
    df = pd.merge(embalse, historic_data, on='date')
    df = pd.merge(df, nao_data, on='date')
    df = df.drop(['fecha'], axis=1)

    dates = []
    for i in range(0, df['date'].size):
        try:
            dates.append(time.mktime(df['date'][i].timetuple()))
        except Exception as e:
            print(e)

    df = df.fillna(0)
    df['date'] = dates




    return df, agua_total


pd.set_option('display.max_columns', None)

def generate_model(model, municipality):
    # each number represents a specific model: 1 = random forest,  2 = lasso ,  3 = decision tree
    # if day 6 or 7 have null values is better not to predict them
    # prediction_data dataframe which contains the data of the days to predict
    # df contains the dataframes to trai

    centrales = [{'Central': 'Central de Aldeadávila', 'Alias': 'Aldeadávila', 'ID': '37014', 'provincia': 'Salamanca'},
                 {'Central': 'Central José María de Oriol', 'Alias': 'Alcántara', 'ID': '10008', 'provincia': 'Cáceres'},
                 {'Central': 'Central de Villarino', 'Alias': 'Almendra', 'ID': '37364', 'provincia': 'Salamanca'},
                 {'Central': 'Central de Cortes-La Muela', 'Alias': 'La Muela', 'ID': '46099', 'provincia': 'Valencia'},
                 {'Central': 'Central de Saucelle', 'Alias': 'Saucelle', 'ID': '37302', 'provincia': 'Salamanca'},
                 {'Central': 'Cedillo', 'Alias': 'Cedillo', 'ID': '10062', 'provincia': 'Caceres'},
                 {'Central': 'Estany-Gento Sallente', 'Alias': 'Sallente', 'ID': '25227', 'provincia': 'Lleida'},
                 {'Central': 'Central de Tajo de la Encantada', 'Alias': 'Conde Guadalhorce', 'ID': '29012', 'provincia': 'Málaga'},
                 {'Central': 'Central de Aguayo', 'Alias': 'Alsa', 'ID': '39070', 'provincia': 'Cantabria'},
                 {'Central': 'Mequinenza', 'Alias': 'MEQUINENZA', 'ID': '50165', 'provincia': 'Zaragoza'},
                 {'Central': 'Mora de Luna', 'Alias': 'Barrios de Luna', 'ID': '24012', 'provincia': 'León'}]

    for i in centrales:
        if i.get('Central') == municipality:
            embalseAlias = i.get('Alias')
            provincia = i.get('provincia')

    historic_data = pd.read_csv('./data/aemet_data.csv', sep=',')
    embalse = pd.read_csv('./data/embalses.csv', sep=';')
    prediction_data = aemet_predictions.select_municipality(municipality)
    df, agua_total = predictions_preprocessing(embalse, historic_data, embalseAlias)





    df = df.drop(['embalse','indicativo', 'nombre', 'provincia'], axis=1)
    prediction_data = prediction_data.dropna()
    prediction_data['aao_index_cdas'] = aemet_predictions.nao_predictions()


    # Establish the target
    X = df.drop('TARGET', axis=1)
    Y = df['TARGET']
    # Split the data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    if model == 1:
        # Create an object of the model Random Forest with 100 trees
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        # Train the model on training data
        rf.fit(X_train, y_train)
        prediccion = rf.predict(prediction_data)

    elif model == 2:

        lasso = Lasso(alpha=0.1)
        lasso.fit(X_train, y_train)

        prediccion = lasso.predict(prediction_data)


    else:

        dtree = DecisionTreeRegressor(max_depth=7)
        # fit the model
        dtree.fit(X_train, y_train)

        prediccion = dtree.predict(prediction_data)


    return prediccion, agua_total, provincia


#generate_model(2, "Central de Aldeadávila")