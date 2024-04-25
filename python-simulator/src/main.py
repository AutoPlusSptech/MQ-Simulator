import conexao
import sensor
import motherboard
import time
from datetime import datetime

def main():
    
    mq2 = sensor.Sensor('ppm', 'MQ-2', f'{datetime.now()}', 1, 0, 100, 0, "Motor")
    mq7 = sensor.Sensor('ppm', 'MQ-7', f'{datetime.now()}', 1, 100, 50000, 500, "Motor")
    mq135 = sensor.Sensor('ppm', 'MQ-135', f'{datetime.now()}', 1, 10000, 20000, 12500, "Motor")
    dht11 = sensor.Sensor('%', 'DHT-11', f'{datetime.now()}', 1, 5, 100, 70, "Motor")
    
    placa01 = motherboard.Motherboard()
        
    placa01.addSensor(mq2)
    placa01.addSensor(mq7)
    placa01.addSensor(mq135)
    placa01.addSensor(dht11)
    
    # placa01.run()
    placa01.economicRun()
    
main()