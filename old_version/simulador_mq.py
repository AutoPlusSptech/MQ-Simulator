import random
import time
import pymysql
from datetime import datetime
import psutil
import matplotlib.pyplot as plt

connection = pymysql.connect(
    host='localhost', 
    user='user_atividePI', 
    password='sptech', 
    db='vehicle_monitoring'
)

mq7 = list(range(100, 50001, 1))
mq2 = list(range(10, 100, 1))
mq135 = list(range(10000, 20000, 1))

co = mq7[random.randint(0, 1000)]
co_i = mq7.index(co)

c3h8 = mq2[random.randint(0, 10)]
c3h8_i = mq2.index(c3h8)

co2 = mq135[random.randint(0, 300)]
co2_i = mq135.index(co2)

list_mq7 = []
list_mq2 = []
list_mq135 = []

list_carros = []

tempo_100 = []
tempo_1000 = []
tempo_10000 = []
tempo_100000 = []

memoria_100 = []
memoria_1000 = []
memoria_10000 = []
memoria_100000 = []

cpu_100 = []
cpu_1000 = []
cpu_10000 = []
cpu_100000 = []

lotes_100 = []
lotes_1000 = []
lotes_10000 = []
lotes_100000 = []

def gerar_veiculos():
    for x in range(1, 10):
        ano = random.randint(2008, 2024)
        marca = random.choice(['Fiat', 'Ford', 'Chevrolet', 'Volkswagen', 'Toyota', 'Honda', 'Hyundai', 'Renault', 'Peugeot', 'Citroen'])
        modelo = random.choice(['Uno', 'Palio', 'Siena', 'Strada', 'Toro', 'Mobi', 'Argo', 'Cronos', 'Doblò', 'Fiorino', 'Fiorino', 'Grand Siena', 'Linea', 'Punto', 'Toro', 'Uno', 'Ka', 'Fiesta', 'Focus', 'EcoSport', 'Ranger'])
        letras = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(3))
        numeros = ''.join(random.choice('0123456789') for i in range(4))
        placa = f'{letras}{numeros}'
        km = random.randint(100, 200000)
        
        with connection.cursor() as cursor:
            sql = f"INSERT INTO tbVeiculo (ano, marca, modelo, placa, km) VALUES ({ano}, '{marca}', '{modelo}', '{placa}', {km})"
            cursor.execute(sql)
            connection.commit()
            cursor.close()
            
        list_carros.append(cursor.lastrowid)
        
def insert_sensor(unidadeMedida, modelo, fkVeiculo):
    with connection.cursor() as cursor:
        consulta_sensor = "SELECT MAX(idSensor) FROM tbSensor;"
        cursor.execute(consulta_sensor)
        idSensor = cursor.fetchone()[0]
        if idSensor == None:
            idSensor = 1
        else:
            idSensor += 1
        sql = f"INSERT INTO tbSensor (idSensor, unidadeMedida, modelo, dataInstalacao, fkVeiculo) VALUES ({idSensor}, '{unidadeMedida}', '{modelo}', '{datetime.now()}', {fkVeiculo});"
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        
    return idSensor
        
def cadastro_sensor(idCarro):
    with connection.cursor() as cursor:
        sql = f"SELECT fkVeiculo FROM tbSensor WHERE fkVeiculo = {idCarro}"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
    
    if result == None:
        idmq7 = insert_sensor('ppm', 'MQ-7', idCarro)
        idmq2 = insert_sensor('ppm', 'MQ-2', idCarro)
        idmq135 = insert_sensor('ppm', 'MQ-135', idCarro)
    else:
        print(f'Sensor Cadastrado! \n{result}')
        
        with connection.cursor() as cursor:
            sql = f"SELECT idSensor FROM tbSensor WHERE fkVeiculo = {idCarro} AND modelo = 'MQ-7'"
            cursor.execute(sql)
            idmq7 = cursor.fetchone()[0]
            sql = f"SELECT idSensor FROM tbSensor WHERE fkVeiculo = {idCarro} AND modelo = 'MQ-2'"
            cursor.execute(sql)
            idmq2 = cursor.fetchone()[0]
            sql = f"SELECT idSensor FROM tbSensor WHERE fkVeiculo = {idCarro} AND modelo = 'MQ-135'"
            cursor.execute(sql)
            idmq135 = cursor.fetchone()[0]
            cursor.close()
            
    return idmq7, idmq2, idmq135

def simulate_capture(gas, sensor, idSensor, sort_variance, disturb):
    
    gas_i = sensor.index(gas)
    sort_up_down = random.randint(1,2)
    if sort_variance == 1 and disturb < 3:
        print(f'Disturbancia no sensor {gas}! valor de disturb: {disturb}')
        sort_up_down = 1
        if sensor == mq2:
            sort_x = random.randint(10,20)
        else:
            sort_x = random.randint(100,350)
            
        disturb += 1
    else:    
        if sensor == mq2:
            sort_x = random.randint(1,5)
        else:
            sort_x = random.randint(1,35)
    
    if sort_up_down == 1:
        if gas_i + sort_x > len(sensor) - 1:
            gas = sensor[len(sensor) - 1]
            print(f'Valor máximo atingido! {gas}')
            gas_i = sensor.index(gas)
        else:
            gas = sensor[gas_i + sort_x]
            gas_i = sensor.index(gas)
            print(f'Somando {sort_x} ao valor atual! {gas}')
    else:
        if gas_i - sort_x < 0:
            gas = sensor[0]
            print(f'Valor minimo atingido! {gas}')
            gas_i = sensor.index(gas)
        else:
            gas = sensor[gas_i - sort_x]
            gas_i = sensor.index(gas)
            print(f'Subtraindo {sort_x} ao valor atual! {gas}')
    
    if(sensor == mq7):
        list_mq7.append(gas)
    elif(sensor == mq2):
        list_mq2.append(gas)
    elif(sensor == mq135):
        list_mq135.append(gas)
        
    sql = f"INSERT INTO tbDadosSensor (registro, fkSensor, dtColeta) VALUES "
    sql = f"('{gas}', {idSensor}, '{datetime.now()}')"
    if len(lotes_100) < 1200:
        lotes_100.append(sql)
    elif len(lotes_1000) < 12000:
        lotes_1000.append(sql)
    elif len(lotes_10000) < 120000:
        lotes_10000.append(sql)
    elif len(lotes_100000) < 1200000:
        lotes_100000.append(sql)
    else:
        print('Lotes cheios!')
        return disturb
    
    time.sleep(0.1)
    
    return disturb, gas

