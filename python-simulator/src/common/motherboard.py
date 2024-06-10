import common.sensor as sensor
import simplejson as json
import sys
import azure.iot.hub as iotHub
import azure.iot.device as iotDevice
from azure.iot.device import Message
import random
import time
import zlib
import re
from datetime import datetime, timedelta
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
            listJson = []
            
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
                
                # Mensagem sendo enviada para o IoT Hub
                mensagem_data = {
                    'sensorId': int(sensor.idSensor),
                    'registry': sensor.valor,
                    'battery': round(self.bateria, 2),
                    'dtColeta': str(datetime.now())
                }

                #jsonMessage = json.dumps(mensagem_data)
                listJson.append(mensagem_data)

            jsonMessage = json.dumps(listJson)

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
                print(f'Mensagem maior que 200 bytes!\n')
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


                # listData.append(sensor.valor)
                # listIdSensor.append(sensor.idSensor)
                
            # mensagem_data = {
            #     'vehicleId': self.sensores[0].fkVeiculo,
            #     'sensorId': listIdSensor,
            #     'registry': listData,
            #     'battery': round(self.bateria, 2),
            #     'dtColeta': str(datetime.now())
            # }
            
            # jsonMessage = json.dumps(mensagem_data)
            
            # mensagem = Message(jsonMessage, content_encoding='utf-8', content_type='application/json')
            
            # print(f'Mensagen: {mensagem}')
            # print(f'Bytes Mensagem: {sys.getsizeof(jsonMessage)}')
            
            
                
        def cloud_run(self):
            while True:
                self.simulate()
                
                time.sleep(60)
                
        def local_run(self):

            last_capture = datetime.now()
            data_arquivo = last_capture.strftime('%d-%m-%Y-%H-%M-%S')
            
            while True:

                if last_capture.hour > 17 or last_capture.hour < 9:
                    proximo_dia = last_capture + timedelta(days=1)
                    proximo_dia = proximo_dia.strftime('%Y-%m-%d')
                    last_capture = datetime.strptime(f'{proximo_dia} 09:00:00', '%Y-%m-%d %H:%M:%S')
                data_arquivo = last_capture.strftime('%d-%m-%Y-%H-%M-%S')

                path_execution = os.getcwd()
                
                with open(f'{path_execution}/python-simulator/data/dados_simulador-{data_arquivo}.json', 'w') as file:
                    file.write('[{"origin": "simulator", "version": "local_run", "destiny":"s3", "body": []}]')
                
                problemaMotor = random.randint(1, 50000)
                
                if problemaMotor == 67:
                    for x in self.sensores:
                        if x.grupo == 'Motor':
                            x.elevarFator()
                            
                            print(f'Fator elevado para o sensor {x.modelo}')
                            
                upOrDown = random.randint(1, 2)
                
                frenagem = False
            
                for x in self.sensores:
                    
                    if x.modelo == 'VL53L0X':
                        x.generateValue(upOrDown, frenagem)
                    else:
                        frenagem = x.generateValue(upOrDown)
                    
                    with open(f'{path_execution}/python-simulator/data/dados_simulador-{data_arquivo}.json', 'r') as file:
                        dados = json.load(file)
                        
                        campo_dado = {
                            'id_sensor': x.idSensor,
                            'modelo': x.modelo,
                            'valor': x.valor,
                            'dt_coleta': str(last_capture)
                        }
                        
                        dados[0]['body'].append(campo_dado)
                        
                    with open(f'{path_execution}/python-simulator/data/dados_simulador-{data_arquivo}.json', 'w') as file:
                        json.dump(dados, file)
                        
                self.messageId += 1
                    
                bucket_name = '3cco-autoplus-mq-bucket-raw'

                dia_atual = last_capture.strftime('%d-%m-%Y')
                
                s3path = f'data/ec2/{dia_atual}'
                
                formatacao_data = re.sub(r'[\s:]', '-', str(last_capture))
                
                s3 = boto3.client('s3')
                s3.upload_file(f'{path_execution}/python-simulator/data/dados_simulador-{data_arquivo}.json', bucket_name, f'{s3path}/dados-{formatacao_data}.json')
                
                os.remove(f'{path_execution}/python-simulator/data/dados_simulador-{data_arquivo}.json')

                last_capture += timedelta(minutes=5)
                    
                time.sleep(0.01)
