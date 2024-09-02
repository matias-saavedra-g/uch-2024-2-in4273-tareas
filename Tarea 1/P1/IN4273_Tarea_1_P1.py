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
## Pregunta 1
# Actividad	Letra asignada	Estaciones	Tiempo
# Escanear la credencial	A	10	2 min/persona
# Revision de seguridad	B	12	5 min/persona
# Asignacion de ruta	C	14	4 min/persona

# Se crean las actividades
actividad_A = Actividad("A", 10, 2)
actividad_B = Actividad("B", 12, 5)
actividad_C = Actividad("C", 14, 4)

# Se crea el sistema
sistema = Sistema([actividad_A, actividad_B, actividad_C])

### --------------------------------------------------------------------------------------------------------------- ###
## Pregunta 1.2
# Se calculan las capacidades de cada actividad, el cuello de botella del sistema, y la capacidad maxima del sistema
print("\nPregunta 1.2.")
string_respuestas += "# Pregunta 1.2.\n"
sistema.calcular_cuello_botella()

# Las muestra
print(sistema)
string_respuestas += str(sistema) + "\n"
print("\n---")
string_respuestas += "\n---\n\n"
for actividad in sistema.actividades:
    print(actividad)
    string_respuestas += str(actividad) + "\n"
    print(f"Capacidad: {actividad.capacidad} personas/minuto")
    string_respuestas += f"Capacidad: {actividad.capacidad} personas/minuto\n"
    print(f"{'Cuello de botella' if actividad.cuello_botella else ''}")
    string_respuestas += f"{'Cuello de botella' if actividad.cuello_botella else ''}\n"
    print("\n---")
    string_respuestas += "\n---\n\n"
    
print(f"Capacidad del sistema: {sistema.capacidad} personas/minuto")
string_respuestas += f"Capacidad del sistema: {sistema.capacidad} personas/minuto\n"
print("\n---")
string_respuestas += "\n---\n\n"

# Calcula la utilizacion de cada etapa considerando la tasa de entrada como el cuello de botella
sistema.tasa_entrada = sistema.capacidad
sistema.calcular_utilizacion()
for actividad in sistema.actividades:
    print(f"Utilizacion de la actividad {actividad.letra}: {actividad.utilizacion * 100:.2f}%")
    string_respuestas += f"Utilizacion de la actividad {actividad.letra}: {actividad.utilizacion * 100:.2f}%\n"
    print("\n---")
    string_respuestas += "\n---\n\n"

### --------------------------------------------------------------------------------------------------------------- ###
## Pregunta 1.3
# Calcular el inventario promedio de la ley de little, considerando la tasa de procesamiento como el tiempo de flujo y el tiempo promedio como 8 horas
# Usando la funcion calcular_little
print("Pregunta 1.3. Parte 1")
string_respuestas += "# Pregunta 1.3.\n"
string_respuestas += "## Pregunta 1.3. Parte 1\n"
L = calcular_little(-1, 8*60, sistema.capacidad)
print(f"Inventario promedio: {calcular_inventario_promedio(L, 8*60, sistema.capacidad)}")
string_respuestas += f"Inventario promedio: {calcular_inventario_promedio(L, 8*60, sistema.capacidad)}\n"
print("\n---")
string_respuestas += "\n---\n\n"

# Mostramos la cantidad de gente total que ingreso durante 8 horas en base al inventario promedio integrado sobre el tiempo
print(f"Cantidad de gente total que ingreso durante 8 horas: {L * 8 * 60:.0f}")
string_respuestas += f"Cantidad de gente total que ingreso durante 8 horas: {L * 8 * 60:.0f}\n"
print("\n---")
string_respuestas += "\n---\n\n"

# Aumentamos la tasa de entrada de 2.4 a 2.4*1.5 en un sistema_mod y vemos como cambia la utilizacion de cada actividad
print("Pregunta 1.3. Parte 2")
string_respuestas += "## Pregunta 1.3. Parte 2\n"
sistema2 = Sistema([actividad_A, actividad_B, actividad_C])
sistema2.calcular_cuello_botella()
sistema2.tasa_entrada = 2.4*1.5
sistema2.calcular_utilizacion()

