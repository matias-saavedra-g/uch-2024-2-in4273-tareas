### Este script se encarga de realizar la tarea 1 de la asignatura IN4273
## El encoding del archivo era utf-8, pero se quitaron todos los caracteres especiales para evitar problemas de compatibilidad

## Importacion de librerias
import matplotlib.pyplot as plt
import numpy as np
from math import ceil
## Definicion de clases
# Se crea una clase para representar el sistema y sus actividades: incluyendo el tiempo de actividad, la cantidad de estaciones que pueden funcionar en paralelo, su letra asignada, la capacidad de la actividad, la utilizacion, el cuello de botella (boolean).

class Actividad:
    def __init__(self, letra, estaciones, tiempo):
        self.letra = letra
        self.estaciones = estaciones
        self.tiempo = tiempo
        self.capacidad = 0
        self.utilizacion = 0
        self.cuello_botella = False

    def __str__(self):
        return f"Actividad {self.letra} con {self.estaciones} estaciones y tiempo de {self.tiempo} min/persona"
    
    def calcular_capacidad(self):
        self.capacidad = self.estaciones / self.tiempo
    
# Se crea la clase Sistema que contiene la tasa de entrada al sistema, la actividad cuello de botella, la capacidad del sistema, el tiempo de flujo, el tiempo de ciclo, y el tiempo de produccion de las primeras N unidades

class Sistema:
    def __init__(self, actividades, tasa_entrada=0):
        self.tasa_entrada = tasa_entrada
        self.actividades = actividades
        self.actividad_cuello_botella = None
        self.capacidad = 0
        self.tiempo_flujo = 0
        self.tiempo_ciclo = 0
        self.tiempo_produccion = 0

    def __str__(self):
        return f"Sistema con tasa de entrada de {self.tasa_entrada} personas/minuto"

    def calcular_cuello_botella(self):
        for actividad in self.actividades:
            actividad.calcular_capacidad()
        self.actividad_cuello_botella = min(self.actividades, key=lambda x: x.capacidad)
        self.actividad_cuello_botella.cuello_botella = True
        self.capacidad = self.actividad_cuello_botella.capacidad

    def calcular_tiempos(self, N):
        self.tiempo_flujo = sum([actividad.tiempo for actividad in self.actividades])
        self.tiempo_ciclo = 1 / self.tiempo_flujo
        self.tiempo_produccion = (N - 1)/self.capacidad * self.tiempo_flujo
        
    def calcular_utilizacion(self):
        for actividad in self.actividades:
            actividad.utilizacion = min(self.capacidad,self.tasa_entrada) / actividad.capacidad
        
# Se crea una funcion para calcular la ley de Little con 2 de los 3 parametros, marcando con -1 el parametro que no se tiene.
def calcular_little(L, W, lam):
    if L == -1:
        return W * lam
    elif W == -1:
        return L / lam
    else:
        return L / W
    
# Se crea una funcion para calcular el inventario promedio con respecto a la acumulacion de inventario en el sistema.
def calcular_inventario_promedio(L, W, lam):
    return calcular_little(L, W, lam) * calcular_little(L, W, lam) / lam

### --------------------------------------------------------------------------------------------------------------- ###
## Iniciacion del string que se va a guardar en un archivo de respuestas
string_respuestas = ""

### --------------------------------------------------------------------------------------------------------------- ###
## Pregunta 2
# Actividad	Letra asignada	Estaciones	Tiempo
# Inscripcion y revision de papeles	A	10	1.5 min/persona
# Vacunacion	B	10	2 min/persona
# Entrega de documentos	C	10	0.5 min/persona

# Se crean las actividades
actividad_A = Actividad("A", 10, 1.5)
actividad_B = Actividad("B", 10, 2)
actividad_C = Actividad("C", 10, 0.5)

