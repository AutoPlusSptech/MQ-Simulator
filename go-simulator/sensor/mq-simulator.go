package sensor

import (
	"fmt"
	"math/rand"
)

type Sensor struct {
	IdSensor       int
	UnidadeMedida  string
	Modelo         string
	DataInstalacao string
	FkVeiculo      int
	ValorMinimo    int
	ValorMaximo    int
}

func randomRange(min, max int) int {
	valor := rand.Intn(max-min+1) + min
	return valor
}

func Simulate(lastValue int, sensor Sensor) int {

	newValue := 0
	deterioration := randomRange(1, 1000)
	upOrDown := randomRange(0, 1)
	multiplier := 1

	if deterioration == 67 {
		multiplier = 5
		fmt.Println("Deterioração!")
	}

	if sensor.ValorMaximo > 100 {
		newValue = randomRange(1, 35)
	} else {
		newValue = randomRange(1, 10)
	}

	if upOrDown == 0 {
		if lastValue-newValue*multiplier < sensor.ValorMinimo {
			lastValue = sensor.ValorMinimo
		} else {
			lastValue -= newValue * multiplier
		}
	} else {
		if lastValue+newValue*multiplier > sensor.ValorMaximo {
			lastValue = sensor.ValorMaximo
		} else {
			lastValue += newValue * multiplier
		}
	}

	return lastValue

}
