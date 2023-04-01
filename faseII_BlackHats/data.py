import datetime
import json
import os
import time
from datetime import date, datetime, timedelta, time as date_time
import random
import requests
import pandas as pd
from zipfile import ZipFile
import pypyodbc
import aemet_predictions
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
import warnings

warnings.filterwarnings('ignore')

#############################################################################################
# Downloads the zip from the url
def zip_download(url, save_path, chunk_size=128):
    # accesing the downloading url
    r = requests.get(url, stream=True)
    # opens the file which will contain the zip
    with open(save_path, 'wb') as fd:
        # reads the content of the zip by chunks
        for chunk in r.iter_content(chunk_size=chunk_size):
            # and loads the file
            fd.write(chunk)


# Get the file .mdb from the zip
def fileFromZip(ziptoread, fileToOpen):
    # the system loads the zip file
    with ZipFile(ziptoread, 'r') as zip:

        # the fileToOpen (the mdb file) gets unziped and stored in the data file
        zip.extract(fileToOpen, './data/')



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



def get_dam():
    # opens the "Hidroelectrica.json" and returns a dictionary with its corresponding values
    with open('./data/Hidroelectrica.json') as json_file:
        dict = json.load(json_file)
    return dict




# check if there is new info on the embalses DB
def updateData():

    # the embalses zip gets downloaded
    zip_download(
        'https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/bd-embalses_tcm30-538779.zip',
        './data/bbdd_embalses.zip')

    # unzips the DB from the zip file and converts it into a csv
    fileFromZip('./data/bbdd_embalses.zip', 'BD-Embalses.mdb')
    bbddToCsv('./data/BD-Embalses.mdb', 'T_Datos Embalses 1988-2023', './data/embalses2.csv')

    # variables to compare the size of the old csv and the recently downloaded one
    file_old = os.path.getsize("./data/embalses.csv")
    file_new = os.path.getsize("./data/embalses2.csv")

    # if the embalses file exists
    if os.path.exists("./data/embalses.csv"):
        # compare files size, if the new csv is larger than the old one, then there's new data
        if file_new > file_old:
            # the old file gets deleted and replaced by the new data
            os.remove("./data/embalses.csv")
            # rename new file from embalses2.csv to embalses.csv
            os.rename("./data/embalses2.csv", "./data/embalses.csv")

        else:
            # deleted new csv because there was no new data
            os.remove("./data/embalses2.csv")
    else:
        #if there wasn't a file of embalses, then the downloaded file becomes the main one
        os.remove("./data/embalses.csv")
        # rename new file name from embalses2.csv to embalses.csv
        os.rename("./data/embalses2.csv", "./data/embalses.csv")

# method to obtain the climatic data for every dam
def get_aemet_data_embalse(embalse, idema, last_date_dataframe, date_delta):

    # declares the dataframe which will contain the csv info. And the api_key to access the AEMET API
    df = pd.DataFrame()
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtdHJnb21lejAwQGdtYWlsLmNvbSIsImp0aSI6IjEzODdkM2VkLWFkODItNGYxYy1iNThlLWU3Mzg3MjM4OWExOSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjY2NjAxMTM4LCJ1c2VySWQiOiIxMzg3ZDNlZC1hZDgyLTRmMWMtYjU4ZS1lNzM4NzIzODlhMTkiLCJyb2xlIjoiIn0.jZclNltVxWR1_zn4MN-8xzTYNhpIyWK_70altWc-aks'

    # if the difference of dates is higher than 1000, then the it means that the dam is not on the csv
    if (date_delta > 1000):
        # takes the data from 1988 to 2023, by blocks of 3 years
        for year in range(1988, 2024, 3):
            try:
                # Accessing the api passing the annual dates and the api key to the request
                url = requests.get(
                    'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/' + str(
                        year) + '-01-01T00:00:00UTC/fechafin/' + str(year + 3) + '-12-31T23:59:59UTC/estacion/' + idema,
                    params={'api_key': api_key}).json()
                datos = url['datos']

                datos_response = requests.get(datos, headers={'api_key': api_key}, params={'api_key': api_key})

                time.sleep(2)

                # the data comes in a json
                datos_data = datos_response.json()

                # then transformed into a pandas dataframe, and appending it to the existing dataframe
                df_year = pd.DataFrame(datos_data)
                df = pd.concat([df, df_year], axis=0)
            except Exception as e:
                print(e)
    # the csv file is updated from the last day to today
    else:
        try:
            #
            end_date = date.today()
            last_date_datetime = datetime.combine(last_date_dataframe, date_time.min)
            last_date_datetime = (last_date_datetime + timedelta(days=1)).date()
            # Accessing the api passing the annual dates and the api key to the request
            url = requests.get(
                'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/' + str(
                    last_date_datetime) + 'T00:00:00UTC/fechafin/' + str(end_date) + 'T23:59:59UTC/estacion/' + idema,
                params={'api_key': api_key}).json()
            datos = url['datos']

            datos_response = requests.get(datos, headers={'api_key': api_key}, params={'api_key': api_key})

            time.sleep(2)

            # the data comes in a json
            datos_data = datos_response.json()

            # then transformed into a pandas dataframe, and appending it to the existing dataframe
            df_year = pd.DataFrame(datos_data)
            df = pd.concat([df, df_year], axis=0)
        except:
            pass

    # add embalse column to the dataframe
    df['embalse'] = embalse
    # read csv with all embalse data
    df_aemet = pd.read_csv('./data/aemet_data.csv', sep=',')
    # concat the new data
    df_aemet = pd.concat([df_aemet, df], axis=0)
    # sort the data by embalse and date
    df_aemet = df_aemet.sort_values(['embalse', 'fecha'], ascending=True)
    # fix the dataframa objects to the correct type
    df_aemet = dataframe_preprocessing(df_aemet)
    # save the data
    df_aemet.to_csv("./data/aemet_data.csv", index=False, encoding='utf-8-sig', sep=',')

