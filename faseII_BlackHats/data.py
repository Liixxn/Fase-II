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
        #zip_ref.extract('otro_archivo.txt', 'archivos_extraidos/')
        zip.extract(fileToOpen,'./data/')
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
    zip_download('https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/bd-embalses_tcm30-538779.zip','./data/bbdd_embalses.zip')
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

    if (date_delta>1000):
        print("mayor de mil")
        for year in range(1988, 2024, 3):
            try:
                url = requests.get(
                    'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/' + str(
                        year) + '-01-01T00:00:00UTC/fechafin/' + str(year+3) + '-12-31T23:59:59UTC/estacion/' + idema,
                    params={'api_key': api_key}).json()
                datos = url['datos']

                datos_response = requests.get(datos, headers={'api_key': api_key}, params={'api_key': api_key})

                time.sleep(2)

                datos_data = datos_response.json()

                df_year = pd.DataFrame(datos_data)
                df = pd.concat([df,df_year], axis = 0)
            except Exception as e:
                print(e)
    else:
        try:
            end_date = date.today()
            last_date_datetime = datetime.combine(last_date_dataframe, date_time.min)
            last_date_datetime = (last_date_datetime + timedelta(days=1)).date()
            url = requests.get(
                'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/' + str(
                    last_date_datetime  ) + 'T00:00:00UTC/fechafin/' + str(end_date) + 'T23:59:59UTC/estacion/' + idema,
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
    df_aemet = pd.read_csv('./data/aemet_data.csv', sep=';')
    df_aemet = pd.concat([df_aemet, df], axis=0)
    df_aemet = df_aemet.sort_values(['embalse','fecha'], ascending = True)
    df_aemet.to_csv("./data/aemet_data.csv", index=False, encoding='utf-8-sig', sep=';')



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
        df_aemet = pd.read_csv('./data/aemet_data.csv', sep=';')
        print(df_aemet)
        print(embalse)
        df_embalse_alcantara = df_aemet[df_aemet ["embalse"] == embalse['Hidroeléctrica']]
        print(df_embalse_alcantara)
        if(len(df_embalse_alcantara)!=0):
            last_value = df_embalse_alcantara.iloc[-1]['fecha']
            today_date = date.today()
            if last_value != today_date:
                fecha = datetime.strptime(last_value, "%Y-%m-%d").date()
                diferencia_dias = (fecha - today_date).days
                # api request from the last day to today
                print(last_value)
                get_aemet_data_embalse(embalse['Hidroeléctrica'], embalse['Indicativo'], fecha, diferencia_dias)
        else:
            get_aemet_data_embalse(embalse['Hidroeléctrica'], embalse['Indicativo'], 0, 99999)




#updateData()


#update_aemet_data()


#get_aemetData()
#updateData()