import pymysql
import random
import datetime
from time import ctime
import os
import ntplib
import time

class DataBase :
    def __init__(self):
        self.connection = pymysql.connect("localhost","root","","xhumaru")
        self.cursor = self.connection.cursor()

        print("Conexión establecida")

    def insertar (self,idd,firma,latitud,longitud,fecha,hora,variable,valor):
        mySql_insert_query = """INSERT INTO practica6 ( id,firma,latitud,longitud,fecha,hora,variable,valor) 
                                VALUES (%s, md5(%s), %s, %s, %s, %s, %s, %s) """
        recordTuple = (idd,firma,latitud,longitud,fecha,hora,variable,valor)
        self.cursor.execute(mySql_insert_query, recordTuple)
        self.connection.commit()
        print("Registro insertado correctamente")

    def close(self):
        self.connection.close()

def generar_cadena(tam,caracteres):
    cadena = ""
    
    for ciclo in range(0,tam):
        cadena = cadena + random.choice(caracteres)
    return cadena

    
class SetHora:
    def __init__(self):
        self.miHora = " "
        servidor_de_tiempo = "pool.ntp.org"
        cliente_ntp = ntplib.NTPClient()
        respuesta = cliente_ntp.request(servidor_de_tiempo)
        hora_actual = datetime.datetime.strptime(ctime(respuesta.tx_time), "%a %b %d %H:%M:%S %Y")
        separador = " "
        sep = str(hora_actual).split(separador)
        

        fecha = sep[0]
        hora = sep[1]
        fechass = fecha.split("-")
        anio = fechass[0]
        mes = fechass[1]
        dia = fechass[2]
        horasrr = hora.split(":")
        fhora = horasrr[0]
        fmin = horasrr[1]
        self.miHora = str(hora_actual)
        print(self.miHora)
        finalDate = 'date -u ' + mes + dia + fhora + fmin + anio
        os.system(finalDate)
       
def insertarDatos(cadena):
    dataBase = DataBase()
    miDate = SetHora()
    carNum = "0123456789"
    temperatura = generar_cadena(2,carNum)
    print("\nGeneracion de Firma Digital")
    print("\Firma Digital " + cadena)
    print("\Temperatura " + temperatura)
    fecha = miDate.miHora
    dataBase.insertar('temperatura_01',cadena,'19.721830','-101.185828',fecha,'-6','temperatura',temperatura)
    dataBase.close()
    time.sleep(5)


caracteres = "abcdefghijlmnñopqrs0987654321"
cadena = generar_cadena(16,caracteres)
while True:
    insertarDatos(cadena)







