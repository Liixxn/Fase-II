import json
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

#############################################################################################



"""
-Tener todos los idemas de las hidroeletricas
-Comprobar si esta ese csv actualizado con la fecha de hoy
-De no ser la fecha de hoy hacer una peticion a la api con la ultima fecha en el csv hasta hoy 
    -unir esos datos con los datos que estan en el csv, cargarlos en el dataframe y agregarlos
-guardar el csv 
"""
idemas = ['3526X','2916A']

for i in idemas:






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

    import os
    file_old = os.path.getsize("./data/embalses.csv")
    file_new = os.path.getsize("archivo2.txt")

    # compare file size
    if file_new > file_old:
