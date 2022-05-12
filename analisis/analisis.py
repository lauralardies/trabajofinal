import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def leer_csv(archivo, seleccion, traduccion):

    try:
        f = open(archivo)

    except FileNotFoundError:
        print("El fichero no existe.")

    else:
        lineas = f.readlines()
        f.close()

        linea = lineas[0].strip()
        columnas = linea.split(",")
        
        datos = []

        for linea in lineas[1:]:
            dato = {}
            linea = linea.strip()
            campos = linea.split(",")
            for i in range(len(columnas)):
                if columnas[i] in seleccion:
                    dato[traduccion[columnas[i]]] = campos[i]
            datos.append(dato)

        return datos
    
def seguimiento_online(pacientes):

    online = {"Seguidor Online" : 0, "Comparte LinkedIn" :0, "Comparte Twitter" : 0, "Comparte Facebook" : 0}

    for paciente in pacientes:
        if paciente["Seguidor Online"] != "0":
            online["Seguidor Online"] = online["Seguidor Online"] + 1
        if paciente["Comparte LinkedIn"] != "0":
            online["Comparte LinkedIn"] = online["Comparte LinkedIn"] + 1
        if paciente["Comparte Twitter"] != "0":
            online["Comparte Twitter"] = online["Comparte Twitter"] + 1
        if paciente["Comparte Facebook"] != "0":
            online["Comparte Facebook"] = online["Comparte Facebook"] + 1

    return online

def tipos_ciudades(pacientes):

    ciudades = {} # Diccionario de las ciudades con el número de pacientes que vive en cada una de ellas.

    for paciente in pacientes:
        if paciente["Tipo Ciudad"] not in ciudades:
                ciudades[paciente["Tipo Ciudad"]] = 1
        else:
            ciudades[paciente["Tipo Ciudad"]] = ciudades[paciente["Tipo Ciudad"]] + 1

    del ciudades[""] # Eliminamos aquellos casos en los que no esté especificada la ciudad del paciente.

    return ciudades

def tipo_trabajo(pacientes):

    trabajo = {} # Diccionario de los trabajos con el número de pacientes que se dedican a ello.

    for paciente in pacientes:
        if paciente["Categoria Empleado"] not in trabajo:
            trabajo[paciente["Categoria Empleado"]] = 1
        else:
            trabajo[paciente["Categoria Empleado"]] = trabajo[paciente["Categoria Empleado"]] + 1

    del trabajo[""] # Eliminamos aquellos casos en los que no esté especificado el trabajo del paciente.

    return trabajo

def cantidad_ingresos(pacientes):

    ingresos = {} # Diccionario de los ingresos de cada paciente.

    for paciente in pacientes:
        if paciente["Ingresos"] not in ingresos:
            ingresos[paciente["Ingresos"]] = 1
        else:
            ingresos[paciente["Ingresos"]] = ingresos[paciente["Ingresos"]] + 1

    del ingresos["None"] # Eliminamos aquellos casos en los que no estén especificado los ingresos del paciente.

    return ingresos

def dict_con_rango(datos, variable, n_rango):

    valores = [dato[variable] for dato in datos] # Aquí guardamos una lista con todos los valores de la variable.
    valores[:] = (valor for valor in valores if valor != "None") # Eliminamos todas los valores desconocidos, que en nuestro archivo .csv están marcados como "None".
    # Seguidamente buscamos el máximo y el mínimo para encontrar el rango.
    valor_min = float(min(valores, key=float))
    valor_max = float(max(valores, key=float))

    # Quiero crear n rangos de distintos de esta variable. Estos rangos se generan entre el máximo y el mínimo.
    if (valor_max - valor_min) < 1:
        k = 100
    else:
        k = 1

    rango = (valor_max - valor_min) * k //n_rango
    x = valor_min
    keys = [] # Creamos una lista vacía con los rangos.

    for i in range(n_rango): # En este bucle creamos los rangos de ambas variables(edad y educación).
        key = "{:.2f}".format(x) + "-" + "{:.2f}".format(x + rango/k)
        x = x + rango/k
        keys.append(key)

    values = [0] * n_rango # Lista del número de pacientes por rango (ponemos 5 ceros al haber establecido que queremos 5 rangos).

    for valor in valores: # Bucle que estudia la edad de cada paciente
        for i in range(n_rango):
            if float(valor) < (valor_min + (i + 1) * (rango/k)):
                values[i] = values[i] + 1
                break

    return dict(zip(keys, values))

def puntuacion_puestos(usuarios):

    stalls = {} # Diccionario con el número de stalls visitados por cada paciente.

    for usuario in usuarios:
        if usuario["Número de puestos visitados"] not in stalls:
            stalls[usuario["Número de puestos visitados"]] = 1
        else:
            stalls[usuario["Número de puestos visitados"]] = stalls[usuario["Número de puestos visitados"]] + 1

    return stalls

