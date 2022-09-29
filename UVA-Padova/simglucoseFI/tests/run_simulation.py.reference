from collections import namedtuple
import gym,os
import pandas as pd
from sys import argv
# import pandas as pd
from simglucose.controller.basal_bolus_ctrller import BBController
from simglucose.controller.pid_ctrller import PIDController

Observation = namedtuple('Observation', ['CGM'])
Patient_list=['adult#001','adult#002','adult#003','adult#004','adult#005','adult#006','adult#007','adult#008','adult#009','adult#010', ]
threshold_col_list =['patientA', 'patientB', 'patientC' ,'patientD', 'patientE','patientF', 'patientG', 'patientH', 'patientI' ,'patientJ']

PID_parameters=[

#  [-8.32E-05, -1.00E-07, -1.00E-02],
#  [-3.02E-04, -1.00E-07, -1.00E-02],
#  [-2.87E-06, -6.07E-08, -1.00E-02],
#  [-2.87E-05, -3.49E-07, -3.98E-03],
#  [-1.00E-04, -1.00E-07, -1.00E-02],
#  [-1.00E-04, -5.75E-07, -1.00E-02],
#  [-1.35E-06, -1.58E-07, -1.00E-02],
#  [-4.72E-06, -1.00E-07, -1.00E-02],
#  [-1.00E-04, -1.00E-07, -1.00E-02],
#  [-6.31E-05, -1.00E-07, -1.00E-02]

#MA
[ -1.00E-05, -1.00E-07, -3.49E-03],
[ -4.54E-10, -6.31E-07, -6.31E-03],
[ -4.54E-10, -4.37E-07, -1.00E-03],
[ -1.74E-06, -6.31E-07, -1.00E-03],
[ -4.98E-07, -1.00E-07, -1.00E-03],
[ -4.54E-10, -1.00E-06, -2.87E-03],
[ -3.73E-07, -6.92E-07, -2.75E-03],
[ -1.00E-04, -3.49E-07, -3.49E-03],
[ -4.54E-10, -1.00E-07, -3.49E-03],
[ -4.54E-10, -1.00E-07, -1.00E-03]

]

insulin_list =[]

def iobCalcBilinear(treatment_insulin, minsAgo, dia=3.0): 

    default_dia = 3.0 # assumed duration of insulin activity, in hours
    peak = 75;        # assumed peak insulin activity, in minutes
    end = 180;        # assumed end of insulin activity, in minutes

    # Scale minsAgo by the ratio of the default dia / the user's dia 
    # so the calculations for activityContrib and iobContrib work for 
    # other dia values (while using the constants specified above)
    timeScalar = default_dia / dia; 
    scaled_minsAgo = timeScalar * minsAgo


    activityContrib = 0;  
    iobContrib = 0;       

    # Calc percent of insulin activity at peak, and slopes up to and down from peak
    # Based on area of triangle, because area under the insulin action "curve" must sum to 1
    # (length * height) / 2 = area of triangle (1), therefore height (activityPeak) = 2 / length (which in this case is dia, in minutes)
    # activityPeak scales based on user's dia even though peak and end remain fixed
    activityPeak = 2 / (dia * 60)  
    slopeUp = activityPeak / peak
    slopeDown = -1 * (activityPeak / (end - peak))

    if (scaled_minsAgo < peak) :

        # activityContrib = treatment_insulin * (slopeUp * scaled_minsAgo)

        x1 = (scaled_minsAgo / 5) + 1;  # scaled minutes since bolus, pre-peak; divided by 5 to work with coefficients estimated based on 5 minute increments
        iobContrib = treatment_insulin * ( (-0.001852*x1*x1) + (0.001852*x1) + 1.000000 )

    elif (scaled_minsAgo < end) :

        minsPastPeak = scaled_minsAgo - peak
        # activityContrib = treatment_insulin * (activityPeak + (slopeDown * minsPastPeak))

        x2 = ((scaled_minsAgo - peak) / 5);  # scaled minutes past peak; divided by 5 to work with coefficients estimated based on 5 minute increments
        iobContrib = treatment_insulin * ( (0.001323*x2*x2) + (-0.054233*x2) + 0.555560 )
    
    return(  iobContrib)

def cal_single_iob(treatment_insulin,dia=3):
    iob = 0
    insulin_list.append(treatment_insulin) #update the insulin list with the newest treatment_insulin
    time_scale = int(dia*60/5)

    if len(insulin_list) > time_scale:
        insulin_list.pop(0) #remove the oldest inslin history if length of linslin list is larger than time scale

    length = min(time_scale,len(insulin_list))

    minsAgo = 0 
    for i in range(len(insulin_list)):
        minsAgo += 5 #5 minutes a step
        iob += iobCalcBilinear(insulin_list[-1-i],minsAgo,dia)

    # print(iob)
    
    return (iob)



def save_results(path,df,patient_name):
    # df = self.results()
    if not os.path.isdir(path):
        os.makedirs(path)
    filename = os.path.join(path, str(patient_name) + '.csv')
    df.to_csv(filename)

