import simpy

from src.car_model import Car, Driver, car

env = simpy.Environment()
# car = Car("Ferrari", env)
# driver = Driver(env, car)

charge_station = simpy.Resource(env, capacity=2)
for i in range(4):
    env.process(car('Car {}'.format(i), env, charge_station, i * 2, 5))

env.run(until=15)
