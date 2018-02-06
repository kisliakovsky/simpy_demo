from typing import Generator, Any

import simpy


class Car(object):

    def __init__(self, name: str, env: simpy.Environment, charging_station: Any=None):
        self.__name = name
        self.__env = env
        self.__action = env.process(self._run())

    def _run(self) -> Generator[simpy.Timeout, None, None]:
        while True:
            print('Start parking and charging at {}'.format(self.__env.now))
            charge_duration = 5
            try:
                yield self.__env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                print('Was interrupted. Hope, the battery is full enough!')
            print('Start driving at {}'.format(self.__env.now))
            driving_duration = 2
            yield self.__env.timeout(driving_duration)

    def charge(self, duration: int) -> Generator[simpy.Timeout, None, None]:
        yield self.__env.timeout(duration)

    @property
    def action(self):
        return self.__action


class Driver(object):

    def __init__(self, env: simpy.Environment, car: Car):
        self.__env = env
        self.__car = car
        self.__action = env.process(self._run())

    def _run(self):
        yield self.__env.timeout(3)
        self.__car.action.interrupt()

    @property
    def action(self):
        return self.__action


def car(name: str, env: simpy.Environment, charge_station: simpy.Resource,
        driving_time: int, charge_duration: int):
    yield env.timeout(driving_time)
    print('{} arriving at {}'.format(name, env.now))
    with charge_station.request() as request:
        yield request
        print('{} starting to charge at {}'.format(name, env.now))
        yield env.timeout(charge_duration)
        print('{} leaving the charge station at {}'.format(name, env.now))
