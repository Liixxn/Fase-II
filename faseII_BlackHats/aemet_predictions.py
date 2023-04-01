import time
import requests
import pandas as pd
from datetime import datetime


# ---------- SELECT MUNICIPALITY -------
def select_municipality(municipality):
    # list of the municipalities
    centrales = [{'Central': 'Central de Aldeadávila', 'Alias': 'Aldeadávila', 'ID': '37014'},
                 {'Central': 'Central José María de Oriol', 'Alias': 'Alcántara', 'ID': '10008'},
                 {'Central': 'Central de Villarino', 'Alias': 'Almendra', 'ID': '37364'},
                 {'Central': 'Central de Cortes-La Muela', 'Alias': 'La Muela', 'ID': '46099'},
                 {'Central': 'Central de Saucelle', 'Alias': 'Saucelle', 'ID': '37302'},
                 {'Central': 'Cedillo', 'Alias': 'Cedillo', 'ID': '10062'},
                 {'Central': 'Estany-Gento Sallente', 'Alias': 'Sallente', 'ID': '25227'},
                 {'Central': 'Central de Tajo de la Encantada', 'Alias': 'Conde Guadalhorce', 'ID': '29012'},
                 {'Central': 'Central de Aguayo', 'Alias': 'Alsa', 'ID': '39070'},
                 {'Central': 'Mequinenza', 'Alias': 'MEQUINENZA', 'ID': '50165'},
                 {'Central': 'Mora de Luna', 'Alias': 'Barrios de Luna', 'ID': '24012'}]
    # get the central ID
    for i in centrales:
        if i.get('Central') == municipality:
            municipio = i.get('ID')
    return data(municipio)


# ----------PRECIPITATION DATAFRAME-------
def precipitacion(diccionario):
    # variable for the precipitation
    precipitacion = {}
    pre = pd.DataFrame()
    pre['prec'] = None
    pre['date'] = None
    date = []
    prec = []

    # get the precipitation
    for i in diccionario:
        total = 0
        precipitacion['prec'] = i['probPrecipitacion']
        precipitacion['fecha'] = i['fecha']
        date.append(precipitacion['fecha'])
        if (precipitacion['fecha'] == i['fecha']):
            for n in precipitacion['prec']:
                total = total + n['value']
            prec.append(float(total))
    pre['prec'] = prec
    pre['date'] = date
    # return the precipitation
    return pre


# ------VELOCITY DATAFRAME-------
def velmedia(diccionario):
    # variable for the velocity
    viento = {}
    velmedia = pd.DataFrame()
    velmedia['velmedia'] = None
    velmedia['date'] = None
    date = []
    vel = []

    # get the velocity
    for i in diccionario:
        total = 0
        iterador = 0
        viento['viento'] = i['viento']
        viento['fecha'] = i['fecha']
        date.append(viento['fecha'])
        if (viento['fecha'] == i['fecha']):
            for n in viento['viento']:
                total = total + n['velocidad']
                iterador = iterador + 1
            media = total / iterador
            vel.append(media)

    velmedia['velmedia'] = vel
    velmedia['date'] = date
    # return the velocity
    return velmedia


# ------TEMPERATURE DATAFRAME----------
def temperatura(diccionario):
    # variable for the temperature
    temperatura = {}
    tmax = []
    tmin = []
    tmed = []
    med = 0
    date = []
    temp = pd.DataFrame()
    temp['tmax'] = None
    temp['tmin'] = None
    temp['tmed'] = None
    temp['date'] = None

    # get the temperature
    for i in diccionario:
        total = 0
        iterador = 0
        temperatura['tmax'] = i['temperatura']['maxima']
        temperatura['tmin'] = i['temperatura']['minima']
        temperatura['tmed'] = i['temperatura']['dato']
        temperatura['fecha'] = i['fecha']
        date.append(temperatura['fecha'])
        if (temperatura['fecha'] == i['fecha']):
            tmax.append(float(temperatura['tmax']))
            tmin.append(float(temperatura['tmin']))
            for n in temperatura['tmed']:
                total = total + n['value']
                iterador = iterador + 1
            if (iterador != 0 and total != 0):
                med = total / iterador
            else:
                med = 0
            tmed.append(med)
    temp['tmax'] = tmax
    temp['tmin'] = tmin
    temp['tmed'] = tmed
    temp['date'] = date

    # return the temperature
    return temp


