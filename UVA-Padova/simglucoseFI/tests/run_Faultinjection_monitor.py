import os
import os.path
import numpy as np
import time
from sys import argv
from collections import namedtuple
from importlib import reload
from tests.test_rllab import Rigister_patient,test_rllab
import tests.run_simulation
import pandas as pd



Observation = namedtuple('Observation', ['CGM'])
Patient_list=['adult#001','adult#002','adult#003','adult#004','adult#005','adult#006','adult#007','adult#008','adult#009','adult#010', ]
threshold_col_list =['patientA', 'patientB', 'patientC' ,'patientD', 'patientE','patientF', 'patientG', 'patientH', 'patientI' ,'patientJ']


def insert_fault_code(fileLoc, faultLoc, codeline):
  brk = 0
  bkupFile = fileLoc+'.bkup'
  if os.path.isfile(bkupFile) != True:
    cmd = 'cp ' + fileLoc + ' ' + bkupFile
    os.system(cmd)
  else:
    print('Bkup file already exists!!')

  src_fp = open(fileLoc, 'w')
  bkup_fp = open(bkupFile, 'r')

  for line in bkup_fp:
    src_fp.write(line)
    if brk>0:
      for i in range(1, leadSp+1):
        src_fp.write(' ')
      src_fp.write('else:'+'\n')
      for l in np.arange(brk,len(codeline)):
        for i in range(1, leadSp+3):
          src_fp.write(' ')
        src_fp.write(codeline[l]+'\n')

    brk = 0

    if faultLoc in line:
      print ("injected 888")
      leadSp = len(line) - len(line.lstrip(' ')) # calculate the leading spaces

      for i in range(1, leadSp+1):
        src_fp.write(' ')
      src_fp.write(codeline[0]+'\n')

      for l in np.arange(1,len(codeline)):
        if codeline[l] != 'none\n':
          for i in range(1, leadSp+3):
            src_fp.write(' ')
          src_fp.write(codeline[l]+'\n')
        else:
          brk=l+1
          for i in range(1,3):
            src_fp.write(' ')
          break

  src_fp.close()
  bkup_fp.close()