# Se crean actividades que solo operan al 60% de su capacidad
actividad_A_60 = Actividad("A", 6, 1.5)
actividad_B_60 = Actividad("B", 6, 2)
actividad_C_60 = Actividad("C", 6, 0.5)

# Se crea el sistema de full capacidad
sistema_full = Sistema([actividad_A, actividad_B, actividad_C])

# Se crea un sistema que opera a 60% de su capacidad
sistema_60 = Sistema([actividad_A_60, actividad_B_60, actividad_C_60])

### --------------------------------------------------------------------------------------------------------------- ###
## Pregunta 2.1
# Se calculan los tiempos del sistema_full
sistema_full.calcular_cuello_botella()
sistema_full.calcular_utilizacion()

print("Pregunta 2.1")
string_respuestas += f"# Pregunta 2.1\n"
print("\n---")
string_respuestas += "\n---\n"

print(sistema_full)
string_respuestas += f"{sistema_full}\n"
print("\n---")
string_respuestas += "\n---\n"

for actividad in sistema_full.actividades:
    print(actividad)
    string_respuestas += f"{actividad}\n"
    print(f"Capacidad: {actividad.capacidad} personas/minuto")
    string_respuestas += f"Capacidad: {actividad.capacidad} personas/minuto\n"
    print(f"{'Cuello de botella' if actividad.cuello_botella else ''}")
    string_respuestas += f"{'Cuello de botella' if actividad.cuello_botella else ''}\n"
    print("\n---")
    string_respuestas += "\n---\n"
    
print(f"Capacidad del sistema: {sistema_full.capacidad} personas/minuto")
string_respuestas += f"Capacidad del sistema: {sistema_full.capacidad} personas/minuto\n"
print("\n---")
string_respuestas += "\n---\n"

### --------------------------------------------------------------------------------------------------------------- ###

## Pregunta 2.2
print("Pregunta 2.2")
string_respuestas += f"# Pregunta 2.2\n"
print("\n---")
string_respuestas += "\n---\n"

# El sistema opera desde las 8:00 AM hasta las 16:00 PM

# Condiciones de la tasa de entrada
# Durante las primeras 2 horas la tasa de entrada al sistema es de 50 personas/hora
# Durante las siguientes 4 horas la tasa de entrada al sistema es de 180 personas/hora
# Durante las ultimas 2 horas la tasa de entrada al sistema es nula

# Condiciones de las actividades
# Durante las primeras 3 horas el sistema opera a 60% de su capacidad
# Durante las ultimas 5 horas el sistema opera a full capacidad

# Calculamos los parametros de ambos sistemas en torno a las combinaciones de tasa de entrada y capacidad de las actividades

# Combinaciones
# sistema1: 50 personas/hora y 60% de capacidad
# sistema2: 180 personas/hora y 60% de capacidad
# sistema3: 180 personas/hora y full capacidad
# sistema4: 0 personas/hora y full capacidad

# Se define el sistema 1 de 8:00 AM a 10:00 AM
sistema1 = Sistema([actividad_A_60, actividad_B_60, actividad_C_60], 50/60)
sistema1.calcular_cuello_botella()
sistema1.calcular_utilizacion()

# Se define el sistema 2 de 10:00 AM a 11:00 AM
sistema2 = Sistema([actividad_A_60, actividad_B_60, actividad_C_60], 180/60)
sistema2.calcular_cuello_botella()
sistema2.calcular_utilizacion()

# Se define el sistema 3 de 11:00 AM a 14:00 PM
sistema3 = Sistema([actividad_A, actividad_B, actividad_C], 180/60)
sistema3.calcular_cuello_botella()
sistema3.calcular_utilizacion()

# Se define el sistema 4 de 14:00 PM a 16:00 PM
sistema4 = Sistema([actividad_A, actividad_B, actividad_C], 0)
sistema4.calcular_cuello_botella()
sistema4.calcular_utilizacion()

# Se imprimen los resultados
dia_laboral = [sistema1, sistema2, sistema3, sistema4]