for actividad in sistema.actividades:
    print(f"Utilizacion de la actividad {actividad.letra}: {actividad.utilizacion * 100:.2f}%")
    string_respuestas += f"Utilizacion de la actividad {actividad.letra}: {actividad.utilizacion * 100:.2f}%\n"
    print("\n---")
    string_respuestas += "\n---\n\n"
    
# Vemos la acumulacion de inventario en un grafico
# Se crea un rango de tiempo de 8 horas
tiempo = np.linspace(0, 8*60, 1000)

# Se define la pendiente del inventario como (tasa de entrada - tasa de salida)/(tasa de salida)
pendiente = (sistema.tasa_entrada - sistema.capacidad) / sistema.capacidad
pendiente2 = (sistema2.tasa_entrada - sistema2.capacidad) / sistema2.capacidad

# Se calcula el inventario en funcion del tiempo de manera lineal f = m*x + b
inventario = pendiente*tiempo
inventario2 = pendiente2*tiempo

# Se grafican ambos sistemas y se muestran las tasas de entrada y salida en un recuadro
plt.plot(tiempo, inventario)
plt.plot(tiempo, inventario2)
plt.axhline(0, color="black", linestyle="--")
plt.axvline(0, color="black", linestyle="--")
plt.xlabel("Tiempo (minutos)")
plt.ylabel("Inventario")
plt.legend(["Sistema 1", "Sistema 2"])
plt.title("Comparacion de acumulacion de inventario en sistemas 1 y 2")
plt.grid()
# Guarda el grafico
plt.savefig("IN4273_Tarea_1_P1_Sys1o2.png")
plt.show()

# Necesitamos redefinir el sistema3 para aumentar la capacidad de la acctividad B a 3.6 personas/minuto y la actividad C a 3.6 personas/minuto
# La cantidad de estaciones debe ser entera, por lo que se redondea hacia arriba
# Se crean actividades B2 y C2
print("Pregunta 1.3. Parte 3")
string_respuestas += "## Pregunta 1.3. Parte 3\n"
actividad_B2 = Actividad("B2", ceil(5*3.6), 5)
actividad_C2 = Actividad("C2", ceil(4*3.6), 4)

# Se crea el sistema 3
sistema3 = Sistema([actividad_A, actividad_B2, actividad_C2])
sistema3.calcular_cuello_botella()
sistema3.tasa_entrada = 2.4*1.5
sistema3.calcular_utilizacion()

print(sistema3)
string_respuestas += str(sistema3) + "\n"
print("\n---")
string_respuestas += "\n---\n\n"
for actividad in sistema3.actividades:
    print(actividad)
    string_respuestas += str(actividad) + "\n"
    print(f"Capacidad: {actividad.capacidad} personas/minuto")
    string_respuestas += f"Capacidad: {actividad.capacidad} personas/minuto\n"
    print(f"{'Cuello de botella' if actividad.cuello_botella else ''}")
    string_respuestas += f"{'Cuello de botella' if actividad.cuello_botella else ''}\n"
    print("\n---")
    string_respuestas += "\n---\n\n"
    
# Se muestra la utilizacion de cada actividad
for actividad in sistema3.actividades:
    print(f"Utilizacion de la actividad {actividad.letra}: {actividad.utilizacion * 100:.2f}%")
    string_respuestas += f"Utilizacion de la actividad {actividad.letra}: {actividad.utilizacion * 100:.2f}%\n"
    print("\n---")
    string_respuestas += "\n---\n\n"
    
# Se grafica la acumulacion de inventario
# Se define la pendiente del inventario como (tasa de entrada - tasa de salida)/(tasa de salida)
pendiente3 = (sistema3.tasa_entrada - sistema3.capacidad) / sistema3.capacidad

# Se calcula el inventario en funcion del tiempo
inventario3 = pendiente3*tiempo

# Inventario debe ser mayor a 0
inventario3[inventario3 < 0] = 0

