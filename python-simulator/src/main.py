import conexao
import sensor
import motherboard
import time
from datetime import datetime
import psutil
from matplotlib import pyplot as plt

def main():
    
    mq2 = sensor.Sensor('ppm', 'MQ-2', f'{datetime.now()}', 1, 0, 100, 0, "Motor")
    mq7 = sensor.Sensor('ppm', 'MQ-7', f'{datetime.now()}', 1, 100, 50000, 500, "Motor")
    mq135 = sensor.Sensor('ppm', 'MQ-135', f'{datetime.now()}', 1, 10000, 20000, 11000, "Motor")
    dht11 = sensor.Sensor('%', 'DHT-11', f'{datetime.now()}', 1, 0, 100, 40, "Motor")
    mpu6050 = sensor.Sensor('m/s²', 'MPU-6050', f'{datetime.now()}', 1, -32768, 32767, None, "Pneu")
    vl53l0x = sensor.Sensor('mm', 'VL53L0X', f'{datetime.now()}', 1, 0, 1, 0.5, "Pneu")
    
    placa = motherboard.Motherboard()
    
    placa.addSensor(mq2)
    placa.addSensor(mq7)
    placa.addSensor(mq135)
    placa.addSensor(dht11)
    placa.addSensor(mpu6050)
    placa.addSensor(vl53l0x)
    
    placa.economicRun()
    
main()