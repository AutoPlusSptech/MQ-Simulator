import pandas as pd
import matplotlib.pyplot as plt

# Carregar o CSV para um DataFrame e forçar 'valor' como numérico
df = pd.read_csv('dados.csv', sep=';', parse_dates=['dtColeta'], dtype={'valor': float})

# Filtrar os dados para cada sensor
sensor_3280 = df[df['idSensor'] == 3280]
sensor_3281 = df[df['idSensor'] == 3281]
sensor_3282 = df[df['idSensor'] == 3282]
sensor_3283 = df[df['idSensor'] == 3283]
sensor_3286 = df[df['idSensor'] == 3286]

# Plotar os gráficos de linha para cada sensor
plt.plot(sensor_3280['dtColeta'], sensor_3280['valor'], label='Sensor MQ-2')

# Adicionar rótulos e legenda
plt.xlabel('Data e Hora')
plt.ylabel('Valor')
plt.title('Valores do Sensor MQ-2 ao longo do Tempo')
plt.legend()

# Mostrar o gráfico
plt.show()

plt.plot(sensor_3281['dtColeta'], sensor_3281['valor'], label='Sensor MQ-7')

plt.xlabel('Data e Hora')
plt.ylabel('Valor')
plt.title('Valores do Sensor DHT-11 ao longo do Tempo')

plt.legend()

plt.show()

plt.plot(sensor_3282['dtColeta'], sensor_3282['valor'], label='Sensor MQ-135')

plt.xlabel('Data e Hora')
plt.ylabel('Valor')
plt.title('Valores do Sensor DHT-11 ao longo do Tempo')

plt.legend()

plt.show()

plt.plot(sensor_3283['dtColeta'], sensor_3283['valor'], label='Sensor DHT-11')

plt.xlabel('Data e Hora')
plt.ylabel('Valor')
plt.title('Valores do Sensor DHT-11 ao longo do Tempo')

plt.legend()

plt.show()

plt.plot(sensor_3286['dtColeta'], sensor_3286['valor'], label='Sensor F01R064905')

plt.xlabel('Data e Hora')
plt.ylabel('Valor')
plt.title('Valores do Sensor DHT-11 ao longo do Tempo')

plt.legend()

plt.show()