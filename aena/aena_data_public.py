#!/usr/bin/env python
# coding: utf-8

# <a id='Index'></a>

# ### <font color='blue'>Índice</font>
# 
# Este Jupyter Notebook consta de los siguientes apartados:
# 
# 1) [Introducción al Notebook aena_dataset](#Section0)<br>
# 2) [Glosario de Variables y Constantes](#Section1)<br>
# 3) [Código Principal](#Section2)<br>
# 4) [Últimos ajustes](#Section3)<br>
# 5) [Creación del archivo csv/xls](#Section4)<br>
# 6) [Actualización del archivo csv/xls](#Section5)<br>
# 7) [Visualización de datos](#Section6)
# 

# <a id='Section0'></a>

# ### <font color='blue'>Introducción al Notebook aena_dataset</font>
# 
# Aena publica mensualmente en su web (tanto en archivo excel como en PDF), los datos del tráfico aéreo de pasajeros, operaciones y mercancías (kg) en los aeropuertos españoles gestionados por ellos (o alguna de sus filiales). Estos datos se remontan a 2004.
# 
# A la hora de querer usar estos datos para crear nuestros gráficos, ver tendencias por temporada o la progresión en el tiempo de algún aeropuerto en concreto, tal y como están presentados los datos resulta complejo de realizar. Es por ello que hemos creado este código de python; el objetivo es crear un archivo que aune todos los datos otorgados por Aena y, sobretodo, estructurarlo y ordenarlo para facilitar su uso posterior. El archivo 'salida' es un archivo .csv (también añadimos la opción de obtener una hoja de excel, si bien pasar de uno a otro no debería suponer ningun problema), que se puede utilizar para visualizar datos, alimentar una Base de Datos o usarlo en algún software de análisis de datos, entre otras cosas.
# 
# Para lograr este fin, la herramienta utilizada es Jupyter Notebook (un IDE de Python). Además del archivo .csv/xls mencionado, también se facilita el Notebook (tanto en formato .ipynb como en .py), por si alguno de los lectores se maneja con este lenguaje de programación y quiere 'trastear'. Todo comentario al respecto es bienvenido y espero que le sea útil o interesante a alguien.
# 
# PD. Los datos recogidos son desde 2010, ya que las hojas excel de años anteriores dan problemas con el código (se tratará de solventar este problema para tener todos los datos desde 2004).<br>
# PD2. El código se irá revisando con frecuencia para su optimización.
# 
# [Volver al índice](#Index)

# <a id='Section1'></a>

# ### <font color="blue">Glosario de Variables y Constantes</font>
# 
# 1) <b>month</b>: Lista con los meses del año<br>
# 2) <b>year</b>: Lista de strings numéricos que relacionan los años desde 2010 con su orden secuencial<br>
# 3) <b>root_dict</b>: Diccionario cuyos valores son listas de tuplas. Necesario para obtener los links de Aena sin web scraping<br>
# 4) <b>url_aena</b>: Es una lista de los links de Aena, que se construye por una iteración de concatenación de strings<br>
# 5) <b>traffic_df</b>: Primer DataFrame en aparecer. Es el DataFrame en bruto de cada excel de Aena<br>
# 6) <b>dataset</b>: Es una función que realiza una serie de transformaciones para obtener el DataFrame 'pulido'.<br>
# 7) <b>dataset_net</b>: Previa a la creación del archivo .csv se requiere hacer unos reemplazos por inconsistencia en los datos de Aena<br>
# 8) <b>aena_dataset</b>: Es el DataFrame salida de las funciones dataset y dataset_net. Es el que vamos a usar para visualización de datos, manipulación, transformación, etc.
# 
# [Volver al índice](#Index)

# <a id='Section2'></a>

# ### <font color='Blue'>Código Principal</font>
# 
# A continuación se presenta el Código Principal de este Notebook. Para realizar las transformaciones necesarias, primero hay que idear un método de obtención de los datos desde la página web de Aena.
# 
# [Volver al índice](#Index)

# In[ ]:


#####################################################################
#Cargamos las librerias que vamos a utilizar para el Código Principal
#####################################################################

import pandas as pd
import calendar
import locale