def puesto_masvisitado(usuarios):
    stall = {} # Diccionario con el número de stalls visitados por cada paciente.

    for usuario in usuarios:
        if usuario["Número último puesto visitado"] not in stall:
            stall[usuario["Número último puesto visitado"]] = 1
        else:
            stall[usuario["Número último puesto visitado"]] = stall[usuario["Número último puesto visitado"]] + 1

    return stall

def juntar_diccionarios(diccionario):
    for usuario in diccionario:
        id = usuario["ID Paciente"]
        dict = next((paciente for paciente in pacientes if paciente["ID Paciente"] == id), None)
        usuario.update(dict)

def borrar_datos(x):
    n, m = np.shape(x)
    filas_borrar = []

    for i in range(n):
        for j in range(m):
            if x[i,j] == "None":
                filas_borrar.append(i)
                break
            else:
                x[i,j] = float(x[i,j])

    for i in reversed(filas_borrar):
        x = np.delete(x, i, axis = 0)

    return x

def append(x, *matrix):
    n = len(x)
    x = np.reshape(x, (n, 1))

    for m in matrix:
        m = np.reshape(m, (n, 1))
        x = np.append(x, m, axis = 1)

    x = borrar_datos(x)
    
    return x

def digitalizar(vector):
    categoria = []
    
    for v in vector:
        if v not in categoria:
            categoria.append(v)
    
    for c in categoria:
        index = categoria.index(c)
        vector[vector == c] = index

    return vector

def split(matriz):
    np.random.shuffle(matriz)
    n, m = np.shape(matriz)
    n1 = int(n * 0.75)

    A1 = matriz[:n1, :]
    A2 = matriz[(n1+ 1):, :]

    return A1, A2

def diagrama_barras(variable, titulo, horizontal, saveas):

    if horizontal == True: # Con la variable horizontal marco si quiero realizar una gráfica de barras horizontales o verticales.
        plt.barh(list(variable.keys()), variable.values(), color = np.random.rand(3,)) # La información que aparecerá en los ejes.
        plt.xlabel("Número de pacientes") # Título que explica los datos del eje X.

    else:
        plt.bar(variable.keys(), variable.values(), color = np.random.rand(3,)) # La información que aparecerá en los ejes.
        plt.ylabel("Número de pacientes") # Título que explica los datos del eje Y.

    plt.title(titulo)
    #plt.savefig("img/" + saveas + ".pdf")
    plt.show()

def scatter(x, columna1, columna2, titulo_x, titulo_y, titulo):
    plt.scatter(x[:, columna1], x[:, columna2])
    plt.xlabel(titulo_x)
    plt.ylabel(titulo_y)
    plt.title(titulo)
    plt.show()

# ----- L E C T U R A   D E   A R C H I V O -----
# Primero analizamos el fichero y creamos una lista de diccionarios.

# Fichero Patient_Profile.csv
perfil_paciente = "health-care analytics\Train\Patient_Profile.csv"
var_paciente = ["Patient_ID", "Online_Follower", "LinkedIn_Shared", "Twitter_Shared", "Facebook_Shared", "Income", "Education_Score", "Age", "First_Interaction", "City_Type", "Employer_Category"]
traduccion_var = {"Patient_ID" : "ID Paciente", "Online_Follower" : "Seguidor Online", "LinkedIn_Shared" : "Comparte LinkedIn", "Twitter_Shared" : "Comparte Twitter", "Facebook_Shared" : "Comparte Facebook", "Income" : "Ingresos", "Education_Score" : "Educación", "Age" : "Edad", "First_Interaction" : "Primera Iteracción", "City_Type" : "Tipo Ciudad", "Employer_Category" : "Categoria Empleado"}
pacientes = leer_csv(perfil_paciente, var_paciente, traduccion_var)

# Fichero First_Health_Camp_Attended.csv
info_campamento1 = "health-care analytics\Train\First_Health_Camp_Attended.csv"
var_campamento1 = ["Patient_ID", "Health_Camp_ID", "Donation", "Health_Score"]
traduccion_var1 = {"Patient_ID":"ID Paciente", "Health_Camp_ID" : "ID Campamento", "Donation" : "Donación", "Health_Score" : "Puntuación Salud"}
usuarios_1 = leer_csv(info_campamento1, var_campamento1, traduccion_var1)

# Fichero Second_Health_Camp_Attended.csv
info_campamento2 = "health-care analytics\Train\Second_Health_Camp_Attended.csv"
var_campamento2 = ["Patient_ID", "Health_Camp_ID", "Health Score"]
traduccion_var2 = {"Patient_ID":"ID Paciente", "Health_Camp_ID" : "ID Campamento", "Health Score" : "Puntuación Salud"}
usuarios_2 = leer_csv(info_campamento2, var_campamento2, traduccion_var2)