# Se grafica el sistema 3
plt.plot(tiempo, inventario3)
plt.axhline(0, color="black", linestyle="--")
plt.axvline(0, color="black", linestyle="--")
plt.xlabel("Tiempo (minutos)")
plt.ylabel("Inventario")
plt.legend(["Sistema 3"])
plt.title("Acumulacion de inventario en sistemas 3")
plt.grid()
# Guarda el grafico
plt.savefig("IN4273_Tarea_1_P1_Sys3.png")
plt.show()

### --------------------------------------------------------------------------------------------------------------- ###
## Pregunta 1.4
# Ahora la actividad A tiene una eficiencia del 95%, la B del 90%, y la C del 70%
# Las nuevas capacidades son capacidad * eficiencia
print("Pregunta 1.4.")
string_respuestas += "# Pregunta 1.4.\n"
actividad_A.capacidad *= 0.95
actividad_B.capacidad *= 0.90
actividad_C.capacidad *= 0.70

# Muestra las capacidades de cada actividad
for actividad in sistema.actividades:
    print(actividad)
    string_respuestas += str(actividad) + "\n"
    print(f"Capacidad: {actividad.capacidad} personas/minuto")
    string_respuestas += f"Capacidad: {actividad.capacidad} personas/minuto\n"
    print("\n---")
    string_respuestas += "\n---\n\n"
    
### --------------------------------------------------------------------------------------------------------------- ###
## Pregunta 1.5
# Se va a calcular el costo/beneficio de aumentar la eficiencia de B al 100% que cuesta 40 USD/hora VS incrementar la cantidad de estaciones de B que es 15 USD/hora por estacion

# Se calcula el costo de aumentar la eficiencia de B al 100%
costo_eficiencia = 40
costo_estacion = 15

# Se calcula el beneficio de aumentar la eficiencia de B al 100%
beneficio_eficiencia = (actividad_B.capacidad * 0.90 - actividad_B.capacidad) * 60 * costo_eficiencia

# Se calcula el beneficio de aumentar la cantidad de estaciones de B
beneficio_estacion = (actividad_B.capacidad * 0.90 - actividad_B.capacidad) * 60 * costo_estacion

# Se muestra el costo/beneficio de aumentar la eficiencia de B al 100%
print("Pregunta 1.5.")
string_respuestas += "# Pregunta 1.5.\n"
print(f"Beneficio de aumentar la eficiencia de B al 100%: {beneficio_eficiencia} USD")
string_respuestas += f"Beneficio de aumentar la eficiencia de B al 100%: {beneficio_eficiencia} USD\n"
print(f"Beneficio de aumentar la cantidad de estaciones de B: {beneficio_estacion} USD")
string_respuestas += f"Beneficio de aumentar la cantidad de estaciones de B: {beneficio_estacion} USD\n"
print(f"Costo de aumentar la eficiencia de B al 100%: {costo_eficiencia} USD")
string_respuestas += f"Costo de aumentar la eficiencia de B al 100%: {costo_eficiencia} USD\n"
print(f"Costo de aumentar la cantidad de estaciones de B: {costo_estacion} USD")
string_respuestas += f"Costo de aumentar la cantidad de estaciones de B: {costo_estacion} USD\n"
print("\n---")
string_respuestas += "\n---\n\n"

# Se calcula el costo/beneficio de aumentar la eficiencia de B al 100% VS incrementar la cantidad de estaciones de B
if beneficio_eficiencia - costo_eficiencia > beneficio_estacion - costo_estacion:
    print("Es mas conveniente aumentar la eficiencia de B al 100%")
    string_respuestas += "Es mas conveniente aumentar la eficiencia de B al 100%\n"
else:
    print("Es mas conveniente aumentar la cantidad de estaciones de B")
    string_respuestas += "Es mas conveniente aumentar la cantidad de estaciones de B\n"
    
print("\n---")
string_respuestas += "\n---\n\n"
    
### --------------------------------------------------------------------------------------------------------------- ###
## Escribe el string de respuestas en un archivo
with open("IN4273_Tarea_1_P1_Ans.md", "w") as file:
    file.write(string_respuestas)
    
### --------------------------------------------------------------------------------------------------------------- ###

if __name__ == "__main__":
    pass