for sistema in dia_laboral:
    print(f"Sistema N-{dia_laboral.index(sistema)+1}")
    string_respuestas += f"Sistema N-{dia_laboral.index(sistema)+1}\n"
    print(sistema)
    string_respuestas += f"{sistema}\n"
    print("\n---")
    string_respuestas += "\n---\n"
    for actividad in sistema.actividades:
        print(actividad)
        string_respuestas += f"{actividad}\n"
        print(f"Capacidad: {actividad.capacidad} personas/minuto")
        string_respuestas += f"Capacidad: {actividad.capacidad} personas/minuto\n"
        print(f"{'Cuello de botella' if actividad.cuello_botella else ''}")
        string_respuestas += f"{'Cuello de botella' if actividad.cuello_botella else ''}\n"
        print("\n---")
        string_respuestas += "\n---\n"
    print(f"Capacidad del sistema: {sistema.capacidad} personas/minuto")
    string_respuestas += f"Capacidad del sistema: {sistema.capacidad} personas/minuto\n"
    print("\n---")
    string_respuestas += "\n---\n"
    
# Se grafica la acumulacion de inventario durante todo el dia

# Se definen cuatro arrays de tiempo para los 4 itinerarios respectivos a los sistemas
t1 = np.arange(0, 120, 1)
t2 = np.arange(120, 180, 1)
t3 = np.arange(180, 420, 1)
t4 = np.arange(420, 600, 1)

# Se define la pendiente de cada inventario como (tasa de entrada - tasa de salida)/(tasa de salida)
m1 = (sistema1.tasa_entrada - sistema1.capacidad)/sistema1.capacidad
m2 = (sistema2.tasa_entrada - sistema2.capacidad)/sistema2.capacidad
m3 = (sistema3.tasa_entrada - sistema3.capacidad)/sistema3.capacidad
m4 = (sistema4.tasa_entrada - sistema4.capacidad)/sistema4.capacidad

# Se calcula el inventario en funcion del tiempo
inv1 = m1 * t1
inv2 = m2 * t2 + inv1[-1]
inv3 = m3 * t3 + inv2[-1]
inv4 = m4 * t4 + inv3[-1]

# Se concatenan los tiempos y los inventarios
t = np.concatenate((t1, t2, t3, t4))
inv = np.concatenate((inv1, inv2, inv3, inv4))

# Inventario debe ser mayor a 0
inv[inv < 0] = 0

# Se grafica el inventario
plt.plot(t, inv, color='red', linewidth=2)
# Agrega un marcador para las 8:00 AM, 10:00 AM, 11:00 AM, 14:00 PM y 16:00 PM
plt.axvline(x=120, color='black', linestyle='--', linewidth=0.5)
plt.axvline(x=180, color='black', linestyle='--', linewidth=0.5)
plt.axvline(x=420, color='black', linestyle='--', linewidth=0.5)
plt.title("Inventario acumulado durante el dia normal")
plt.xlabel("Minuto")
plt.ylabel("Inventario acumulado")
plt.grid()
plt.savefig("IN4273_Tarea_1_P2_day.png")
plt.show()

# Se calcula el tiempo promedio de espera en el sistema usando ley de Little
wait1 = max(0,calcular_little(np.mean(inv1), -1, sistema1.capacidad))
wait2 = max(0,calcular_little(np.mean(inv2), -1, sistema2.capacidad))
wait3 = max(0,calcular_little(np.mean(inv3), -1, sistema3.capacidad))
wait4 = max(0,calcular_little(np.mean(inv4), -1, sistema4.capacidad))

waiting_times = [wait1, wait2, wait3, wait4]

for wait in waiting_times:
    print(f"Tiempo promedio de espera en el sistema {waiting_times.index(wait)+1}: {wait:.0f} minutos")
    string_respuestas += f"Tiempo promedio de espera en el sistema {waiting_times.index(wait)+1}: {wait:.0f} minutos\n"
    print("\n---")
    string_respuestas += "\n---\n"

