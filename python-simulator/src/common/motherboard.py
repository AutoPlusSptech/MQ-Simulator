import common.sensor as sensor
import json
import sys
import azure.iot.hub as iotHub
import azure.iot.device as iotDevice
from azure.iot.device import Message
import random
import time
import zlib
import re
from datetime import datetime
import boto3
import os

class Motherboard:
        
        def __init__(self):
            self.sensores = []
            self.bateria = 100
            self.messageId = 0
            self.deviceId = 'mq-simulator-demo'
            self.registry = iotDevice.IoTHubDeviceClient.create_from_connection_string('HostName=hub-testes.azure-devices.net;DeviceId=mq-simulator-demo;SharedAccessKey=cTqz1wr8bSvcE3MX+e4X0Om5vQ+rqkyGoAIoTJmPB4w=')
            self.registry.connect()
            
        def addSensor(self, sensor):
            self.sensores.append(sensor)
            
        def compress(self, message):
            msgJson = json.dumps(message)
            msgJson = re.sub(r'\s', '', msgJson)
            msgBytes = bytes(msgJson.encode('utf-8'))
            msgCompressed = zlib.compress(msgBytes)
            return msgCompressed
        
        def descompress(self, message):
            msgDecompressed = zlib.decompress(message)
            msgJson = json.loads(msgDecompressed)
            return msgJson
            
        def simulate(self):
            listData = []
            listIdSensor = []
            
            frenagem = False
            
            problemaMotor = random.randint(1, 100)
                
            if problemaMotor == 67:
                for x in self.sensores:
                    if x.grupo == 'Motor':
                        x.elevarFator()
                            
                        print(f'Fator elevado para o sensor {x.modelo}')
                        
            upOrDown = random.randint(1, 2)
            
            for sensor in self.sensores:
                
                if sensor.modelo == 'VL53L0X':
                    sensor.generateValue(upOrDown, frenagem)
                else:
                    frenagem = sensor.generateValue(upOrDown)                
                sensor.sendValueDb()
                listData.append(sensor.valor)
                listIdSensor.append(sensor.idSensor)
                
            self.messageId += 1
                
            mensagem_data = {
                'vehicleId': self.sensores[0].fkVeiculo,
                'sensorId': listIdSensor,
                'registry': listData,
                'battery': round(self.bateria, 2)
            }
            
            jsonMessage = json.dumps(mensagem_data)
            
            mensagem = Message(jsonMessage, content_encoding='utf-8', content_type='application/json')
            
            print(f'Mensagen: {mensagem}')
            print(f'Bytes Mensagem: {sys.getsizeof(jsonMessage)}')
            
            if sys.getsizeof(jsonMessage) <= 200:
                
                chanceErro = random.randint(1, 100)
                
                if chanceErro <= 3:
                    print('Erro ao enviar mensagem!')
                else:
                    try:
                        self.registry.send_message(mensagem)
                        print('Mensagem enviada com sucesso!')
                    except Exception as e:
                        print(f'Erro ao enviar mensagem: {e}')
                
                self.bateria -= 0.05
            else:
                print(f'Mensagem maior que 200 bytes!\nTamanho da mensagem: {sys.getsizeof(jsonMessage)}')
                
                print(f'Tentando comprimir a mensagem...')
                
                jsonMessage = self.compress(mensagem_data)
                
                print(f'Mensagem comprimida: {jsonMessage}')
                
                print(f'Bytes Mensagem Comprimida: {sys.getsizeof(jsonMessage)}')
                
                if sys.getsizeof(jsonMessage) <= 200:
                    
                    chanceErro = random.randint(1, 100)
                    
                    if chanceErro <= 3:
                        print('Erro ao enviar mensagem!')
                    else:
                        try:
                            self.registry.send_message(mensagem)
                            print('Mensagem enviada com sucesso!')
                        except Exception as e:
                            print(f'Erro ao enviar mensagem: {e}')
                    
                    self.bateria -= 0.05
                
                else:
                    
                    print(f'Mensagem ainda maior que 200 bytes!\nTamanho da mensagem: {sys.getsizeof(jsonMessage)}')
                    print('Mensagem não enviada!')
                
        def cloud_run(self):
            while True:
                self.simulate()
                
                time.sleep(300)
                
        def local_run(self):
            
            data_arquivo = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
            
            
            while True:
                
                with open(f'../data/dados_simulador-{data_arquivo}.json', 'w') as file:
                    file.write('[{"origin": "simulator"}, {"version": "local_run"}, {"destiny":"s3"}]')
                
                problemaMotor = random.randint(1, 500)
                
                if problemaMotor == 67:
                    for x in self.sensores:
                        if x.grupo == 'Motor':
                            x.elevarFator()
                            
                            print(f'Fator elevado para o sensor {x.modelo}')
                    
                # if problemaPneu == 67:
                #     for x in self.sensores:
                #         if x.grupo == 'Pneu':
                #             x.elevarFator()
                            
                #             print(f'Fator elevado para o sensor {x.modelo}')
                            
                upOrDown = random.randint(1, 2)
                
                listData = []
                listIdSensor = []
                
                frenagem = False
            
                for x in self.sensores:
                    
                    if x.modelo == 'VL53L0X':
                        x.generateValue(upOrDown, frenagem)
                    else:
                        frenagem = x.generateValue(upOrDown)                
                    # x.sendValueDb()
                    listData.append(x.valor)
                    
                    with open(f'../data/dados_simulador-{data_arquivo}.json', 'r') as file:
                        dados = json.load(file)
                        
                        campo_dado = {
                            "body": {
                                'idSensor': x.idSensor,
                                'modelo': x.modelo,
                                'valor': x.valor,
                                'lastCaptureAt': str(datetime.now())
                            }
                        }
                        
                        dados.append(campo_dado)
                        
                    with open(f'../data/dados_simulador-{data_arquivo}.json', 'w') as file:
                        json.dump(dados, file)
                    
                    # with open(f'python-simulator/data/dados_simulador-{data_arquivo}.csv', 'a') as file:
                    #     # file.write(f'{x.idSensor},{x.valor},{x.lastCaptureAt}\n')
                    #     file.write(f'{x.idSensor};{x.modelo};{x.valor};{datetime.now()}\n')
                        
                        
                self.messageId += 1
                
                
                    
                message = {
                    'm': self.messageId,
                    'v': self.sensores[0].fkVeiculo,
                    's': listIdSensor,
                    'r': listData,
                    'b': self.bateria
                }
                    
                jsonMessage = json.dumps(message)
                    
                # print(f'Mensagen: {jsonMessage}')
                    # print(f'Bytes Mensagem: {sys.getsizeof(jsonMessage)}\n')
                    
                # with open (f'dados-{datetime.now().date()}.json', 'w') as file:
                #     file.write(jsonMessage)
                    
                bucket_name = '3cco-autoplus-mq-bucket-raw'
                
                s3path = 'data/ec2'
                
                s3 = boto3.client('s3')
                s3.upload_file(f'../data/dados_simulador-{data_arquivo}.json', bucket_name, f'{s3path}/dados-{datetime.now()}.json')
                
                os.remove(f'../data/dados_simulador-{data_arquivo}.json')
                
                    
                msgCompressed = self.compress(jsonMessage)
                    
                    # print(f'Mensagem Comprimida: {msgCompressed}')
                    # print(f'Bytes Mensagem Comprimida: {sys.getsizeof(msgCompressed)}\n')
                    
                msgDecompressed = self.descompress(msgCompressed)
                    
                    # print(f'Mensagem Descomprimida: {msgDecompressed}')
                    # print(f'Bytes Mensagem Descomprimida: {sys.getsizeof(msgDecompressed)}\n')
                    
                    
                time.sleep(0.1)
