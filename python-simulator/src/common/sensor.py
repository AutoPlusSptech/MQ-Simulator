import random
import time
import common.conexao as conexao
from datetime import datetime
from .simulador_mpu import CarSimulator
import json
import sys
import msgpack
import struct
import math

class Sensor:
    
    def __init__(self, unidadeMedida, modelo, dataInstalacao, fkVeiculo, valorMinimo, valorMaximo, valor, grupo, idSensor = 0, lastCaptureAt = None, messageId = 0, fator = 1, eixos = None, degradacao = 0):
        self.unidadeMedida = unidadeMedida
        self.modelo = modelo
        self.dataInstalacao = dataInstalacao
        self.fkVeiculo = fkVeiculo
        self.valorMinimo = valorMinimo
        self.valorMaximo = valorMaximo
        self.valor = valor
        self.grupo = grupo
        self.fator = fator
        self.eixos = eixos
        self.degradacao = degradacao
        self.idSensor = idSensor

        if self.idSensor == 0:
            self.idSensor = self.register_sensor()

    def register_sensor(self):
        # db = conexao.Conexao('user_atividePI', 'sptech', 'localhost', 'vehicle_monitoring')
        db = conexao.Conexao('user', 'password', 'server', 'database')
        
        #query = f"INSERT INTO tbsensor (unidadeMedida, modelo, dataInstalacao, fkVeiculo) VALUES ('{self.unidadeMedida}', '{self.modelo}', '{self.dataInstalacao}', {self.fkVeiculo});"
        query = f"INSERT INTO sensor (unidade_medida, modelo, fk_veiculo) VALUES ('{self.unidadeMedida}', '{self.modelo}',  {self.fkVeiculo});"
        
        print(f'Query de insert do Sensor: {query}')
        
        db.insert(query)
        idSensor = db.getLastId()

        print(f'ID do Sensor: {idSensor}')

        # idSensor = random.randint(1, 100000)
        db.close()

        return idSensor
        
    def generateValue(self, upOrDown, frenagem = False):
        
        

        if "MQ-" in self.modelo:
        
            if self.valorMaximo > 100:
                valorGerado = random.randint(1, 8)
            else:
                valorGerado = random.randint(1, 3)
             
              
            # To do: Implementar logica de fator (multiplicando ou aplicando % ao valor simulado)                  
            if upOrDown == 1:
                novoValor = self.valor + valorGerado
                if self.fator > 1 and self.degradacao > 0:
                    
                    if "MQ-135" in self.modelo:
                        novoValor = int(self.valor + (novoValor * (self.fator * 0.01)))
                        print(f'Degradacao MQ: {self.degradacao}')
                        self.degradacao -= 1
                        
                    else:
                        novoValor = int(self.valor + (novoValor * (self.fator * 0.10)))
                        self.degradacao -= 1
            else:
                novoValor = self.valor - valorGerado
                if self.fator > 1:
                    # novoValor = int(novoValor - (self.valor * (self.fator * 0.10)))
                    print(f'Fator: {self.fator}')
                    
        if "DHT-11" in self.modelo:
            valorGerado = random.random()

            if upOrDown == 1 and self.degradacao > 0:
                novoValor = self.valor - (valorGerado * self.fator)
                print(f'Degradacao DHT: {self.degradacao}')
                self.degradacao -= 1
            elif upOrDown == 2:
                novoValor = self.valor + valorGerado
                
            else:
                novoValor = self.valor - valorGerado

            novoValor = round(novoValor, 1)
            
        if "F01" in self.modelo:
            # Valor entre 70 e 100
            valorGerado = random.randint(1, 3)
            
            if upOrDown == 1 and self.degradacao > 0:
                novoValor = self.valor + (valorGerado * (self.fator * 0.60))
                print(f'Degradacao F01: {self.degradacao}')
                self.degradacao -= 1
            elif upOrDown == 1:
                novoValor = self.valor + valorGerado
            else:
                novoValor = self.valor - valorGerado
                
            novoValor = round(novoValor, 1)
            
        if "MPU" in self.modelo and self.unidadeMedida == 'm/s²':
            car_simulator = CarSimulator()

            car_simulator.simulate_speed()

            new_acce = car_simulator.get_last_speed()

            self.valor = new_acce
            self.last_temp = self.valor
            
        if "MPU" in self.modelo and self.unidadeMedida == 'rad/s':
            car_simulator = CarSimulator()

            car_simulator.simulate_speed()

            new_veloc = car_simulator.get_last_speed()

            self.valor = new_veloc
            self.last_temp = self.valor

        if "MPU" in self.modelo and self.unidadeMedida == 'ºC':
            brake_pad_simulator = CarSimulator()

            brake_pad_simulator.update_temperature()

            new_temp = brake_pad_simulator.get_last_temperature()

            self.valor = new_temp
            self.last_temp = self.valor
            
        if "VL53L0X" in self.modelo:
            if self.valor == 0:
                altura_cavidade = random.uniform(0.6, 0.8)
                
            if frenagem:
                altura_cavidade = random.uniform(0, 0.05)
            else:
                altura_cavidade = random.uniform(0.0, 0.0001)
                
                
            novoValor = self.valor - altura_cavidade
            
            if novoValor < 0:
                novoValor = 0
                
            self.valor = novoValor

            
            
        if self.grupo == 'Motor':
            
            if novoValor > self.valorMaximo:
                novoValor = self.valorMaximo
            elif novoValor < self.valorMinimo:
                novoValor = self.valorMinimo
            
            self.valor = novoValor
        
    def sendValueDb(self):
        
        self.lastCaptureAt = datetime.now()
        
        db = conexao.Conexao('user_atividePI', 'sptech', 'localhost', 'vehicle_monitoring')
        # db = conexao.Conexao('user_auto_plus', 'password', 'host', 'vehicle_monitoring')
        
        query = f"INSERT INTO tbdadossensor (registro, dtColeta, fkSensor) VALUES ('{self.valor}', '{self.lastCaptureAt}', '{self.idSensor}');"
        # query = f"INSERT INTO tbdadossensor (registro, fkSensor) VALUES ('{self.valor}', '{self.idSensor}');"
        
        db.insert(query)
        db.close()
        
    
        
    def sendValueIoTHub(self):
        
        message = {
            'messageId': 848941,
            'vehicleId': 45000,
            'sensorId': [11451, 11452, 11453],
            'registry': [15, 14000, 25000],
            'battery': [97.85, 97.85, 97.85]
        }
        
        jsonMessage = json.dumps(message)
        
        # print(f'Message: {jsonMessage}')
        # print(f'Size JSON: {sys.getsizeof(jsonMessage)}\n')
        
    def elevarFator(self):
        self.fator += 1
        self.degradacao = 5
        
    def resetFator(self):
        self.fator = 1
        self.degradacao = 0