def update_aemet_data():
    # get all the dams
    embalses = get_dam()
    for embalse in embalses:
        # read the csv with all the data
        df_aemet = pd.read_csv('./data/aemet_data.csv', sep=',')
        # filter the data by the dam
        df_embalse_alcantara = df_aemet[df_aemet["embalse"] == embalse['Hidroeléctrica']]

        # check if the dam is on the csv file, if not, then download the data about the dam
        if (len(df_embalse_alcantara) != 0):
            # get the last data date of the dam
            last_value = df_embalse_alcantara.iloc[-1]['fecha']
            # get the difference of days between the last date and today
            today_date = date.today()
            # if had difference of dates then download the data from the last date to today
            if last_value != today_date:
                fecha = datetime.strptime(last_value, "%Y-%m-%d").date()
                diferencia_dias = (fecha - today_date).days
                # api request from the last day to today
                get_aemet_data_embalse(embalse['Hidroeléctrica'], embalse['Indicativo'], fecha, diferencia_dias)
        else:
            # if the dam is not on the csv file, then download all the data from 1988 to 2023
            get_aemet_data_embalse(embalse['Hidroeléctrica'], embalse['Indicativo'], 0, 99999)



# preprocess the data from the downloaded csv
def dataframe_preprocessing(df_aemet):

    # the following columns are drop due to irrelevance for the model
    df_aemet = df_aemet.drop(['dir', 'altitud', 'horatmax', 'horaracha',
                              'horatmin', 'horaPresMax', 'horaPresMin', 'presMax', 'presMin'], axis=1)

    # the string data modified to function as floats
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



    # returns the dataframe preprocessed
    return aemet_data


# preprocessing the data for predictions
def predictions_preprocessing(df_embalse, historic_data, alias):

    # gets just the data from the desired dam alias
    historic_data = historic_data.loc[historic_data['embalse'] == alias]
    embalse = df_embalse[(df_embalse['EMBALSE_NOMBRE'] == alias)]
    # replacing the values to get read as floats
    embalse['AGUA_TOTAL'] = embalse['AGUA_TOTAL'].replace(',', '.', regex=True)
    embalse['AGUA_ACTUAL'] = embalse['AGUA_ACTUAL'].replace(',', '.', regex=True)
    embalse['AGUA_TOTAL'] = embalse['AGUA_TOTAL'].astype(float)
    embalse['AGUA_ACTUAL'] = embalse['AGUA_ACTUAL'].astype(float)
    # the target is the percentage of water that the dam has froma a certain day
    embalse['TARGET'] = (embalse['AGUA_ACTUAL'] / embalse['AGUA_TOTAL']) * 100
    embalse['date'] = pd.to_datetime(embalse['FECHA'])
    # store the total water of the dam and drops the irrelevant columns for the model and changes the date to unix
    agua_total = embalse.iloc[0]['AGUA_TOTAL']
    embalse = embalse.drop(['AGUA_TOTAL', 'AGUA_ACTUAL', 'AMBITO_NOMBRE', 'EMBALSE_NOMBRE', 'ELECTRICO_FLAG', 'FECHA'],
                            axis=1)
    historic_data['date'] = pd.to_datetime(historic_data['fecha'])

    # using the NAO index to predict the water level of the dams
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
