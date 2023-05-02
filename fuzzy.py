# -*- coding: utf-8 -*-
"""fuzzy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17olUTMLD6ypmofUAM6Z6acUatTjPKT2M

# Trabalho Fuzz

## Import Libs
"""
import skfuzzy as fz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

"""## Get infos"""

data = pd.read_csv('historicoGravidadeLabel.txt', sep='|', header=0)

data

"""## Normalize and create the antecent & consequent"""

q = np.linspace(data['qPa'].min(),data['qPa'].max(), len(data))
p = np.linspace(data['pulse'].min(),data['pulse'].max(), len(data))
r = np.linspace(data['resp'].min(),data['resp'].max(), len(data))
g = np.linspace(data['gravity'].min(),data['gravity'].max(), len(data))

qPa = ctrl.Antecedent(q, 'qPa')
pulse = ctrl.Antecedent(p, 'pulse')
resp = ctrl.Antecedent(r, 'resp')

gravity = ctrl.Consequent(g, 'gravity')

"""## Create MembershipFunction"""

qPa.automf(names=["poor", "good","high"])
# = fz.gaussmf(resp.universe, -9, 9)
#qPa['average'] = fz.gaussmf(resp.universe,-1,9)
'''
pulse['poor'] = fz.trimf(pulse.universe, [0, 0, 70])
pulse['good'] = fz.trimf(pulse.universe, [40, 70, 100])
pulse['high'] = fz.trimf(pulse.universe, [70, 200, 200])'''
pulse.automf(names=["poor", "good","high"])

'''
resp['poor'] = fz.trimf(resp.universe, [0, 0, 14])
resp['good'] = fz.trimf(resp.universe, [9, 14, 19])
resp['high'] = fz.trimf(resp.universe, [14, 22, 22])
'''
resp.automf(names=["poor", "good","high"])

gravity.automf(names=["critical","unstable", "potentially unstable","stable"])

'''
gravity['critical'] = fz.trimf(gravity.universe, [12, 12, 19])
gravity['unstable'] = fz.trimf(gravity.universe, [12, 19, 38])
gravity['potentially unstable'] = fz.trimf(gravity.universe, [19, 38, 80])
gravity['stable'] = fz.trim'(gravity.universe, [38, 80, 80 ])'''

qPa.view()
pulse.view()
resp.view()
gravity.view()

"""## Rules From Spec"""

rules_ctrl_spec = []

#1
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["poor"] | resp["poor"],gravity["critical"]))
#2
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["poor"] | resp["high"],gravity["critical"]))
#3
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["poor"] | resp["good"],gravity["unstable"]))
#4
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["high"] | resp["high"],gravity["critical"]))
#5
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["high"] | resp["poor"],gravity["critical"]))
#6
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["high"] | resp["good"],gravity["unstable"]))
#7
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["good"] | resp["poor"],gravity["unstable"]))
#8
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["good"] | resp["high"],gravity["unstable"]))
#9
rules_ctrl_spec.append(ctrl.Rule(qPa["poor"]  |  pulse["good"] | resp["good"],gravity["potentially unstable"]))

#10
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["poor"] | resp["poor"],gravity["critical"]))
#11
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["poor"] | resp["high"],gravity["critical"]))
#12
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["poor"] | resp["good"],gravity["unstable"]))
#13
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["high"] | resp["poor"],gravity["critical"]))
#14
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["high"] | resp["good"],gravity["unstable"]))
#15
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["high"] | resp["high"],gravity["critical"]))
#16
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["good"] | resp["poor"],gravity["unstable"]))
#17
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["good"] | resp["high"],gravity["unstable"]))
#18
rules_ctrl_spec.append(ctrl.Rule(qPa["high"]  |  pulse["good"] | resp["good"],gravity["potentially unstable"]))


#10
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["poor"] | resp["poor"],gravity["unstable"]))
#11
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["poor"] | resp["high"],gravity["unstable"]))
#12
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["poor"] | resp["good"],gravity["potentially unstable"]))
#13
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["high"] | resp["poor"],gravity["unstable"]))
#14
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["high"] | resp["good"],gravity["potentially unstable"]))
#15
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["high"] | resp["high"],gravity["unstable"]))
#16
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["good"] | resp["poor"],gravity["potentially unstable"]))
#17
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["good"] | resp["high"],gravity["potentially unstable"]))
#18
rules_ctrl_spec.append(ctrl.Rule(qPa["good"]  |  pulse["good"] | resp["good"],gravity["stable"]))

"""## Rules From Wang Mandel"""