# In[ ]:


#############################
#Definimos algunas constantes
#############################

locale.setlocale(locale.LC_ALL, 'es_ES')

year = []
for i in range(11):
    year.append(str(2010 + i))
month = []
for i in range(13):
    month.append(calendar.month_name[i].capitalize())
month.pop(0)

###############################################################################################################################
#La siguiente variable es necesaria si no consideramos web scraping. Son números que aparecen en las urls de Aena y que no 
#siguen ningún orden que podamos automatizar
###############################################################################################################################

root = [[(8,1012),(751,810),(336,99),(688,180),(43,295),(957,890),(384,673),(653,407),(855,829),(1023,205),(391,623),
        (191,1022)],[(905,889),(624,688),(209,1001),(561,58),(940,172),(830,768),(257,551),(526,285),(728,707),(896,83),
        (264,501),(64,900)],[(438,866),(221,786),(766,984),(94,958),(407,476),(747,816),(814,48),(825,34),(899,331),
        (493,371),(821,579),(621,955)],[(1005,529),(531,7),(307,682),(658,160),(456,1019),(285,53),(351,838),(845,254),
        (504,562),(582,762),(589,651),(516,526)],[(529,560),(683,5),(523,609),(972,716),(866,146),(737,1023),(95,819),
        (189,287),(178,329),(792,174),(689,836),(794,238)],[(754,192),(845,124),(178,74),(692,915),(441,589),(903,996),
        (454,860),(753,107),(965,148),(599,94),(981,649),(667,360)],[(819,681),(910,613),(1007,255),(625,431),(314,467),
        (776,874),(327,738),(626,1009),(838,26),(472,996),(370,274),(540,238)],[(692,559),(783,491),(48,745),(690,920),
        (379,956),(841,339),(392,203),(691,474),(903,515),(537,461),(435,763),(605,727)],[(565,437),(656,369),(945,622),
        (311,663),(252,834),(714,217),(265,81),(564,352),(776,393),(410,339),(308,641),(478,605)],[(438,315),(529,247),
        (818,500),(436,676),(125,712),(587,95),(138,983),(437,230),(649,271),(283,217),(181,519),(351,483)],[(424,132),
        (79,556),(912,375),(80,325),(937,665),(227,647),(800,817),(587,699),(917,183),(815,717)]]
root_dict = dict(zip(year,root))


# In[ ]:


##########################################################################################################################
#Creamos una lista con las rutas de los excel que contienen los datos. El hecho de que las rutas que otorga Aena no sigan
#siempre el mismo patrón año tras año (incluso dentro de un mismo año), es lo que nos lleva a una definición de u_a algo
#más tediosa
##########################################################################################################################

url_aena = []

for i in range(10):
    for j in range(12):
        u_a = 'https://wwwssl.aena.es/csee/ccurl/' + str(root_dict[year[i]][j][0]) + '/' + str(root_dict[year[i]][j][1])
        if (i not in (3,4)) and (j < 9):
            u_a = u_a + '/0'
        elif (i not in (3,4) and (j >= 9)) or (i == 4):
            u_a = u_a + '/'
        if (i == 6 and j < 2) or (i > 6):
            u_a = u_a + str(j+1) + '.' + month[j] + '_Definitivo_' + year[i] + '.xls'    
        elif (i == 6 and j >=2) or (i == 5 and (j <= 9 or j == 11)):
            u_a = u_a + str(j+1) + '.' + month[j] + '-Definitivo-' + year[i] + '.xls'
        elif (i == 5 and j == 10):
            u_a = u_a + str(j+1) + '.' + month[j] + '-Definitivo-%20' + year[i] + '.xls'    
        elif i == 4:
            u_a = u_a + month[j] + '-Definitivo%20' + year[i] + '.xls'
        elif i == 3:
            u_a = u_a + '/Estadistica%20' + month[j] + '%20DEF%20' + year[i] + '.xls'            
        elif i == 2:
            u_a = u_a + str(j+1) + '.Estadisticas_' + month[j] + '%20DEF_' + year[i] + '.xls'
        elif i in (0,1):
            u_a = u_a + str(j+1) + '_Estadisticas_' + month[j] + '_' + year[i] + '.xls'
        url_aena.append(u_a)
                
