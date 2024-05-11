import matplotlib.pyplot as plt
import csv

valores_mq2 = []
valores_mq7 = []
valores_mq135 = []

with open('dados_simulados_mq_4.csv', 'r') as arquivo_csv:
    resultado_leitura = csv.DictReader(arquivo_csv, delimiter=';')
    for linha in resultado_leitura:
        if linha['modelo'] == 'MQ-2':
            valores_mq2.append(float(linha['registro']))
        elif linha['modelo'] == 'MQ-7':
            valores_mq7.append(float(linha['registro']))
        elif linha['modelo'] == 'MQ-135':
            valores_mq135.append(float(linha['registro']))
            
plt.plot(valores_mq7, label='MQ-7')
plt.plot(valores_mq135, label='MQ-135')
plt.legend()
plt.title('Simulação de valores de sensores - MQ-7 e MQ-135')
plt.ylabel('Captura do sensor - em ppm')
plt.show()

plt.plot(valores_mq2, label='MQ-2')
plt.legend()
plt.title('Simulação de valores de sensores MQ-2')
plt.ylabel('Captura do sensor - em ppm')
plt.show()


# plt.legend()
# plt.ylabel('Captura do sensor - em ppm')
# plt.title('Simulação de valores de sensores MQ-135')
# plt.show()
