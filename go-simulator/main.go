package main

import (
	"fmt"
	"time"
)

func main() {
	mq2 := Sensor{1, "ppm", "MQ-2", "2021-01-01", 1, 10, 100}
	mq7 := Sensor{2, "ppm", "MQ-7", "2024-03-29", 1, 100, 50000}

	valueMq2 := 10
	valueMq7 := 100

	for x := 0; x < 10; x++ {
		valueMq2 = simulate(valueMq2, mq2)
		valueMq7 = simulate(valueMq7, mq7)
		fmt.Printf("Valor atual do MQ-2: %d\n", valueMq2)
		fmt.Printf("Valor atual do MQ-7: %d\n", valueMq7)
		time.Sleep(3 * time.Second)
	}
}