# ----PERIOD DATAFRAME--------
def racha(diccionario):
    # variable for the period
    rachamax = {}
    date = []
    racha = []
    rach = pd.DataFrame()
    rach['racha'] = None
    rach['date'] = None

    # get the period
    for i in diccionario:
        suma = 0
        iterador = 0
        rachamax['racha'] = i['rachaMax']
        rachamax['date'] = i['fecha']
        date.append(rachamax['date'])
        if (rachamax['date'] == i['fecha']):
            for n in rachamax['racha']:
                if (n['value'] != ''):
                    suma = suma + int(n['value'])
                iterador = iterador + 1
            media = suma / iterador
            racha.append(media)
    rach['racha'] = racha
    rach['date'] = date
    # return the period
    return rach


# ------SUN DATAFRAME-------
def estadoCielo(diccionario):
    # variable for the sun
    estadoCielo = {}
    fecha = []
    despejado = []
    sol = pd.DataFrame()
    sol['sol'] = None
    sol['date'] = None
    # get the sun
    for i in diccionario:
        total = 0
        estadoCielo['sol'] = i['estadoCielo']
        estadoCielo['date'] = i['fecha']
        fecha.append(estadoCielo['date'])

        if (estadoCielo['date'] == i['fecha']):
            for n in estadoCielo['sol']:
                try:
                    if (n['descripcion'] == 'Despejado'):
                        horas = n['periodo']
                        num = horas.split('-')
                        total = int(num[1]) - int(num[0])
                except:
                    total = 0
        despejado.append(float(total))

    sol['sol'] = despejado
    sol['date'] = fecha
    # return the sun
    return sol


# -----------DATAFRAME CREATE-----------
def dataframe(datos):
    #
    diccionario = datos[0]['prediccion']['dia']

    # generate dataframe for each variable
    sol = estadoCielo(diccionario)
    rach = racha(diccionario)
    temp = temperatura(diccionario)
    viento = velmedia(diccionario)
    prec = precipitacion(diccionario)

    # merge all dataframes
    df = sol.merge(rach)
    df = df.merge(temp)
    df = df.merge(viento)
    df = df.merge(prec)
    dates = []
    # convert date to timestamp
    for i in range(0, df['date'].size):
        date_t = df['date'][i].split('T')
        df_date = datetime.strptime(date_t[0], '%Y-%m-%d').date()
        dates.append(time.mktime(df_date.timetuple()))
    df = df.fillna(0)
    df['date'] = dates

    # select only the columns we need
    df = df[['date', 'tmed', 'prec', 'tmin', 'tmax', 'velmedia', 'racha', 'sol']]
    return df


# ------DATAFRAME NAO PREDICTIONS -------
def nao_predictions():
    # get the NAO index
    nao = pd.read_csv('https://ftp.cpc.ncep.noaa.gov/cwlinks/norm.daily.aao.gefs.z700.120days.csv')
    # get the latest day and valid time
    latest_day = nao['time'].max()
    latest_valid = nao['valid_time'].max()
    nao = nao[nao['time'] == latest_day]
    nao = nao[nao['valid_time'] == latest_valid]
    # get the mean of the NAO index
    mean_aao_index = nao['aao_index'].mean()

    return mean_aao_index


# -----------GET AEMET DATA-------------
def data(id_municipio):
    # AEMET API
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtdHJnb21lejAwQGdtYWlsLmNvbSIsImp0aSI6IjEzODdkM2VkLWFkODItNGYxYy1iNThlLWU3Mzg3MjM4OWExOSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjY2NjAxMTM4LCJ1c2VySWQiOiIxMzg3ZDNlZC1hZDgyLTRmMWMtYjU4ZS1lNzM4NzIzODlhMTkiLCJyb2xlIjoiIn0.jZclNltVxWR1_zn4MN-8xzTYNhpIyWK_70altWc-aks'
    url_aemet_prediction = requests.get(
        "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/" + str(id_municipio))
    url_aemet_prediction.headers['api_key'] = api_key
    url_aemet_prediction = requests.get(
        "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/" + str(id_municipio),
        headers={'api_key': api_key})
    # format data
    data = url_aemet_prediction.json()
    # get data
    data = data['datos']
    url = requests.get(data)
    datos = url.json()

    # return a dataframe with the data
    return dataframe(datos)