# Fichero Third_Health_Camp_Attended.csv
info_campamento3 = "health-care analytics\Train\Third_Health_Camp_Attended.csv"
var_campamento3= ["Patient_ID", "Health_Camp_ID", "Number_of_stall_visited", "Last_Stall_Visited_Number"]
traduccion_var3 = {"Patient_ID":"ID Paciente", "Health_Camp_ID" : "ID Campamento", "Number_of_stall_visited" : "Número de puestos visitados", "Last_Stall_Visited_Number" : "Número último puesto visitado"}
usuarios_3 = leer_csv(info_campamento3, var_campamento3, traduccion_var3)

# ----- G R Á F I C A S -----
# Vamos a realizar las gráficas de barras con los datos analizados hasta ahora.

# Datos de pacientes.
#diagrama_barras(seguimiento_online(pacientes), "Pacientes y su seguimiento Online de MedCamp", True, "Seguimiento Online")
#diagrama_barras(tipos_ciudades(pacientes), "¿En qué ciudades viven nuestros pacientes?", False, "Ciudades")
#diagrama_barras(tipo_trabajo(pacientes), "¿En qué trabajan los pacientes de MedCamp?", True, "Trabajo")
#diagrama_barras(cantidad_ingresos(pacientes), "Relación Ingresos - Paciente", False, "Ingresos")
#diagrama_barras(dict_con_rango(pacientes, "Edad", 5), "Edad de los pacientes de MedCamp", False, "Edad")
#diagrama_barras(dict_con_rango(pacientes, "Educación", 5), "Puntuación de la educación recibida por lo pacientes", True, "Educacion")

# Datos de campamentos.
#diagrama_barras(dict_con_rango(usuarios_1, "Puntuación Salud", 12), "Puntuación de Salud del Primer Campamento de Medcamp", True, "Puntuación1")
#diagrama_barras(dict_con_rango(usuarios_2, "Puntuación Salud", 12), "Puntuación de Salud del Segundo Campamento de Medcamp", True, "Puntuacion2")
#diagrama_barras(puntuacion_puestos(usuarios_3), "Número total de puestos visitados por cada paciente en el Tercer Campamento", False, "NumeroStalls")
#diagrama_barras(puesto_masvisitado(usuarios_3), "Puesto más visitado como el último puesto de los pacientes", False, "UltimoPuesto")

# Análisis de datos con el cruce de pacientes y campamentos.
# Ahora queremos comparar datos de archivos diferentes. Para ello, vamos a juntarlos. Vamos a crear una súpertabla.
# Comenzamos modificando los diccionarios usuarios_1, usuarios_2 y usuarios_3 añadiéndoles la información del paciente que está en el diccionario pacientes.

juntar_diccionarios(usuarios_1)
juntar_diccionarios(usuarios_2)
juntar_diccionarios(usuarios_3)

# Tras estas preparaciones, graficamos. Esta vez se dibuja un diagrama de dispersión.

A = np.array([dato["Edad"] for dato in usuarios_1])
x = np.array([dato["Educación"] for dato in usuarios_1])
i = np.array([dato["Ingresos"] for dato in usuarios_1])
z = np.array([dato["Comparte LinkedIn"] for dato in usuarios_1])
s = np.array([dato["Comparte Twitter"] for dato in usuarios_1])
r = np.array([dato["Comparte Facebook"] for dato in usuarios_1])
t = np.array([dato["Seguidor Online"] for dato in usuarios_1])
w = np.array([dato["Tipo Ciudad"] for dato in usuarios_1])
w = digitalizar(w)
c = np.array([dato["Categoria Empleado"] for dato in usuarios_1])
c = digitalizar(c)
y = np.array([dato["Puntuación Salud"] for dato in usuarios_1])
A = append(A, x, i, z, s, r, t, w, c, y)

#scatter(A, 0, -1, "Edad", "Puntuación de Salud", "Edad vs. Puntuación")
#scatter(A, 2, -1, "Ingresos", "Puntuación de Salud", "Ingresos vs. Puntuación")
#scatter(A, 7, -1, "Tipo Ciudad", "Puntuación de Salud", "Ciudad vs. Puntuación")

# -----  F I N   A N Á L I S I S   D E   D A T O S   -----

# Vamos a predecir la probabilidad de que el paciente obtenga un resultado favorable, es decir, que termine el campamento con una buena puntuación.

x_training, x_test = split(A)

y_training = x_training[:, -1]
y_training = np.reshape(y_training, (len(y_training), 1))
x_training = np.delete(x_training, -1, axis = 1)

y_test = x_test[:, -1]
y_test = np.reshape(y_test, (len(y_test), 1))
x_test = np.delete(x_test, -1, axis = 1)


lin_model = LinearRegression()
lin_model.fit(x_training, y_training)

# Evalua el modelo contra desviacion media (los 10 primeros valores)
y_train_predict = lin_model.predict(x_test)
rmse = (np.sqrt(mean_squared_error(y_test, y_train_predict)))

print("El rendimiento del modelo")
print("--------------------------------------")
print('El error cuadrático medio es {}'.format(rmse))
print("\n")