i = 10
for j in range(10):
    u_a = 'https://wwwssl.aena.es/csee/ccurl/' + str(root_dict[year[i]][j][0]) + '/' + str(root_dict[year[i]][j][1]) + '/'
    if j != 2:
        u_a = u_a + str(j+1) + '.Estadisticas_' + month[j] + '_' + year[i] + '.xls'
    if j == 2:
        u_a = u_a + str(j+1) + '.Estadisticas_' + month[j] + '_' + year[i] + '%20(1)' + '.xls'
    url_aena.append(u_a)


# In[ ]:


#######################################################
#Opcional - En caso de que queramos ver un url concreto
#######################################################

#print(url_aena[0])

################################################################################
#Realizamos las transformaciones requeridas para estructurar y ordenar los datos
################################################################################

def dataset(url_aena):
    traffic_df_list = []
    c_drop = [0,1,3,5,6,9,10,13] #Columnas a eliminar del archivo origen, son siempre las mismas a diferencia de las filas
    traffic_df_net_list = []
    for j in range(len(url_aena)):
        #print(j) #-> Lo usamos para comprobación. Una vez realizada, prescindimos de este print que solo consume recursos
        traffic_df = pd.read_excel(url_aena[j])
        traffic_df_list.append(traffic_df)
    
        r_drop = [] #Filas a eliminar del archivo origen, definido más abajo
        for i in range(traffic_df_list[j].shape[0]):
            if (type(traffic_df_list[j].iloc[i,4]) != int and (traffic_df_list[j].iloc[i,4]) != '---')            or (traffic_df_list[j].iloc[i,2].upper() == 'TOTAL'):
                r_drop.append(i)
        for numbers in c_drop: 
            traffic_df_list[j] = traffic_df_list[j].drop(['Unnamed: ' + str(numbers)], axis = 1)
        for numbers in r_drop:
            traffic_df_list[j] = traffic_df_list[j].drop([numbers])
    
        value_list = []
        for i in range(3):
            value = traffic_df_list[j][[traffic_df_list[j].columns[2*i],traffic_df_list[j].columns[2*i+1]]].            sort_values([traffic_df_list[j].columns[2*i]])
            value.index = range(value.shape[0])
            value_list.append(value)
        traffic_df_net = pd.concat(value_list, axis = 1)
        traffic_df_net.insert(1,'MONTH',(j%12)+1)
        traffic_df_net.insert(2,'YEAR',year[j//12])
        traffic_df_net_list.append(traffic_df_net)

    dataset = pd.concat(traffic_df_net_list)
    dataset.columns = ('AIRPORTS','MONTH','YEAR','PAX','AIRPORTS2','MOVEMENTS','AIRPORTS3','CARGO (KG)')
    dataset = dataset.drop(['AIRPORTS2','AIRPORTS3'], axis = 1)
    dataset.index = range(dataset.shape[0])
    return dataset

aena_dataset = dataset(url_aena)
display(aena_dataset)


# <a id='Section3'></a>

# ### <font color='blue'>Últimos ajustes</font>
# 
# En la anterior celda ya podéis ver el DataFrame con todos los datos desde enero de 2010 hasta los últimos datos presentados 
# por Aena de octubre de 2020. Si bien ya podríamos crear el archivo .csv y/o .xls, hay dos pasos previos que hay que realizar debido
# a cómo están presentados los datos:
# 
# a) Al parecer, algunos datos de 2013 aparecen como '---' en lugar de '0', así que vamos a realizar dicho reemplazo.<br>
# b) Bien porque algunos aeropuertos han ido cambiando de nombre con el tiempo (como es el caso de Barajas), o bien porque
# Aena en los datos no ha mantenido tipográficamente el mismo nombre de algunos aeropuertos, vamos a realizar reemplazos de tal manera que haya una relación unívoca entre nombre y aeropuerto.
# 
# [Volver al índice](#Index)

# In[ ]:


#######################################################################################################################
#En primer lugar vamos a identificar los aeropuertos que aparecen, para solventar el problema mencionado en el punto b)
#del anterior párrafo. Luego creamos una lista con los nombres definitivos de aquellos aeropuertos que tienen más de un
#nombre en los datos de Aena y realizamos los cambios para resolver los puntos a) y b)
#######################################################################################################################

def dataset_net(dataset):
    Name_Def = ['ADOLFO SUAREZ MADRID-BARAJAS','AEROPUERTO INTL. REGION MURCIA','ALGECIRAS-HELIPUERTO','ALICANTE-ELCHE',
           'BARCELONA-EL PRAT J.T.','CEUTA-HELIPUERTO','GIRONA-COSTA BRAVA','LANZAROTE-CESAR MANRIQUE','MALAGA-COSTA DEL SOL',
           'MURCIA-SAN JAVIER','SANTIAGO-ROSALIA DE CASTRO','SEVE BALLESTEROS-SANTANDER','TENERIFE NORTE-C. LA LAGUNA',
           'TENERIFE SUR']
    Name_Alt = [['ADOLFO SUÁREZ MADRID-BARAJAS','MADRID-BARAJAS'],['AEROPUERTO INTL. REGIÓN MURCIA','AEROPUERTO INTL. REGIÓN MURCIA  (**)'],
           ['ALGECIRAS /HELIPUERTO'],['ALICANTE'],['BARCELONA','BARCELONA-EL PRAT'],['CEUTA /HELIPUERTO'],['GIRONA'],['LANZAROTE',
            'LANZAROTE CÉSAR MANRIQUE'],['MALAGA'],['MURCIA-SAN JAVIER  (*)'],['SANTIAGO','SANTIAGO-ROSALÍA DE CASTRO'],
            ['SANTANDER'],['TENERIFE NORTE','TENERIFE-NORTE'],['TENERIFE-SUR']]

    for j in range(dataset.shape[1]):
        for i in range(dataset.shape[0]):
            if dataset.iloc[i,j] == '---':
                dataset.iloc[i,j] = int(0)
            for k in range(len(Name_Def)):
                if dataset.iloc[i,j] in Name_Alt[k]:
                    dataset.iloc[i,j] = Name_Def[k]
    return dataset

aena_dataset = dataset_net(aena_dataset)
aena_dataset = aena_dataset.sort_values(['YEAR','MONTH','AIRPORTS'])
aena_dataset.index = range(aena_dataset.shape[0])


# <a id='Section4'></a>

# ### <font color='blue'>Creación del archivo csv/xls</font>
# 
# Teniendo ya el DataFrame listo, crear los archivos .csv y .xls es inmediato. Solo hay que particularizar la ruta donde vamos a almacenar los archivos.
# 
# [Volver al índice](#Index)

# In[ ]:


aena_dataset.to_csv('root/filename.csv') #Sustituir por la ruta y nombre de archivo elegido
aena_dataset.to_excel('root/filename.xls') #Sustituir por la ruta y nombre de archivo elegido


# <a id='Section5'></a>

# ### <font color='blue'>Actualización del archivo csv/xls</font>
# Para finales de la primera semana de cada mes, Aena publica un archivo excel (y un archivo PDF) con los datos del mes anterior. Si queremos actualizar nuestro archivo .csv con los nuevos datos, deberemos realizar lo siguiente:
# 
# [Volver al índice](#Index)

# In[ ]:


aena_dataset = pd.read_csv('root/filename.csv') #Sustituir por la ruta y nombre de archivo donde se encuentra

aena_dataset = aena_dataset.drop(['Unnamed: 0'], axis = 1)
airport_number_prev = len(aena_dataset['AIRPORTS'].unique())
url_aena = [] #Insertamos la url de la página de Aena con el mes que queremos añadir a nuestro archivo

aena_dataset_update = dataset(url_aena)
aena_dataset = pd.concat(aena_dataset,aena_dataset_update)

airport_number_aft = len(aena_dataset_update['AIRPORTS'].unique())
if airport_number_prev != airport_number_aft:
    print('Hay que revisar la última entrada de datos, ya faltan aeropuertos o han aumentado/disminuidoel número de aeropuertos gestionados por Aena')
else:
    dataset_net(aena_dataset)

aena_dataset.to_csv('root/filename.csv') #Sustituir por la ruta y nombre de archivo donde se encuentra
aena_dataset.to_excel('root/filename.xls') #Sustituir por la ruta y nombre de archivo donde se encuentra


# <a id='Section6'></a>

# ### <font color='blue'>Visualización de datos</font>
# 
# Como un añadido al Código Principal y al archivo de salida csv/xls, a continuación dejamos algunas de las conclusiones y/o visualizaciones de datos que podemos obtener con los datos de Aena. En algunos casos vamos a importar librerias o DataFrames que aparecen en el Código Principal; esto solo es necesario si en la sesión que os encontráis no habeís ejecutado el Código Principal.<br>
# 
# La segunda celda, justo después de importar las librerías que vamos a usar, nos va a servir para conocer el nº de aeropuertos involucrados y si ha habido aumento/disminución del número de aeropuertos desde 2010.
# 
# [Volver al índice](#Index)

# In[ ]:


###########################################################################
#Cargamos las librerias que vamos a utilizar para la visualización de datos
###########################################################################

import pandas as pd #Volvemos a cargarlo por si no estamos ejecutando el Código Principal
import math
import seaborn as sbn
import matplotlib.pyplot as plt
import numpy as np
import calendar #Volvemos a cargarlo por si no estamos ejecutando el Código Principal
import locale #Volvemos a cargarlo por si no estamos ejecutando el Código Principal


# In[ ]:


##################################################################################################################
#Si vamos a realizar solo esta parte del código (en caso de que tuvieramos previamente los datos ya cargados en un 
#archivo .csv), hay que realizar previamente lo siguiente:
##################################################################################################################

aena_dataset = pd.read_csv('root/filename.csv') #Sustituir por la ruta y nombre de archivo donde se encuentra
aena_dataset = aena_dataset.drop(['Unnamed: 0'], axis = 1)

#################################################################
#Analizamos previamente los aeropuertos involucrados en los datos
#################################################################

airports = list(aena_dataset['AIRPORTS'].unique())
print('El número de aeropuertos/helipuertos gestionados por Aena o alguna de sus filiales, desde 2010, es de',len(airports))
locale.setlocale(locale.LC_ALL, 'es_ES')
month = []
for i in range(13):
    month.append(calendar.month_name[i].capitalize())
month.pop(0)

airports_not_complete = set()
for i in range(len(airports)):
    for j in range(len(month)):
        prueba = aena_dataset[(aena_dataset['AIRPORTS'] == airports[i]) & (aena_dataset['MONTH'] == j+1)]
        if prueba.shape[0] != 11 and month[j] not in ('Noviembre','Diciembre'):
            airports_not_complete.add(airports[i])

print()
print('A los siguientes aeropuertos/helipuertos les faltan datos en algún mes o meses por falta de datos de Aena o porque', 
'no estaba operativo/gestionado por Aena',airports_not_complete)


# Por un lado hemos obtenido que desde 2010, Aena ha gestionado un total de 50 (48 aeropuertos y 2 helipuertos). Sabemos que actualmente gestiona 45 aeropuertos + el aeropuerto Internacional Región de Murcia a través de una filial + 2 helipuertos, con lo cual hay dos aeropuertos que aparecen en nuestros datos y que ya no gestiona Aena.<br>
# 
# El segundo dato obtenido son los aeropuertos/helipuertos que no tienen todos los datos desde 2010, con lo cual, de los 4 obtenidos, 2 de ellos tienen que ser los que ya no están gestionados por Aena. Analizamos cada uno:<br>
# 
# 1) <b>Aeropuerto de San Javier, Murcia</b>: Es uno de los dos aeropuertos que ya no gestiona Aena, concretamente no hay datos desde mediados de enero de 2019.<br>
# 2) <b>Aeropuerto Intl. Región de Murcia</b>: Comienza a ser gestionado por la filial de Aena en enero de 2019, coincidiendo con el cese de la gestión del Aeropuerto de San Javier.<br>
# 3) <b>Helipuerto de Algeciras</b>: Es un caso raro que aparezca aquí, ya que la ausencia de datos es en algunos meses puntuales. Desconocemos si la omisión de esos datos puntuales es por error a la hora de publicar Aena los excel o hay otro motivo.<br>
# 4) <b>Aeropuerto de Torrejón, Madrid</b>: Es el segundo aeropuerto que dejó de gestionar Aena, en enero de 2013 (hay entradas en el resto de meses de 2013 pero todos ellos nulos).

# In[ ]:


#####################################################################
#Vamos a empezar con datos pre-COVID, dejando fuera los datos de 2020
#####################################################################

##################################################################################
#¿Cuál es el top 5 de aeropuertos con mayor media de tráfico de pasajeros en 2019?
##################################################################################

pax = aena_dataset[(aena_dataset['YEAR'] == 2019) & (aena_dataset['AIRPORTS'] != 'MURCIA-SAN JAVIER')]
pax = pax[[pax.columns[0],pax.columns[3]]]
pax = pax.groupby(['AIRPORTS']).mean()
pax = pax.sort_values(['PAX'], ascending = 0)

print('Los cinco aeropuertos con mayor media mensual de PASAJEROS en 2019 fueron los de:')
for i in range(5):
    print(j+1,pax.index[i],'con',math.ceil(pax.iloc[i,0]),'pasajeros.')

####################################
#¿Lo mismo para operaciones y carga?
####################################

kind = ['MOVEMENTS','CARGO (KG)']
kind_esp = ['OPERACIONES','KG DE MERCANCIA']
for i in range(2):
    traffic = aena_dataset[(aena_dataset['YEAR'] == 2019) & (aena_dataset['AIRPORTS'] != 'MURCIA-SAN JAVIER')]
    traffic = traffic[[traffic.columns[0],traffic.columns[i+4]]]
    traffic = traffic.groupby(['AIRPORTS']).mean().astype(int)
    traffic = traffic.sort_values([kind[i]], ascending = 0)

    print()
    print('Los cinco aeropuertos con mayor media mensual de',kind_esp[i],'en 2019 fueron los de:')
    for j in range(5):
        print(j+1,traffic.index[j],'con',math.ceil(pax.iloc[j,0]),kind_esp[i])


# In[ ]:


###########################################################################
#Las mismas preguntas de antes pero ahora con los 5 aeropuertos por la cola
###########################################################################

kind = ['PAX','MOVEMENTS','CARGO (KG)']
kind_esp = ['PASAJEROS','OPERACIONES','KG DE MERCANCIA']
for i in range(3):
    traffic = aena_dataset[(aena_dataset['YEAR'] == 2019) & (aena_dataset['AIRPORTS'] != 'MURCIA-SAN JAVIER')]
    traffic = traffic[[traffic.columns[0],traffic.columns[i+3]]]
    traffic = traffic.groupby(['AIRPORTS']).mean().astype(int)
    traffic = traffic.sort_values([kind[i]], ascending = 1)
    
    print()
    print('Los cinco aeropuertos con menor media mensual de',kind_esp[i],'en 2019 fueron los de:')
    for j in range(5):
        print(j+1,traffic.index[j],'con',math.ceil(traffic.iloc[j,0]),kind_esp[i])


# In[ ]:


###############################################################################################
#¿Cuál es el aeropuerto que, en media de pasajeros, ha crecido más en el 2019 respecto de 2018?
###############################################################################################

pax = aena_dataset[((aena_dataset['YEAR'] == 2018) | (aena_dataset['YEAR'] == 2019)) &                    ((aena_dataset['AIRPORTS'] != 'AEROPUERTO INTL. REGION MURCIA') &                   (aena_dataset['AIRPORTS'] != 'MURCIA-SAN JAVIER'))]
pax = pax.drop(['MONTH','MOVEMENTS','CARGO (KG)'], axis = 1)
pax = pax.groupby(['AIRPORTS','YEAR']).sum()

var = []
for i in range(0,pax.shape[0],2):
    var_i = round((pax.iloc[i+1,0]/pax.iloc[i,0]-1)*100,2)
    var.append(var_i)
    #print('El aeropuerto',pax.index[i][0],'ha crecido/decrecido su actividad en un',var_i) ->Podéis hacer un print para ver
    #el % de crecimiento/decrecimiento que cada aeropuerto tuvo en 2019 respecto de 2018
var.index(max(var))
print('El aeropuerto que más creció en pasajeros en 2019, respecto de 2018, fue el aeropuerto de',pax.index[var.index(max(var))*2][0],      'con un crecimiento del',max(var),'%')

###################################################################
#¿Y si lo que quiero son los cinco aeropuertos que más han crecido?
###################################################################

var_s = sorted(var,reverse = 1)
var_s_indx = []
for i in range(5):
    for j in range(len(var)):
        if var_s[i] == var[j]:
            var_s_indx.append(2*j)

print()            
print('Los cinco aeropuertos/helipuertos que más han crecido en pasajeros en 2019, respecto de 2018, fueron los aeropuertos de:')
for i in range(5):
    print(i+1,pax.index[var_s_indx[i]][0],'con un crecimiento del',var_s[i],'%')


# In[ ]:


####################################################################
#Queremos ver la evolución mensual del tráfico en las islas baleares
####################################################################

ibalear = aena_dataset[(aena_dataset['YEAR'] != 2020) & ((aena_dataset['AIRPORTS'] == 'PALMA DE MALLORCA') |                                                        (aena_dataset['AIRPORTS'] == 'IBIZA') |                                                        (aena_dataset['AIRPORTS'] == 'MENORCA'))]
ibalear = ibalear.drop(['YEAR','MOVEMENTS','CARGO (KG)'], axis = 1)
plot = sbn.lineplot(x="MONTH", y="PAX", hue='AIRPORTS', data = ibalear)


# In[ ]:


####################################################################################
#Si queremos ver cómo ha afectado el COVID-19 al Aeropuerto de Adolfo Suárez-Barajas
####################################################################################

madrid = aena_dataset[((aena_dataset['YEAR'] == 2020) | (aena_dataset['YEAR'] == 2019))  & (aena_dataset['AIRPORTS'] == 'ADOLFO SUAREZ MADRID-BARAJAS')]
madrid = madrid.drop(['MOVEMENTS','CARGO (KG)'], axis = 1)
madrid = madrid.sort_values(['MONTH','YEAR'])

month_str = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre']
var = []
for i in range(0,20,2):
    var_i = round((madrid.iloc[i+1,3]/madrid.iloc[i,3]-1)*100,2)
    var.append(var_i)
#for i in range(10):
#    print('El aeropuerto Adolfo Suarez Madrid-Barajas ha crecido/decrecido su actividad en',month_str[i],'un',var[i])

plt.figure(figsize=(10, 4))
plot = sbn.lineplot(x=month_str, y=var,sort=0)
plot.set(xlabel='Meses', ylabel='Variación %')
plot.set_title('Aeropuerto Adolfo Suárez, Madrid - Evolución de Pasajeros en 2020 respecto de 2019')
plt.show()


# In[ ]:


###################################################
#La misma pregunta en cuanto al movimiento de carga
###################################################

madrid = aena_dataset[((aena_dataset['YEAR'] == 2020) | (aena_dataset['YEAR'] == 2019))  & (aena_dataset['AIRPORTS'] == 'ADOLFO SUAREZ MADRID-BARAJAS')]
madrid = madrid.drop(['PAX','MOVEMENTS'], axis = 1)
madrid = madrid.sort_values(['MONTH','YEAR'])

month_str = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre']
var = []
for i in range(0,20,2):
    var_i = round((madrid.iloc[i+1,3]/madrid.iloc[i,3]-1)*100,2)
    var.append(var_i)
#for i in range(10):
#    print('El aeropuerto Adolfo Suarez Madrid-Barajas ha crecido/decrecido su actividad en',month_str[i],'un',var[i])

plt.figure(figsize=(10, 4))
plot = sbn.lineplot(x=month_str, y=var, sort=0)
plot.set(xlabel='Meses', ylabel='Variación %')
plot.set_title('Aeropuerto Adolfo Suárez, Madrid - Evolución de Mercancías en 2020 respecto de 2019')
plt.show()


# In[ ]:




