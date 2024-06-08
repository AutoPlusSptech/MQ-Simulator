import common.conexao as conexao
import common.sensor as sensor
import common.motherboard as motherboard
import time
from datetime import datetime
import psutil
from matplotlib import pyplot as plt
import sys
import argparse


idMq2 = 0
idMq7 = 0
idMq135 = 0
idDht11 = 0
idMpu6050_aceleracao = 0
idMpu6050_velocidade = 0
idMpu6050_temp = 0
idVl53l0x = 0
idF01r064905 = 0

def main(flag_ids, flag_local):

    print('''
    ================================================
          
           Auto+ - Monitoramento de Veículos

    ================================================
    ''')

    time.sleep(5)

    if flag_local:
        print('Flag de local ativada, o simulador irá rodar localmente.\nTenha certeza de ter as credencias da AWS configuradas no seu ambiente.\n')
        time.sleep(2)

    if flag_ids:

        print('Flag de IDs ativada, por favor informe os IDs dos sensores informados a seguir:\nIMPORTANTE: Os IDs devem ser válidos e já estarem cadastrados no database.\n')

        time.sleep(2)

        idMq2 = int(input('ID do sensor MQ-2: '))
        idMq7 = int(input('ID do sensor MQ-7: '))
        idMq135 = int(input('ID do sensor MQ-135: '))
        idDht11 = int(input('ID do sensor DHT-11: '))
        idMpu6050_aceleracao = int(input('ID do sensor MPU-6050 (Aceleração): '))
        idMpu6050_velocidade = int(input('ID do sensor MPU-6050 (Velocidade): '))
        idMpu6050_temp = int(input('ID do sensor MPU-6050 (Temperatura): '))
        idVl53l0x = int(input('ID do sensor VL53L0X: '))
        idF01r064905 = int(input('ID do sensor F01R064905: '))

        mq2 = sensor.Sensor('ppm', 'MQ-2', f'{datetime.now()}', 1, 0, 100, 0, "Motor", idMq2)
        mq7 = sensor.Sensor('ppm', 'MQ-7', f'{datetime.now()}', 1, 100, 50000, 500, "Motor", idMq7)
        mq135 = sensor.Sensor('ppm', 'MQ-135', f'{datetime.now()}', 1, 10000, 20000, 10000, "Motor", idMq135)
        dht11 = sensor.Sensor('%', 'DHT-11', f'{datetime.now()}', 1, 0, 100, 40, "Motor", idDht11)
        mpu6050_aceleracao = sensor.Sensor('m/s²', 'MPU-6050', f'{datetime.now()}', 1, 0, 25, None, "Pneu", idMpu6050_aceleracao)
        mpu6050_velocidade = sensor.Sensor('rad/s', 'MPU-6050', f'{datetime.now()}', 1, 0, 20, None, "Pneu", idMpu6050_velocidade)
        mpu6050_temp = sensor.Sensor('ºC', 'MPU-6050', f'{datetime.now()}', 1, -20, 85, None, "Pneu", idMpu6050_temp)
        vl53l0x = sensor.Sensor('mm', 'VL53L0X', f'{datetime.now()}', 1, 0, 1, 0.5, "Pneu", idVl53l0x)
        f01r064905 = sensor.Sensor('°C', 'F01R064905', f'{datetime.now()}', 1, 70, 100, 0, "Motor", idF01r064905)

    else:
    
        mq2 = sensor.Sensor('ppm', 'MQ-2', f'{datetime.now()}', 1, 0, 100, 0, "Motor")
        mq7 = sensor.Sensor('ppm', 'MQ-7', f'{datetime.now()}', 1, 100, 50000, 500, "Motor")
        mq135 = sensor.Sensor('ppm', 'MQ-135', f'{datetime.now()}', 1, 10000, 20000, 10000, "Motor")
        dht11 = sensor.Sensor('%', 'DHT-11', f'{datetime.now()}', 1, 0, 100, 40, "Motor")
        mpu6050_aceleracao = sensor.Sensor('m/s²', 'MPU-6050', f'{datetime.now()}', 1, 0, 25, None, "Pneu")
        mpu6050_velocidade = sensor.Sensor('rad/s', 'MPU-6050', f'{datetime.now()}', 1, 0, 20, None, "Pneu")
        mpu6050_temp = sensor.Sensor('ºC', 'MPU-6050', f'{datetime.now()}', 1, -20, 85, None, "Pneu")
        vl53l0x = sensor.Sensor('mm', 'VL53L0X', f'{datetime.now()}', 1, 0, 1, 0.5, "Pneu")
        f01r064905 = sensor.Sensor('°C', 'F01R064905', f'{datetime.now()}', 1, 70, 100, 0, "Motor")
    
    placa = motherboard.Motherboard()
    
    placa.addSensor(mq2)
    placa.addSensor(mq7)
    placa.addSensor(mq135)
    placa.addSensor(dht11)
    placa.addSensor(mpu6050_aceleracao)
    placa.addSensor(mpu6050_velocidade)
    placa.addSensor(mpu6050_temp)
    placa.addSensor(vl53l0x)
    placa.addSensor(f01r064905)
    
    if flag_local:
        placa.local_run()
    else:
        placa.cloud_run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto+ - Monitoramento de Veículos')
    parser.add_argument('--ids', type=bool, default=False, help='Flag para informar os IDs dos sensores já cadastrados no database')
    parser.add_argument('--local', type=bool, default=False, help='Flag para rodar o simulador localmente')

    args = parser.parse_args()

    main(args.ids, args.local)