rules = []
for _, row in data.iterrows():
  listX1 , listX2, listX3 ,listY = [],[],[],[]
  #qPA
  listX1.append(fz.interp_membership(data['qPa'],
                                      qPa["poor"].mf,
                                      row["qPa"]))
  listX1.append(fz.interp_membership(data['qPa'],
                                      qPa["good"].mf,
                                      row["qPa"]))
  listX1.append(fz.interp_membership(data['qPa'],
                                      qPa["high"].mf,
                                      row["qPa"]))

  #pulse
  listX2.append(fz.interp_membership(data['pulse'],
                                      pulse["poor"].mf,
                                      row["pulse"]))
  listX2.append(fz.interp_membership(data['pulse'],
                                      pulse["good"].mf,
                                      row["pulse"]))
  listX2.append(fz.interp_membership(data['pulse'],
                                      pulse["high"].mf,
                                      row["pulse"]))

  #resp
  listX3.append(fz.interp_membership(data['resp'],
                                      resp["poor"].mf,
                                      row["resp"]))
  listX3.append(fz.interp_membership(data['resp'],
                                      resp["good"].mf,
                                      row["resp"]))
  listX3.append(fz.interp_membership(data['resp'],
                                      resp["high"].mf,
                                      row["resp"]))


  #gravity
  listY.append(fz.interp_membership(data['gravity'],
                                      gravity["critical"].mf,
                                      row["gravity"]))
  listY.append(fz.interp_membership(data['gravity'],
                                      gravity["unstable"].mf,
                                      row["gravity"]))
  listY.append(fz.interp_membership(data['gravity'],
                                      gravity["potentially unstable"].mf,
                                      row["gravity"]))
  listY.append(fz.interp_membership(data['gravity'],
                                      gravity["stable"].mf,
                                      row["gravity"]))

  x1Max , x2max , x3max, ymax = np.argmax(listX1) , np.argmax(listX2), np.argmax(listX3), np.argmax(listY)
  degree = listX1[x1Max] * listX2[x2max] * listX3[x3max] * listY[ymax]
  rules.append([x1Max,x2max,x3max , ymax , degree])

print('primitive Rules:')
print('we have',len(rules),'rules!','\n')

unique = np.unique(rules, axis=0)
print('unique rule: ')
print(len(unique))

array_rule = {}
for i in unique:
  t = str(i[:-1])
  if t not in array_rule:
    array_rule[t] = i[-1]
  elif array_rule[t] < i[-1]:
    array_rule[t] = i[-1]

print('finall rules: ')
print(len(array_rule))

def convertRule(i):
  i = int(i)
  if i == 0 :
    return "poor"
  if i == 1:
    return "high"
  if i == 2:
    return "good"

def convertRuleG(i):
  i = int(i)
  if i == 0:
    return "critical"
  if i == 1:
    return "unstable"
  if i == 2:
    return "potentially unstable"
  if i == 3:
    return "stable"

rules_ctrl = []
for i in array_rule:
  l = [float(x) for x in i[1:-1].split()]
  _qPa = convertRule(l[0])
  _pulse = convertRule(l[1])
  _resp = convertRule(l[2])
  _gravity = convertRuleG(l[3])
  rules_ctrl.append(ctrl.Rule(qPa[_qPa] | pulse[_pulse] | resp[_resp],gravity[_gravity] ))

"""## Simulation"""

def state_gravity(value):
  if value <= 25:
    return "critico"
  if value <= 50:
    return "instavel"
  if value <= 75:
    return "potEstavel"
  if value <= 100:
    return "estavel"
  return "err"

def simulation(data,sim):
  erro = 0
  rms = 0
  for index, row in data.iterrows():
    sim.input["qPa"] = row["qPa"]
    sim.input["pulse"] = row["pulse"]
    sim.input["resp"] = row["resp"]
    sim.compute()
    fuzzy_result = sim.output["gravity"]
    label = state_gravity(fuzzy_result)
    if label != row["label"].replace("'",""):
        erro += 1
    rms += (fuzzy_result - row["gravity"])**2
  N = len(data)
  print("Pco: {}".format(100*(N-erro)/N))
  print("erro {}".format(erro))
  print("RMSE: {}".format(math.sqrt(1/N*rms)))

"""### By Specialist"""

sim =  ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules=rules_ctrl_spec))

sim.input["qPa"] = 8.6096
sim.input["pulse"] = 51.3438
sim.input["resp"] = 21.0420
sim.compute()
sim.output["gravity"]
#8.6096|51.3438|21.0420

simulation(data, sim)

"""### By Wang Mandel"""

sim_wang =  ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules=rules_ctrl))

simulation(data, sim_wang)

