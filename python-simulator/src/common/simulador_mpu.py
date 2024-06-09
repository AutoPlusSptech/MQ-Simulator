import random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CarSimulator:
    def __init__(self):
        self.last_speed = random.uniform(0, 10)
        self.speed_range = (0, 20)
        self.max_acceleration = 2.5
        self.max_deceleration = -2.5
        self.valor = self.last_speed
        self.speeds = []
        self.stop_duration = 0
        self.temperature = 20
        self.velocity = 0
        self.acceleration = 0
        self.temp_range = (-20, 85)
        self.velocity_range = (0, 30)
        self.acceleration_range = (-10, 10)
        self.temperatures = []

    def simulate_speed(self):
        stop_light_chance = 0.05

        if self.stop_duration > 0:
            new_speed = 0
            self.stop_duration -= 1
        elif self.last_speed is not None and random.random() < stop_light_chance:
            new_speed = max(self.last_speed + self.max_deceleration, 0)
            if new_speed == 0:
                self.stop_duration = random.randint(5, 10)
        else:
            keep_speed_chance = 0.7

            if self.last_speed is not None and random.random() < keep_speed_chance:
                new_speed = self.last_speed
            else:
                if self.last_speed is not None:
                    min_next_speed = max(self.last_speed + self.max_deceleration, self.speed_range[0])
                    max_next_speed = min(self.last_speed + self.max_acceleration, self.speed_range[1])
                    new_speed = random.uniform(min_next_speed, max_next_speed)
                else:
                    new_speed = random.uniform(*self.speed_range)

        speed_change = new_speed - self.last_speed
        if speed_change > self.max_acceleration:
            new_speed = self.last_speed + self.max_acceleration
        elif speed_change < self.max_deceleration:
            new_speed = self.last_speed + self.max_deceleration

        self.valor = new_speed
        self.last_speed = self.valor
        self.speeds.append(self.valor)

    def get_last_speed(self):
        return self.valor

    def update_temperature(self):
        temp_change = (self.velocity + self.acceleration) * random.uniform(0.01, 0.1)
        
        cooling_factor = 0.1
        
        net_temp_change = temp_change - cooling_factor * (self.temperature - 20)
        
        self.temperature += net_temp_change
        
        self.temperature = max(min(self.temperature, self.temp_range[1]), self.temp_range[0])

        self.temperatures.append(self.temperature)

    def update_car(self):
        self.velocity += random.uniform(-1, 1)
        self.acceleration += random.uniform(-0.5, 0.5)
        
        self.velocity = max(min(self.velocity, self.velocity_range[1]), self.velocity_range[0])
        self.acceleration = max(min(self.acceleration, self.acceleration_range[1]), self.acceleration_range[0])

    def get_last_temperature(self):
        return self.temperature