# def inject_fault(fileName,es,policy):
class FInject(object):

  def __init__(
            self,
            fileName,
            es,
            policy,
            patient_id=1,
            Initial_Bg=0,
            file_testlist = None,
            test_result = None):
    self.fileName =fileName
    self.es = es
    self.policy = policy
    self.patient_id=patient_id
    self.Initial_Bg=Initial_Bg
    self.file_testlist=file_testlist
    self.test_result=test_result

  def inject_fault(self):
    # global start_time_0
    in_file = self.fileName+'.txt'
    # outfile_path = 'out/'
    sceneLine  = self.fileName.split('_')
    sceneNum = sceneLine[len(sceneLine)-1]

    # # recFaultTime="//fltTime=open(\'out/fault_times.txt\',\'a+\')//fltTime.write(str(time.time())+\'||\')//fltTime.close()"
    # recFaultTime="//fltTime=open(\'out/fault_times.txt\',\'a+\')//fltTime.write(str(_)+\'||\')//fltTime.close()"

    # name_end = 0
    # name_id = []
    # fileNames = os.listdir("./result")
    # #rint("Num of Line",len(fileNames))
    # if len(fileNames) == 0:
    #   name_end = 0
    # else:
    #   for name in fileNames:
    #     name_id.append(int(((name.split('_')[1])).split('.')[0]))
    #   name_end = max(name_id)

    with open(in_file, 'r') as fp:
      print( in_file)
      line = fp.readline() # title line
      tLine = line.split('-')
      hz = tLine[len(tLine)-1].replace('\n','')
      title_num = line.split(':')
      scene_num = title_num[1].split('_')
      title = line.split(':')
      title[1] = title[1].replace('\n','')

      # if os.path.isdir('../output_files/'+title[1]) != True:
      #   os.makedirs('../output_files/'+title[1])

      # hazardFile = open('../output_files/'+title[1]+'/Hazards.txt','w')
      # alertFile = open('../output_files/'+title[1]+'/Alerts.txt','w')
      # summFile = open('../output_files/'+title[1]+'/summary.csv','w')

      # summLine = 'Scenario#,Fault#,Fault-line,Alerts,Hazards,T1,T2,T3\n'
      # summFile.write(summLine)

      # hazardFile.close()
      # alertFile.close()
      # summFile.close()

      # hazardFile = open('../output_files/'+title[1]+'/Hazards.txt','a+')
      # alertFile = open('../output_files/'+title[1]+'/Alerts.txt','a+')
      # summFile = open('../output_files/'+title[1]+'/summary.csv','a')

      line = fp.readline() # fault location line
      lineSeg = line.split('//')
      fileLoc = lineSeg[1]
      faultLoc = lineSeg[2]
      for line in fp:
        # line = line + recFaultTime
        lineSeg = line.split('//')
        startWord = lineSeg[0].split(' ')
        del lineSeg[0]

        if startWord[0]=='fault':
          print("+++++++++++Initial_Bg="+str(self.Initial_Bg)+'//'+title[1]+'//fault '+startWord[1]+"++++++++++++++")
          if MITIGATION >0:
            scenario_inf = title[1]
            scenario_num=int(scenario_inf.split('_')[0])
            fault_num=int(startWord[1])    
            patient =threshold_col_list[self.patient_id]        
            filename_test = '../simulationCollection_uvasimulator/{}/{}/{}/data_{}_{}.csv'.format(patient,scenario_inf,fault_num,patient, self.Initial_Bg)
            if not (filename_test in self.file_testlist):
              continue

            datastream_test = self.test_result[self.test_result['Scenario']==scenario_num]
            datastream_test = datastream_test[datastream_test['fault']==fault_num]            
            if Monitor == 2: #DT
              if MITIGATION ==1: #TP
                if not (filename_test in tps):
                  continue
              elif MITIGATION ==2:
                if not (filename_test in fps): #only test FP cases: alert>0 and hazard==0
                  continue

            else:
              alert_num = int(datastream_test[datastream_test['init_bg']==self.Initial_Bg]['alert_num'].tolist()[0])
              hazard_num = int(datastream_test[datastream_test['init_bg']==self.Initial_Bg]['hazard_num'].tolist()[0])
              if MITIGATION ==1:
                if hazard_num<1: #only test on hazardous cases P:TP+FN
                  continue
              elif MITIGATION ==2:
                if alert_num<1 or hazard_num>0: #only test FP cases: alert>0 and hazard==0
                  continue
              print('alert_num={},hazard_num={}'.format(alert_num,hazard_num))

          insert_fault_code(fileLoc, faultLoc, lineSeg)
          # print(os.getcwd())

          # print(self.es.get_action(1, Observation(CGM=180), self.policy))
          # print(self.es)

          # os.system('python3 run_simulation.py  '+self.es + '  ' +self.policy)#+title[1]+' '+startWord[1]) #pass scenario and fault num to the .sh script
         
          
          ##############reload tests.run_simulation and Run_simulation function#######
          # from importlib import reload
          # import tests.run_simulation
          reload(tests.run_simulation)
          from tests.run_simulation import Run_simulation
          ############################################################################


          rs=Run_simulation(
            es=self.es,
            policy=self.policy,
            patient_id=self.patient_id,
            Initial_Bg=self.Initial_Bg)

          #use static method as there is some problem in transmiting parameters using default method
          rs.run(es=self.es,
            policy=self.policy,
            patient_id=self.patient_id,
            Initial_Bg=self.Initial_Bg)

          # cmd = 'rm run_simulation.pyc' 
          # os.system(cmd)

          '''Copy all output files in a common directory'''
          # cmd = 'cp -a ' + outfile_path+'/.' + ' ' + output_dir
          # os.system(cmd)

          patient_name =str(Patient_list[patient_id])
          dir_source = './simulation_data'
          if os.path.isdir(dir_source) == True:
            dir_dest = './simulationCollection_Mitigation/'+ patient_name + '/' +title[1]+'/'+startWord[1]
            if os.path.isdir(dir_dest) != True:
              os.makedirs(dir_dest)
            cmd = 'mv -f {}/{} '.format(dir_source,str(patient_name+'.csv')) + ' ' + dir_dest+'/{}_{}.csv'.format(patient_name,Initial_Bg)
            os.system(cmd)
            # cmd = 'rm -rf ./simulation_data'
            # os.system(cmd)
              
            
      
      print('Fault injection and execution done !!!')
      bkupFile = fileLoc+'.bkup'
      refFile = fileLoc+'.reference'       
      cmd = 'cp ' + fileLoc + ' ' + refFile
      os.system(cmd)
      cmd = 'cp ' + bkupFile + ' ' + fileLoc
      os.system(cmd)
      cmd = 'rm ' + bkupFile
      os.system(cmd)