gerar_veiculos()

def preparar_inserts(lote, len_lote):
    list_inserts = []
    i = 0
    for x in lote:
        if i < len_lote:
            if i == 0:
                insert = 'INSERT INTO tbDadosSensor (registro, fkSensor, dtColeta) VALUES '
                
            if i == len_lote - 1 or x == lote[-1]:
                insert += f"{x};\n"
                list_inserts.append(insert)
                i = 0
            else:
                insert += f"{x},"
                i += 1
                
    return list_inserts

def processar_lotes():
    list_insert_100 = preparar_inserts(lotes_100, 100)
    print(f'Teste lista: {list_insert_100}')
    list_insert_1000 = preparar_inserts(lotes_1000, 1000)
    list_insert_10000 = preparar_inserts(lotes_10000, 10000)
    list_insert_100000 = preparar_inserts(lotes_100000, 100000)
    
    print (f'Iniciando processamento dos lotes 100')
    
    for x in list_insert_100:
        inicio_100 = time.time()
        with connection.cursor() as cursor:
            cursor.execute(x)
            connection.commit()
        fim_100 = time.time()
        tempo_100.append(fim_100 - inicio_100)
        memoria_100.append(psutil.Process().memory_info().rss / 1024 ** 2)
        cpu_100.append(psutil.cpu_percent())
    
    print('\n----------------------------------------------------------------\n')
    
    print (f'Iniciando processamento dos lotes 1000')
    
    
    for x in list_insert_1000:
        inicio_1000 = time.time()
        with connection.cursor() as cursor:
            cursor.execute(x)
            connection.commit()
        fim_1000 = time.time()
        tempo_1000.append(fim_1000 - inicio_1000)
        memoria_1000.append(psutil.Process().memory_info().rss / 1024 ** 2)
        cpu_1000.append(psutil.cpu_percent())
        
    print('\n----------------------------------------------------------------\n')
    
    print (f'Iniciando processamento dos lotes 10000')
        
    for x in list_insert_10000:
        inicio_10000 = time.time()
        with connection.cursor() as cursor:
            cursor.execute(x)
            connection.commit()
        fim_10000 = time.time()
        tempo_10000.append(fim_10000 - inicio_10000)
        memoria_10000.append(psutil.Process().memory_info().rss / 1024 ** 2)
        cpu_10000.append(psutil.cpu_percent())
        
    print('\n----------------------------------------------------------------\n')
    
    print (f'Iniciando processamento dos lotes 100000')
    
    for x in list_insert_100000:
        inicio_100000 = time.time()
        with connection.cursor() as cursor:
            cursor.execute(x)
            connection.commit()
        fim_100000 = time.time()
        tempo_100000.append(fim_100000 - inicio_100000)
        memoria_100000.append(psutil.Process().memory_info().rss / 1024 ** 2)
        cpu_100000.append(psutil.cpu_percent())
    
    cursor.close()
    
    print('\n----------------------------------------------------------------\n')
    
    print('Processamento finalizado!')
            
    

for x in list_carros:
    mq7id, mq2id, mq135id = cadastro_sensor(x)
    inicio = time.time()
    print(f'Iniciando simulação para o veículo {x}...')
    disturbmq7 = 0
    disturbmq2 = 0
    disturbmq135 = 0
    while time.time() - inicio < 10:
        sort_variance = random.randint(1, 50)
        disturbmq7, co = simulate_capture(co, mq7, mq7id, sort_variance, disturbmq7)
        disturbmq2, c3h8 = simulate_capture(c3h8, mq2, mq2id, sort_variance, disturbmq2)
        disturbmq135, co2 = simulate_capture(co2, mq135, mq135id, sort_variance, disturbmq135)
        
    
processar_lotes()

# plt.plot(range(1, len(tempo_100) + 1), tempo_100, label='100 registros', marker='o')
# plt.title('Tempo de processamento - Lotes de 100 registros')
# plt.legend()
# plt.show()

# plt.plot(range(1, len(tempo_1000) + 1), tempo_1000, label='1000 registros', marker='o')
# plt.title('Tempo de processamento - Lotes de 1000 registros')
# plt.legend()
# plt.show()

# plt.plot(range(1, len(tempo_10000) + 1), tempo_10000, label='10000 registros', marker='o')
# plt.title('Tempo de processamento - Lotes de 10000 registros')
# plt.legend()
# plt.show()

# plt.plot(range(1, len(tempo_100000) + 1), tempo_100000, label='100000 registros', marker='o')
# plt.title('Tempo de processamento - Lotes de 100000 registros')
# plt.legend()
# plt.show()