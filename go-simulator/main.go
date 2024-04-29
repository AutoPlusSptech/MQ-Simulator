package main

import (
	"fmt"
	"sync"
	"time"

	"github.com/AutoPlusSptech/MQ-Simulator/sensor"
)

func main() {
	mq2 := sensor.Sensor{1, "ppm", "MQ-2", "2021-01-01", 1, 10, 100}
	mq7 := sensor.Sensor{2, "ppm", "MQ-7", "2024-03-29", 1, 100, 50000}

	// Canal para receber resultados das simulações
	resultChannel := make(chan int)

	// WaitGroup para sincronizar a conclusão de todas as simulações
	var wg sync.WaitGroup
	wg.Add(2) // Número de simulações

	// Executar simulações em paralelo
	go simulateSensor(mq2, resultChannel, &wg)
	go simulateSensor(mq7, resultChannel, &wg)

	// Função para coletar e imprimir resultados
	go func() {
		for value := range resultChannel {
			fmt.Printf("Valor atual: %d\n", value)
		}
	}()

	// Aguardar a conclusão de todas as simulações
	wg.Wait()

	// Fechar o canal para evitar vazamentos de memória
	close(resultChannel)
}

// Função para simular o sensor e enviar resultados para o canal
func simulateSensor(teste sensor.Sensor, resultChannel chan<- int, wg *sync.WaitGroup) {
	defer wg.Done() // Marca a conclusão da simulação

	value := 10 // Valor inicial

	for i := 0; i < 10; i++ {
		value = sensor.Simulate(value, teste) // Corrigido para chamar sensor.Simulate
		resultChannel <- value                // Enviar o resultado para o canal
		time.Sleep(3 * time.Second)
	}
}
