import unittest
from gym.envs.registration import register
# from tests.run_Faultinjection_monitor import FInject
from collections import namedtuple
import gym,os

Observation = namedtuple('Observation', ['CGM'])
# Patient_list=['adult#001','adult#002','adult#003','adult#004','adult#005','adult#006','adult#007','adult#008','adult#009','adult#010', ]

def Rigister_patient(patient_id=1,Initial_Bg=0):
    Patient_list=['adult#001','adult#002','adult#003','adult#004','adult#005','adult#006','adult#007','adult#008','adult#009','adult#010', ]
    register(
        id='simglucose-adult{}-CHO{}-v0'.format(Initial_Bg,patient_id+1),
        entry_point='simglucose.envs:T1DSimEnv',
        kwargs={
            'patient_name': Patient_list[patient_id],
            'Initial_Bg': Initial_Bg
        })
    


# class testRLLab(unittest.TestCase):
#     def test_rllab(self):
def test_rllab(patient_id=1,Initial_Bg=0):
        try:
            from rllab.algos.ddpg import DDPG
            from rllab.envs.normalized_env import normalize
            from rllab.exploration_strategies.ou_strategy import OUStrategy
            from rllab.policies.deterministic_mlp_policy import DeterministicMLPPolicy
            from rllab.q_functions.continuous_mlp_q_function import ContinuousMLPQFunction
            from rllab.envs.gym_env import GymEnv
        except ImportError:
            print('rllab is not installed!')
            return None

        env = GymEnv('simglucose-adult{}-CHO{}-v0'.format(Initial_Bg,patient_id+1))
        env = normalize(env)

        policy = DeterministicMLPPolicy(
            env_spec=env.spec,
            # The neural network policy should have two hidden layers, each
            # with 32 hidden units.
            hidden_sizes=(32, 32))

        es = OUStrategy(env_spec=env.spec)

        qf = ContinuousMLPQFunction(env_spec=env.spec)

        algo = DDPG(
            env=env,
            policy=policy,
            es=es,
            qf=qf,
            batch_size=32,
            max_path_length=100,
            epoch_length=1000,
            min_pool_size=10000,
            n_epochs=5,
            discount=0.99,
            scale_reward=0.01,
            qf_learning_rate=1e-3,
            policy_learning_rate=1e-4)
        algo.train()

        # env.close()

        return es,policy

if __name__ == '__main__':
    # unittest.main()
    for patient_id in range(1):
        Rigister_patient(patient_id)
        es,policy=test_rllab(patient_id)

        # fi=FInject(
        #     'fault_library_monitor_V2/scenario_9',
        #     es=es,
        #     policy=policy,
        #     patient_id=patient_id
        #     )
        # fi.inject_fault()

        # os.system('./run_fault_inject_monitor_V2_campaign.sh '+es + policy)#+title[1]+' '+startWord[1]) #pass scenario and fault num to the .sh script

        # Run_simulation(es,policy,patient_id)