fault_lib=[
  'fault_library_monitor_V2/scenario_9',
  'fault_library_monitor_V2/scenario_12',
  'fault_library_monitor_V2/scenario_13',
  'fault_library_monitor_V2/scenario_14',
  'fault_library_monitor_V2/scenario_17',
  'fault_library_monitor_V2/scenario_18',
  'fault_library_monitor_V2/scenario_19',
  'fault_library_monitor_V2/scenario_20',
  'fault_library_monitor_V2/scenario_21',
  'fault_library_monitor_V2/scenario_22',

]
Fault_Injection_Enable = True
RL_policy_Enable= False
#####################################################
MITIGATION=1 #whether activate mitigation code 0:None; 1:TP; 2:FP; 3:TP+FP
Monitor = 2 #0:CAWT; 1:MPC 2:DT
if Monitor == 2:
	fps = np.load('/home/uva-dsa/Research/Medical/test/openaps_monitor/Reseult/script_jupyternotebook/results_fordt/DT-uva_FPs_list.npy')
	tps = np.load('/home/uva-dsa/Research/Medical/test/openaps_monitor/Reseult/script_jupyternotebook/results_fordt/DT-uva_TPs_list.npy')
##########################################################

if __name__ == "__main__":
      
  start_time_0 = time.time()

  # if len(argv)>3:
  #   fi=FInject(argv[1],argv[2],argv[3])
  #   fi.inject_fault()
  # else:
  #   print('Fault library filename is missing, pass the filename as argument')


  for patient_id in range(10):

    if MITIGATION>0:
      file_testlist = np.load("/home/uva-dsa/Research/Medical/test/openaps_monitor/Reseult/script_jupyternotebook/filelist_Uvasimulator/file_testlist_{}_CV{}.npy".format(threshold_col_list[patient_id],0))
      test_result =pd.read_csv('/home/uva-dsa/Research/Medical/test/openaps_monitor/Reseult/scripts-12rules_uvasimulator/result/CAWT/summary_monitor_hardware_{0}-{0}_CV0.csv'.format(threshold_col_list[patient_id]))
      # test_result =pd.read_csv('/home/uva-dsa/Research/Medical/test/openaps_monitor/Reseult/scripts-12rules_uvasimulator/result/MPC/summary_monitor_hardware_baseline_{}-CV0.csv'.format(threshold_col_list[patient_id]))
    else:
      file_testlist = None
      test_result = None

    for Initial_Bg in range(80,210,20):
      Rigister_patient(patient_id,Initial_Bg)
      #RL controller
      if RL_policy_Enable:
        es,policy=test_rllab(patient_id,Initial_Bg)
      # #otherwise
      else:
        es=0
        policy=0

      
      #inject fault##############################################
      if Fault_Injection_Enable:
        for fault_item in fault_lib:
          fi=FInject(
              fault_item,
              es=es,
              policy=policy,
              patient_id=patient_id,
              Initial_Bg=Initial_Bg,
              file_testlist = file_testlist,
              test_result = test_result
              )
          fi.inject_fault()

      ###run fault free cases####################################
      else:
        from tests.run_simulation import Run_simulation

        rs=Run_simulation(
          es=es,
          policy=policy,
          patient_id=patient_id,
          Initial_Bg=Initial_Bg)

        #use static method as there is some problem in transmiting parameters using default method
        rs.run(es=es,
          policy=policy,
          patient_id=patient_id,
          Initial_Bg=Initial_Bg)

        #save
        patient_name =str(Patient_list[patient_id])
        dir_source = './simulation_data'
        if os.path.isdir(dir_source) == True:
          dir_dest = './simulationCollection_faultfree_PID/'+ patient_name
          if os.path.isdir(dir_dest) != True:
            os.makedirs(dir_dest)
          cmd = 'mv -f {}/{} '.format(dir_source,str(patient_name+'.csv')) + ' ' + dir_dest+'/{}_{}.csv'.format(patient_name,Initial_Bg)
          os.system(cmd)
          # cmd = 'rm -rf ./simulation_data'
          # os.system(cmd)

  print('\n\n Total runtime: %f seconds' %(time.time()-start_time_0))

