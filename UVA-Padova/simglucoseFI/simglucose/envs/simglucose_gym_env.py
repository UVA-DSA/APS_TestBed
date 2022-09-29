from simglucose.simulation.env import T1DSimEnv as _T1DSimEnv
from simglucose.patient.t1dpatient import T1DPatient
from simglucose.sensor.cgm import CGMSensor
from simglucose.actuator.pump import InsulinPump
from simglucose.simulation.scenario_gen import RandomScenario
from simglucose.simulation.scenario import CustomScenario
from simglucose.controller.base import Action
import numpy as np
import pkg_resources
import gym
from gym import spaces
from gym.utils import seeding
from datetime import datetime

PATIENT_PARA_FILE = pkg_resources.resource_filename(
    'simglucose', 'params/vpatient_params.csv')


class T1DSimEnv(gym.Env):
    '''
    A wrapper of simglucose.simulation.env.T1DSimEnv to support gym API
    '''
    metadata = {'render.modes': ['human']}

    def __init__(self, patient_name=None, reward_fun=None, Initial_Bg=0):
        '''
        patient_name must be 'adolescent#001' to 'adolescent#010',
        or 'adult#001' to 'adult#010', or 'child#001' to 'child#010'
        '''
        seeds = self._seed()
        # have to hard code the patient_name, gym has some interesting
        # error when choosing the patient
        if patient_name is None:
            patient_name = 'adolescent#001'
        patient = T1DPatient.withName(patient_name,Initial_Bg)
        sensor = CGMSensor.withName('GuardianRT', seed=seeds[1])#Dexcom
        hour = 20#self.np_random.randint(low=0.0, high=24.0)
        start_time = datetime(2018, 1, 1, hour, 0, 0)
        # scenario = RandomScenario(start_time=start_time, seed=seeds[2])
        # custom scenario is a list of tuples (time, meal_size)
        # scen = [(0,float(Initial_Bg)),(13, 45), (16, 10), (18, 35), (22, 10)]#, (23, 10)]
        scen = [(13, 45), (16, 10), (18, 35), (22, 10)]#, (23, 10)]
        scenario = CustomScenario(start_time=start_time, scenario=scen)

        pump = InsulinPump.withName('Insulet')
        self.env = _T1DSimEnv(patient, sensor, pump, scenario)
        self.reward_fun = reward_fun

    def _step(self, action):
        # This gym only controls basal insulin
        act = Action(basal=action, bolus=0)
        if self.reward_fun is None:
            return self.env.step(act)
        else:
            return self.env.step(act, reward_fun=self.reward_fun)

    def _reset(self):
        obs, _, _, _ = self.env.reset()
        return obs

    def _seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed=seed)
        # Derive a random seed. This gets passed as a uint, but gets
        # checked as an int elsewhere, so we need to keep it below
        # 2**31.
        seed2 = seeding.hash_seed(seed1 + 1) % 2**31
        seed3 = seeding.hash_seed(seed2 + 1) % 2**31
        return [seed1, seed2, seed3]

    def _render(self, mode='human', close=False):
        self.env.render(close=close)
    
    def show_history(self):
        df = self.env.show_history()
        return df

    @property
    def action_space(self):
        ub = self.env.pump._params['max_basal']
        return spaces.Box(low=0, high=ub, shape=(1,))

    @property
    def observation_space(self):
        return spaces.Box(low=0, high=np.inf, shape=(1,))