# def Run_simulation():
class Run_simulation(object):

    def __init__(
        self,
        es=None,
        policy=None,
        patient_id=1,
        Initial_Bg=0):
        self.es=es
        self.policy = policy
        self.patient_id=patient_id
        self.Initial_Bg =Initial_Bg
    
        # action1 = env.action_space.new_tensor_variable(
        #     'action',
        #     extra_dims=1,
        # )
        # obs1=env.observation_space.new_tensor_variable('obs',extra_dims=1,)
        # print (qf.get_qval_sym(Observation(CGM=180),action1))
        # for bg in range(120,200):
        #     # print(algo.policy.get_action(Observation(CGM=bg)))
        #     print(es.get_action(1, Observation(CGM=bg), policy) )
    
    @staticmethod
    def run(es=None,policy=None,patient_id=1,Initial_Bg=0):
        # es=self.es[0]
        print(es)
        env = gym.make('simglucose-adult{}-CHO{}-v0'.format(Initial_Bg,patient_id+1))

        ctrller = BBController()
        # ctrller = PIDController(P=0.001, I=0.00001, D=0.001)
        # ctrller = PIDController(P=PID_parameters[patient_id][0], I=PID_parameters[patient_id][1], D=PID_parameters[patient_id][2])

        reward = 0
        done = False
        info = {'sample_time': 5,
                'patient_name': 'adult#001',
                'meal': 0}

        observation = env.reset()
        pre_glucose = 0
        pre_rate = 0

        ##########################mitigation##################
        Monitor = 2#2 #0:CAWT; 1:MPC 2:DT
        Mitigation_Enable = True
        threshold_col = threshold_col_list[patient_id]+'_CV0'
        if Mitigation_Enable:
        #====read threshold files############
            thresholds=pd.read_csv("/home/uva-dsa/Research/Medical/test/openaps_monitor/Reseult/scripts-12rules_uvasimulator/thresholds.csv")
            threshold=thresholds[threshold_col]
            mitigate_H1_flag = False
            mitigate_H2_flag = False
            if Monitor == 2:
                import numpy as np
                from sklearn.externals import joblib
                model_name = '/home/uva-dsa/Research/Medical/test/openaps_monitor/Reseult/script_jupyternotebook/saved_model_Uva/DT/DT3_NoFIlabel_model_{}.sav'.format(threshold_col)
                print("Load model {} now!".format(model_name))
                clf = joblib.load(model_name)
        delBg = 0
        delIob = 0
        delInsulinRate = 0
        pre_insulinRate = 0
        pre_iob =0
        pre_bg =0

        ######################################################

        for t1 in range(150):
            t = t1 -30 #wait 30*5=150 minutes
            # env.render(mode='human')
            glucose = observation.CGM
            # print(observation)
            glucose_refresh = True 
            rate_refresh = True # update the glucose reading and rate output command


            #Fault injection Hook################
            #glucose:HOOK#


            #hold the glucose value when fresh signal is false
            if glucose_refresh != True:
                glucose = pre_glucose
            #update observation
            if observation.CGM != glucose:
                observation=Observation(CGM=glucose)
                print(observation)

            

            #get the action beased on policy and observation
            # (1) random action
            # action = env.action_space.sample()
            # (2) PID or BB control action
            ctrl_action = ctrller.policy(observation, reward, done, **info)
            action = ctrl_action.basal + ctrl_action.bolus
            # # (3) RL or DDPG action     
            # action,_ = policy.get_action(observation)# action = es.get_action(t, observation, policy) #algo.policy.get_action(observation)
            # print(action)
            # print(es.get_action(t, observation, policy))

            #Fault injection Hook################
            #rate:HOOK#

            
            #hold the action value when fresh signal is false
            if rate_refresh != True:
                action = pre_rate

            #take the action
            observation, reward, done, info = env.step(action)
            #update previous glucose and rate value
            pre_glucose = glucose

            ############################################3#
            #==========mitigation code####++==============
            if Mitigation_Enable:
                bg=glucose
                insulinRate = action
                bgTarget = 140
                iob =cal_single_iob(insulinRate)
                if t1 >1:
                    delBg = bg-pre_bg #data["CGM_glucose"][i] - data["CGM_glucose"][i-1]
                    delIob = iob - pre_iob #data["IOB"][i] - data["IOB"][i-1]
                    delInsulinRate = insulinRate-pre_insulinRate #data["rate"][i] - data["rate"][i-1]

                if t1 >5:
                    sub_alert_msg = ""
                    if Monitor==0: #CAWT
                        sub_alert_flag = False
                        if bg > 180 and delBg > 5: #insufficient insulin
                                if iob <threshold[6] and insulinRate<0.1 :
                                        sub_alert_flag = True
                                        sub_alert_msg = "row_7" # rule14->7

                        if bg > bgTarget+10: #+10?  >150
                                #if delBg >= -3:
                                # if bg>180 and iob < -0.120728641206 and insulinRate == 0: # row_37
                                # if bg>180 and 

                                if delBg > 0.3:
                                        # if bg>190:
                                        if delBg>2.5 and delIob <= 0 and iob <threshold[4]:#-0.3: #row_10 IOB is falling 
                                                if delInsulinRate == 0 and insulinRate<0.1: #keep insulin
                                                        sub_alert_flag = True
                                                        sub_alert_msg = "row_5" # rule10 ->5
                                        elif delIob < 0 and iob <  0:#threshold[0]:#0.145605040799: # row_1
                                                if delInsulinRate < 0: #dec_insulin
                                                        sub_alert_flag = True
                                                        sub_alert_msg = "row_1"
                                        elif delIob == 0 and iob <  threshold[1]: # row_2
                                                if delInsulinRate < 0:  #dec_insulin
                                                        sub_alert_flag = True
                                                        sub_alert_msg = "row_2"

                        else:   #BG<HBGT 
                            if bg < threshold[8]:#bgLowerTh:
                                if insulinRate != 0 :#and iob>-0.5:#zero insulin
                                    sub_alert_flag = True
                                    sub_alert_msg = "row_9"

                            elif bg < bgTarget+10: #110

                                if delBg < -0.3:
                                    if delIob >=0 and iob >threshold[5]:#0.3: # IOB is not falling
                                        if delInsulinRate == 0 and insulinRate>0.05 :
                                            sub_alert_flag = True
                                            sub_alert_msg = "row_6" # rule12->6
                                                    
                                    # checking if BG is falling more than the threshold
                                    #if delBg < thBgFall:
                                    # if bg<80: 
                                    if delIob > 0 and iob > threshold[2]:#-0.199631233636: # row_7->3
                                        if delInsulinRate > 0.05:
                                            sub_alert_flag = True
                                            sub_alert_msg = "row_3"
                                    elif delIob == 0 and iob > threshold[3]: # row_8->4
                                        if delInsulinRate > 0.05:
                                            sub_alert_flag = True
                                            sub_alert_msg = "row_4"
                    
                        if sub_alert_flag:
                            if sub_alert_msg in ["row_3","row_4","row_6","row_9","row_13"]:#H1hazard
                                mitigate_H1_flag = True
                            elif sub_alert_msg in ["row_1","row_2","row_5","row_7"]:#H2hazard
                                mitigate_H2_flag = True


                    #==========mitigation code####++==============
                    elif Monitor ==1: #MPC
                        if glucose <70 :#H1hazard
                            # insulinRate = 0
                            # loaded_suggested_data["fault"] = "yes"
                            # loaded_suggested_data["fault_reason"] = sub_alert_msg+"_Mitigation" 
                            # print("\n***************************************")
                            # print("********** Unsafe Action !!!!! *************")    
                            sub_alert_msg = 'H1'
                            mitigate_H1_flag = True
                        elif glucose>180:#H2hazard
                            # insulinRate  = 2.1
                            # loaded_suggested_data["fault"] = "yes"
                            # loaded_suggested_data["fault_reason"] = sub_alert_msg+"_Mitigation" 
                            # print("\n***************************************")
                            # print("********** Unsafe Action !!!!! *************")    
                            sub_alert_msg = 'H2'
                            mitigate_H2_flag = True

                    elif Monitor == 2: #DT
                        predict_proba=clf.predict_proba(np.array([glucose,iob,insulinRate]).reshape(1,-1))
                        if int(np.argmax(predict_proba,axis=1)):
                            if glucose < bgTarget:
                                sub_alert_msg = 'H1'
                                mitigate_H1_flag = True
                            else:#H2hazard
                                sub_alert_msg = 'H2'
                                mitigate_H2_flag = True

                    #########start to mitigate#########
                    if mitigate_H1_flag == True: 
                        if insulinRate   < pre_insulinRate or glucose>bgTarget+10:#if fault is removed stop mitigation
                            mitigate_H1_flag = False #reset hazard flag
                        insulinRate = 0

                        print("\n***************************************")
                        print(sub_alert_msg)
                        print("********** Unsafe Action !!!!! *************")    

                    elif mitigate_H2_flag == True: 
                        if insulinRate  > pre_insulinRate or glucose<bgTarget+40:#if fault is removed stop mitigation
                            mitigate_H2_flag = False
                        insulinRate  = 0.1 #0.1

                        print("\n***************************************")
                        print(sub_alert_msg)
                        print("********** Unsafe Action !!!!! *************")    

                pre_insulinRate = insulinRate
                pre_iob = iob
                pre_bg =bg                                
            #######################33End of mitigation######################################

            pre_rate = action

            # if done:
            #     print("Episode finished after {} timesteps".format(t + 1))
            #     break
        
        # print(env.show_history())
        save_results('./simulation_data/',env.show_history(),Patient_list[patient_id])
        env.close()

# if __name__ == "__main__":
#     Run_simulation(argv[1],argv[2])  