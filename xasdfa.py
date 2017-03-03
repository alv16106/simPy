# -*- coding: cp1252 -*-

#Rodrigo Alvarado 16106
#Michelle Bloomfield 16803

import simpy
import random
from time import time

class globales:
    rtot=0
tiempo_inicial = time() 
def x(nombre,env, ram, cpu):
   
   
    inst = random.randint(1,10)
    
    llegada = random.expovariate(1.0/10)
    print('proceso %s tiene que esperar %d'% (nombre, llegada))
    yield env.timeout(llegada)

    memoriaPedida = random.randint(1,10)
    print('%s pidio %d de RAM'% (nombre, memoriaPedida))
    yield env.timeout(memoriaPedida)
    globales.rtot=globales.rtot+memoriaPedida
    flag=True
    while flag:
        if (100-ram.level)>=memoriaPedida:
            print ('%s Entro a ready' % nombre)
            yield ram.get(memoriaPedida)
            flag = False
        else:
            print ('%s Espera a ready' % nombre)
            yield env.timeout(memoriaPedida)

    while (inst!=0):
        print ('%s esta en ready' %nombre)    
        with cpu.request() as turno:
            yield turno
            print ('%s Se esta PROCESANDO' % nombre)
            if (inst<0):
                inst=0
            yield env.timeout(inst)

            if (inst<=0):
                break
            else:
                inst=inst-10
                destino=random.randint(1,2)
                if (destino==1):
                    io=random.randint(1,10)
                    yield env.timeout(io)
                else:
                    print ('%s Regreso a READY' % nombre)
                    
                    
            
    print('%s libero %d de RAM'% (nombre, memoriaPedida))
    yield ram.put(memoriaPedida)
        

env = simpy.Environment() #ambiente de simulación
ram = simpy.Container(env, init=10, capacity = 100)
cpu = simpy.Resource(env, capacity=1)


for i in range(50):
    env.process(x(' %d'%i,env, ram, cpu))

   
env.run(until = 200)
print(globales.rtot)

tiempo_final = time()

tiempo_ejecucion = tiempo_final - tiempo_inicial

print 'El tiempo de ejecucion fue:',tiempo_ejecucion #En segundos