### --------------------------------------------------------------------------------------------------------------- ###
## Pregunta 2.3
# Veremos costos asociados y calcular cuanto cuesta operar en base a la modalidad propuesta
# Costo por actividad B: 120 USD/hora
# Costo por actividad A, C: 0 USD/hora
# Costo por espera: 1 USD/hora
# Por otro lado, el tiempo promedio de atencion se ve incrementado en 1 minuto, sumandole a la actividad B 1 minuto de tiempo de atencion

print("Pregunta 2.3")
string_respuestas += f"# Pregunta 2.3\n"
print("\n---")
string_respuestas += "\n---\n"

# Define costos en USD/minutos
costo_B = 120/60
costo_A = 0
costo_C = 0
costo_espera = 1/60

# Define actividad B2 con 1 minuto adicional
actividad_B2 = Actividad("B", 10, 3)

# Define actividad B2_60
actividad_B2_60 = Actividad("B", 6, 3)

# Define sistema 2.1, 2.2, 2.3, 2.4 con el mismo dia laboral, pero considerando la nueva espera de la actividad B2
# Combinaciones
# sistema1: 50 personas/hora y 60% de capacidad
# sistema2: 180 personas/hora y 60% de capacidad
# sistema3: 180 personas/hora y full capacidad
# sistema4: 0 personas/hora y full capacidad

# Se define el sistema 1 de 8:00 AM a 10:00 AM
sistema2_1 = Sistema([actividad_A_60, actividad_B2_60, actividad_C_60], 50/60)
sistema2_1.calcular_cuello_botella()
sistema2_1.calcular_utilizacion()

# Se define el sistema 2 de 10:00 AM a 11:00 AM
sistema2_2 = Sistema([actividad_A_60, actividad_B2_60, actividad_C_60], 180/60)
sistema2_2.calcular_cuello_botella()
sistema2_2.calcular_utilizacion()

# Se define el sistema 3 de 11:00 AM a 14:00 PM
sistema2_3 = Sistema([actividad_A, actividad_B2, actividad_C], 180/60)
sistema2_3.calcular_cuello_botella()
sistema2_3.calcular_utilizacion()

# Se define el sistema 4 de 14:00 PM a 16:00 PM
sistema2_4 = Sistema([actividad_A, actividad_B2, actividad_C], 0)
sistema2_4.calcular_cuello_botella()
sistema2_4.calcular_utilizacion()

# Se imprimen los resultados
dia_laboral_2 = [sistema2_1, sistema2_2, sistema2_3, sistema2_4]

for sistema in dia_laboral_2:
    print(f"Sistema N-{dia_laboral_2.index(sistema)+1}")
    string_respuestas += f"Sistema N-{dia_laboral_2.index(sistema)+1}\n"
    print(sistema)
    string_respuestas += f"{sistema}\n"
    print("\n---")
    string_respuestas += "\n---\n"
    for actividad in sistema.actividades:
        print(actividad)
        string_respuestas += f"{actividad}\n"
        print(f"Capacidad: {actividad.capacidad} personas/minuto")
        string_respuestas += f"Capacidad: {actividad.capacidad} personas/minuto\n"
        print(f"{'Cuello de botella' if actividad.cuello_botella else ''}")
        string_respuestas += f"{'Cuello de botella' if actividad.cuello_botella else ''}\n"
        print("\n---")
        string_respuestas += "\n---\n"
    print(f"Capacidad del sistema: {sistema.capacidad} personas/minuto")
    string_respuestas += f"Capacidad del sistema: {sistema.capacidad} personas/minuto\n"
    print("\n---")
    string_respuestas += "\n---\n"
    
