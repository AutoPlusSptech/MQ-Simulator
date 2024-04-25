import random
import time
import conexao
from datetime import datetime
import json
import sys
import msgpack
import struct

class Sensor:
    
    def __init__(self, unidadeMedida, modelo, dataInstalacao, fkVeiculo, valorMinimo, valorMaximo, valor, area, lastCaptureAt = None, idSensor = None, messageId = 0, deterioracao = [False, False]):
        self.unidadeMedida = unidadeMedida
        self.modelo = modelo
        self.dataInstalacao = dataInstalacao
        self.fkVeiculo = fkVeiculo
        self.valorMinimo = valorMinimo
        self.valorMaximo = valorMaximo
        self.valor = valor
        self.area = area
        self.deterioracao = [False, False]
        
        # db = conexao.Conexao('user', 'senha', 'host', 'database')
        
        # query = f"INSERT INTO tbsensor (unidadeMedida, modelo, dataInstalacao, fkVeiculo) VALUES ('{self.unidadeMedida}', '{self.modelo}', '{self.dataInstalacao}', {self.fkVeiculo});"
        
        # print(f'Query: {query}')
        
        # db.insert(query)
        # self.idSensor = db.getLastId()
        # db.close()

        self.idSensor = 1
        
    def generateValue(self):

        multiplicador = 1

        deterioracaoMotor = random.randint(1, 100)
        deterioracaoPneu = random.randint(1, 100)
        upOrDown = random.randint(1, 2)

        if "MQ" in self.modelo:
            if self.valorMaximo > 100:
                valorGerado = random.randint(1, 35)
            else:
                valorGerado = random.randint(1, 10)

            if deterioracaoMotor == 67:
                multiplicador = 5

                
            
            if upOrDown == 1:
                novoValor = self.valor + valorGerado * multiplicador
            else:
                novoValor = self.valor - valorGerado * multiplicador
        
        if "DHT-11" in self.modelo:
            valorGerado = random.random()
            
            multiplicador = 2

            if upOrDown == 1:
                novoValor = self.valor + valorGerado * multiplicador
            else:
                novoValor = self.valor - valorGerado * multiplicador

            novoValor = round(novoValor, 1)
        
        for x in self.deterioracao:

            print(self.deterioracao.index(x))

        print(self.deterioracao)
            
        if novoValor > self.valorMaximo:
            novoValor = self.valorMaximo
        elif novoValor < self.valorMinimo:
            novoValor = self.valorMinimo
            
        self.valor = novoValor
        
    def sendValueDb(self):
        
        self.lastCaptureAt = datetime.now()
        
        db = conexao.Conexao('user', 'senha', 'host', 'database')
        
        query = f"INSERT INTO tbdadossensor (registro, dtColeta, fkSensor) VALUES ('{self.valor}', '{self.lastCaptureAt}', '{self.idSensor}');"
        
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
        
        print(f'Message: {jsonMessage}')
        print(f'Size JSON: {sys.getsizeof(jsonMessage)}\n')