import simpy
import random

#Algortimos y Estructura de Datos
#Seccion 20
#Autor: Josue Jacobs 15041
#Autor: Marcel Velasquez 15534


def computadora(env, tiempo, mens, ram, cantMemoria, numInstruc, velocidad):

    global t
    global tTotal

    #Poceso New 
    yield env.timeout(tiempo)
    #Es la cantidad de ram que necesita el proceso para realizarlo
    print ('%s: se necesita esta cantidad de RAM: %d para realizar el proceso' % ( mens, cantMemoria)) #muestra cuanto se necesita de memoria RAM
    tRea = env.now

    #Proceso Ready 
    yield ram.get(cantMemoria) # se obtiena la memoria ram
    print ('%s: se puede utilizar la cantidad solicitada de RAM: %d  ' % ( mens, cantMemoria))

    #Variable en donde se guarda la cantidad total de instrucciones terminadas
    instTerm = 0

    #Ciclo para poder hacer la cantidad de instrucciones correctas
    while instTerm < numInstruc:

        with cpu.request() as r:
            yield r

            #comparacion para no tener un numero de instrucciones negativo 
            if (numInstruc - instTerm)>= velocidad:
                real=velocidad
            else:
                real=(numInstruc - instTerm)
            #Mensaje de cuantas instrucciones tiene que hacer y cuantas ha realizado
            print ('%s: El CPU realizara esta cantidad de instrucciones: %d' % (mens, real))
            yield env.timeout(real/velocidad)

            instTerm = instTerm + real
            print ('%s: El CPU ha realizado %d de %d instrucciones' % (mens, instTerm, numInstruc))

        #Random en donde se elige si se realiza un Waiting o un ready
        op = random.randint(1,2)

        if (op == 1) and (instTerm<numInstruc):
            #wait
            with wait.request() as r1:
                yield r1
                yield env.timeout(1)
                print ('%s: Se ha echo operaciones de entrada y salida' % ( mens))

    #Proceso Terminated
    yield ram.put(cantMemoria)
    print ('%s: Se regresa del CPU esta cantidad de RAM: %d' % (mens, cantMemoria))
    tTotal += (env.now - tRea)
    t.append(env.now - tRea)

           
#valores iniciales para poder realizar los procesos        
mRam = 100
tTotal = 0.0
t = []
numProces = 50
velocidad = 3.0    

#Instrucciones para poder realizar la simulacion    
env = simpy.Environment()
ram = simpy.Container(env, capacity=mRam, init=mRam)
cpu = simpy.Resource(env, capacity = 2)
wait = simpy.Resource(env, capacity =2)

numInt = 1
random.seed(2411)

for i in range(numProces):
    tiempo = random.expovariate(1.0 /numInt)
    numInstruc = random.randint(1,10)
    cantMemoria = random.randint(1,10) 
    env.process(computadora(env, tiempo, 'Proceso Numero %d' %i, ram, cantMemoria, numInstruc, velocidad))

#Se realiza el proceso 
env.run()

suma =0
promedio = 0

#Promedio
promedio = (tTotal/numProces)
print ('El promedio de los preocesos es: %f segundos'%(promedio))
#Desviacion estandar
for cont in t:
    suma = suma +((cont-promedio)**2)
desv = (suma/(numProces))**5
print(' La desviacion estandar de los tiempos en los procesos es: %f segundos' %(desv))


