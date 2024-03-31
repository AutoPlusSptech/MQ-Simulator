package sensor

import (
	"fmt"
	"math/rand"
)

type Sensor struct {
	idSensor       int
	unidadeMedida  string
	modelo         string
	dataInstalacao string
	fkVeiculo      int
	valorMinimo    int
	valorMaximo    int
}

func randomRange(min, max int) int {
	valor := rand.Intn(max-min+1) + min
	return valor
}

func simulate(lastValue int, sensor Sensor) int {

	newValue := 0
	criticality := randomRange(1, 1000)
	upOrDown := randomRange(0, 1)
	multiplier := 1

	if criticality == 67 {
		multiplier = 5
		fmt.Println("Criticidade!")
	}

	if sensor.valorMaximo > 100 {
		newValue = randomRange(1, 35)
	} else {
		newValue = randomRange(1, 10)
	}

	if upOrDown == 0 {
		if lastValue-newValue*multiplier < sensor.valorMinimo {
			lastValue = sensor.valorMinimo
		} else {
			lastValue -= newValue * multiplier
		}
	} else {
		if lastValue+newValue*multiplier > sensor.valorMaximo {
			lastValue = sensor.valorMaximo
		} else {
			lastValue += newValue * multiplier
		}
	}

	return lastValue

}
