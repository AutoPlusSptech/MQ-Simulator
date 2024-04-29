from matplotlib import pyplot as plt
import csv

def plotagem():
        
    x_1 = []
    y_1 = []
    x_2 = []
    y_2 = []
    x_3 = []
    y_3 = []
    x_4 = []
    y_4 = []
    
    with open('dados.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == '2871':
                x_1.append(row[2])
                y_1.append(int(row[1]))
            elif row[0] == '2872':
                x_2.append(row[2])
                y_2.append(int(row[1]))
            elif row[0] == '2873':
                x_3.append(row[2])
                y_3.append(int(row[1]))
            elif row[0] == '2874':
                x_4.append(row[2])
                y_4.append(float(row[1]))
                
                
    plt.plot(x_1, y_1, label = 'MQ-2')
    plt.xlabel('Data')
    plt.ylabel('Valor')
    
    plt.title('Gráfico de valores dos sensores')
    
    plt.legend()
    
    plt.show()
    
    plt.plot(x_2, y_2, label = 'MQ-7')
    plt.xlabel('Data')
    plt.ylabel('Valor')
    
    plt.title('Gráfico de valores dos sensores')
    
    plt.legend()
    
    plt.show()
    
    plt.plot(x_3, y_3, label = 'MQ-135')
    
    plt.xlabel('Data')
    plt.ylabel('Valor')
    
    plt.title('Gráfico de valores dos sensores')
    
    plt.legend()
    
    plt.show()
    
    plt.plot(x_4, y_4, label = 'DHT-11')
    
    plt.xlabel('Data')
    plt.ylabel('Valor')
    
    plt.title('Gráfico de valores dos sensores')
    
    plt.legend()
    
    plt.show()
        
plotagem()