# Se grafica la acumulacion de inventario durante todo el dia
# Se define la pendiente de cada inventario como (tasa de entrada - tasa de salida)/(tasa de salida)
m2_1 = (sistema2_1.tasa_entrada - sistema2_1.capacidad)/sistema2_1.capacidad
m2_2 = (sistema2_2.tasa_entrada - sistema2_2.capacidad)/sistema2_2.capacidad
m2_3 = (sistema2_3.tasa_entrada - sistema2_3.capacidad)/sistema2_3.capacidad
m2_4 = (sistema2_4.tasa_entrada - sistema2_4.capacidad)/sistema2_4.capacidad

# Se calcula el inventario en funcion del tiempo
inv2_1 = m2_1 * t1
inv2_2 = m2_2 * t2 + inv2_1[-1]
inv2_3 = m2_3 * t3 + inv2_2[-1]
inv2_4 = m2_4 * t4 + inv2_3[-1]

# Se concatenan los tiempos y los inventarios
t = np.concatenate((t1, t2, t3, t4))
inv = np.concatenate((inv2_1, inv2_2, inv2_3, inv2_4))

# Inventario debe ser mayor a 0
inv[inv < 0] = 0

# Se grafica el inventario
plt.plot(t, inv, color='red', linewidth=2)
# Agrega un marcador para las 8:00 AM, 10:00 AM, 11:00 AM, 14:00 PM y 16:00 PM
plt.axvline(x=120, color='black', linestyle='--', linewidth=0.5)
plt.axvline(x=180, color='black', linestyle='--', linewidth=0.5)
plt.axvline(x=420, color='black', linestyle='--', linewidth=0.5)
plt.title("Inventario acumulado durante el dia con desparasitacion")
plt.xlabel("Minuto")
plt.ylabel("Inventario acumulado")
plt.grid()
plt.savefig("IN4273_Tarea_1_P2_day2.png")
plt.show()

# Se calculan los tiempos de espera
wait2_1 = max(0,calcular_little(np.mean(inv2_1), -1, sistema2_1.capacidad))
wait2_2 = max(0,calcular_little(np.mean(inv2_2), -1, sistema2_2.capacidad))
wait2_3 = max(0,calcular_little(np.mean(inv2_3), -1, sistema2_3.capacidad))
wait2_4 = max(0,calcular_little(np.mean(inv2_4), -1, sistema2_4.capacidad))

waiting_times_2 = [wait2_1, wait2_2, wait2_3, wait2_4]

for wait in waiting_times_2:
    print(f"Tiempo promedio de espera en el sistema {waiting_times_2.index(wait)+1}: {wait:.0f} minutos")
    string_respuestas += f"Tiempo promedio de espera en el sistema {waiting_times_2.index(wait)+1}: {wait:.0f} minutos\n"
    print("\n---")
    string_respuestas += "\n---\n"
    
# Se calculan los costos asociados este dia laboral 2
# Se multiplica el costo de B2 por horas trabajadas y estaciones de trabajo: 120 USD/hora * 6 estaciones * 3 horas + 120 USD/hora * 10 estaciones * 5 horas
costo_fijo_B2 = 120 * 6 * 3 + 120 * 10 * 5

# Se multiplica el tiempo de espera por el costo de espera
costo_fijo_espera = sum(waiting_times_2) * costo_espera

# Se suman los costos
costos_fijos = costo_fijo_B2 + costo_fijo_espera

# Se imprime el costo total
print(f"Costo total del dia: {costos_fijos:.2f} USD")
string_respuestas += f"Costo total del dia: {costos_fijos:.2f} USD\n"
print("\n---")
string_respuestas += "\n---\n"

### --------------------------------------------------------------------------------------------------------------- ###

## Escribe el string de respuestas en un archivo
with open("IN4273_Tarea_1_P2_Ans.md", "w") as file:
    file.write(string_respuestas)
    
### --------------------------------------------------------------------------------------------------------------- ###

if __name__ == "__main__":
    pass