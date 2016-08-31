import simpy
import random

#Algortimos y Estructura de Datos
#Seccion 20
#Autor: Josue Jacobs 15041
#Autor: Marcel Velasquez 15534


def computadora(env, tiempo, mens, ram, cantMemoria, nIns, velocidad):

    global t
    global tTotal

    #New
    yield env.timeout(tiempo)
    print ('%s se necesita esta cantidad %d de RAM' % ( mens, cantMemoria)) #muestra cuanto se necesita de memoria RAM
    tRea = env.now

    #Ready
    yield ram.get(cantMemoria) # se obtiena la memoria ram
    print ('%s. se puede utilizar la cantidad solicitada de RAM, %d  ' % ( mens, cantMemoria))

    instTerm = 0

    while instTerm < nIns:

        with cpu.request() as r:
            yield r

            if (nIns - instTerm)>= velocidad:
                real=velocidad
            else:
                real=(nIns - instTerm)

            print ('%s El CPU realizara %d instrucciones' % (mens, real))
            yield env.timeout(real/velocidad)

            instTerm = instTerm + real
            print ('%s El CPU ha realizado %d de %d instrucciones' % (mens, instTerm, nIns))

        op = random.randint(1,2)

        if (op == 1) and (instTerm<nIns):
            #wait
            with wait.request() as r1:
                yield r1
                yield env.timeout(1)
                print ('%s. Se ha echo operaciones de entrada y salida' % ( mens))

    #terminated
    yield ram.put(cantMemoria)
    print ('%s regresa  %d de cantidad de RAM' % (mens, cantMemoria))
    tTotal += (env.now - tRea)
    t.append(env.now - tRea)

           
           
mRam = 100
tTotal = 0.0
t = []
numProces = 50
velocidad = 3.0    

         

    
env = simpy.Environment()
ram = simpy.Container(env, capacity=mRam, init=mRam)
cpu = simpy.Resource(env, capacity = 2)
wait = simpy.Resource(env, capacity =2)

nInt = 1
random.seed(2411)

for i in range(numProces):
    tiempo = random.expovariate(1.0 /nInt)
    nIns = random.randint(1,10)
    cantMemoria = random.randint(1,10) 
    env.process(computadora(env, tiempo, 'Proceso Numero %d' %i, ram, cantMemoria, nIns, velocidad))

env.run()

