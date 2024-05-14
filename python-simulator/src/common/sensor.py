import random
import time
import common.conexao as conexao
from datetime import datetime
import json
import sys
import msgpack
import struct
import math

class Sensor:
    
    def __init__(self, unidadeMedida, modelo, dataInstalacao, fkVeiculo, valorMinimo, valorMaximo, valor, grupo, lastCaptureAt = None, idSensor = None, messageId = 0, fator = 1, eixos = None, degradacao = 0):
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
        
        # db = conexao.Conexao('user_atividePI', 'sptech', 'localhost', 'vehicle_monitoring')
        # db = conexao.Conexao('user_auto_plus', 'password', 'host', 'vehicle_monitoring')
        
        # query = f"INSERT INTO tbsensor (unidadeMedida, modelo, dataInstalacao, fkVeiculo) VALUES ('{self.unidadeMedida}', '{self.modelo}', '{self.dataInstalacao}', {self.fkVeiculo});"
        # query = f"INSERT INTO tbsensor (unidadeMedida, modelo, fkVeiculo) VALUES ('{self.unidadeMedida}', '{self.modelo}',  {self.fkVeiculo});"
        
        # print(f'Query: {query}')
        
        # db.insert(query)
        # self.idSensor = db.getLastId()
        self.idSensor = random.randint(1, 100000)
        # db.close()
        
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
            self.last_acce = None
            self.acce_range = (0, 25)
            self.max_change_acce = 3

            if self.last_acce is not None:
                min_next_acce = max(self.last_acce - self.max_change_acce, self.acce_range[0])
                max_next_acce = min(self.last_acce + self.max_change_acce, self.acce_range[1])
                new_acce = random.uniform(min_next_acce, max_next_acce)
            else:
                new_acce = random.uniform(*self.acce_range)

            novoValor = new_acce

            if self.valor is not None:
                if self.last_acce is not None:
                    temp_change = abs(new_acce - self.last_acce)
                    if temp_change > self.max_change_acce:
                        new_acce = self.last_acce + self.max_change_acce if new_acce > self.last_acce else self.last_acce - self.max_change_acce
                else:
                    new_acce = self.last_acce if self.last_acce is not None else new_acce

            novoValor = new_acce

            if self.valor is not None and abs(novoValor - self.valor) > self.max_change_acce:
                if novoValor > self.valor:
                    novoValor = self.valor + self.max_change_acce
                else:
                    novoValor = self.valor - self.max_change_acce

            self.valor = novoValor
            self.last_temp = self.valor
            
        if "MPU" in self.modelo and self.unidadeMedida == 'rad/s':
            self.last_speed = None
            self.speed_range = (0, 20)
            self.max_change_speed = 3

            if self.last_speed is not None:
                min_next_spped = max(self.last_speed - self.max_change_speed, self.speed_range[0])
                max_next_speed = min(self.last_speed + self.max_change_speed, self.speed_range[1])
                new_speed = random.uniform(min_next_spped, max_next_speed)
            else:
                new_speed = random.uniform(*self.speed_range)

            novoValor = new_speed

            if self.valor is not None:
                if self.last_speed is not None:
                    temp_change = abs(new_speed - self.last_speed)
                    if temp_change > self.max_change_speed:
                        new_speed = self.last_speed + self.max_change_speed if new_speed > self.last_speed else self.last_speed - self.max_change_speed
                else:
                    new_speed = self.last_speed if self.last_speed is not None else new_speed

            novoValor = new_speed

            if self.valor is not None and abs(novoValor - self.valor) > self.max_change_speed:
                if novoValor > self.valor:
                    novoValor = self.valor + self.max_change_speed
                else:
                    novoValor = self.valor - self.max_change_speed

            self.valor = novoValor
            self.last_temp = self.valor

        if "MPU" in self.modelo and self.unidadeMedida == 'ºC':
            self.last_temp = None
            self.temp_range = (-20, 85)
            self.max_change_temp = 3

            if self.last_temp is not None:
                min_next_temp = max(self.last_temp - self.max_change_temp, self.temp_range[0])
                max_next_temp = min(self.last_temp + self.max_change_temp, self.temp_range[1])
                new_temp = random.uniform(min_next_temp, max_next_temp)
            else:
                new_temp = random.uniform(*self.temp_range)

            novoValor = new_temp

            if self.valor is not None:
                if self.last_temp is not None:
                    temp_change = abs(new_temp - self.last_temp)
                    if temp_change > self.max_change_temp:
                        new_temp = self.last_temp + self.max_change_temp if new_temp > self.last_temp else self.last_temp - self.max_change_temp
                else:
                    new_temp = self.last_temp if self.last_temp is not None else new_temp

            novoValor = new_temp

            if self.valor is not None and abs(novoValor - self.valor) > self.max_change_temp:
                if novoValor > self.valor:
                    novoValor = self.valor + self.max_change_temp
                else:
                    novoValor = self.valor - self.max_change_temp

            self.valor = novoValor
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