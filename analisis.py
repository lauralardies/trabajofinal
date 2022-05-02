import matplotlib.pyplot as plt
import numpy as np

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

    online = {"m" : 0, "l" :0, "t" : 0, "f" : 0}

    for paciente in pacientes:
        if paciente["Seguidor_Online"] != "0":
            online["m"] = online["m"] + 1
        if paciente["Comparte_LinkedIn"] != "0":
            online["l"] = online["l"] + 1
        if paciente["Comparte_Twitter"] != "0":
            online["t"] = online["t"] + 1
        if paciente["Comparte_Facebook"] != "0":
            online["f"] = online["f"] + 1

    return online

def tipos_ciudades(pacientes):

    ciudades = {} # Diccionario de las ciudades con el número de pacientes que vive en cada una de ellas.

    for paciente in pacientes:
        if paciente["Tipo_Ciudad"] not in ciudades:
                ciudades[paciente["Tipo_Ciudad"]] = 1
        else:
            ciudades[paciente["Tipo_Ciudad"]] = ciudades[paciente["Tipo_Ciudad"]] + 1

    del ciudades[""] # Eliminamos aquellos casos en los que no esté especificada la ciudad del paciente.

    return ciudades

def tipo_trabajo(pacientes):

    trabajo = {} # Diccionario de los trabajos con el número de pacientes que se dedican a ello.

    for paciente in pacientes:
        if paciente["Categoria_Empleado"] not in trabajo:
            trabajo[paciente["Categoria_Empleado"]] = 1
        else:
            trabajo[paciente["Categoria_Empleado"]] = trabajo[paciente["Categoria_Empleado"]] + 1

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

def edades_o_educacion(pacientes, variable):

    valores = [paciente[variable] for paciente in pacientes] # Aquí guardamos una lista con todos los valores de la variable.
    valores[:] = (valor for valor in valores if valor != "None") # Eliminamos todas los valores desconocids, que en nuestro archivo .csv están marcadas como "None".
    # Seguidamente buscamos el máximo y el mínimo para encontrar el rango.
    valor_min = float(min(valores, key=float))
    valor_max = float(max(valores, key=float))
    # Quiero crear 5 rangos de distintos de esta variable. Estos rangos se generan entre el máximo y el mínimo.
    rango = (valor_max - valor_min)//5
    x = valor_min
    keys = [] # Creamos una lista vacía con los rangos.

    for i in range(5): # En este bucle creamos los rangos de ambas variables(edad y educación).
        key = str(x) + "-" + str(x + rango)
        x = x + rango
        keys.append(key)

    values = [0, 0, 0, 0, 0] # Lista del número de pacientes por rango (ponemos 5 ceros al haber establecido que queremos 5 rangos).

    for valor in valores: # Bucle que estudia la edad de cada paciente
        for i in range(5):
            if float(valor) < (valor_min + (i + 1) * rango):
                values[i] = values[i] + 1
                break

    return dict(zip(keys, values))

def graficas(variable, horizontal):

    if horizontal == True: # Con la variable horizontal marco si quiero realizar una gráfica de barras horizontales o verticales.
        plt.barh(list(variable.keys()), variable.values(), color = np.random.rand(3,)) # La información que aparecerá en los ejes.
        plt.xlabel("Número de pacientes") # Título que explica los datos del eje X.

    else:
        plt.bar(variable.keys(), variable.values(), color = np.random.rand(3,)) # La información que aparecerá en los ejes.
        plt.ylabel("Número de pacientes") # Título que explica los datos del eje Y.

    plt.show()

# ----- L E C T U R A   D E   A R C H I V O -----
# Primero analizamos el fichero y creamos una lista de diccionarios.

perfil_paciente = "health-care analytics\Train\Patient_Profile.csv"
var_paciente = ["Patient_ID", "Online_Follower", "LinkedIn_Shared", "Twitter_Shared", "Facebook_Shared", "Income", "Education_Score", "Age", "First_Interaction", "City_Type", "Employer_Category"]
traduccion_var = {"Patient_ID":"ID_Paciente", "Online_Follower":"Seguidor_Online", "LinkedIn_Shared":"Comparte_LinkedIn", "Twitter_Shared":"Comparte_Twitter", "Facebook_Shared":"Comparte_Facebook", "Income":"Ingresos", "Education_Score":"Educación", "Age":"Edad", "First_Interaction":"Primera_Iteracción", "City_Type":"Tipo_Ciudad", "Employer_Category":"Categoria_Empleado"}

pacientes = leer_csv(perfil_paciente, var_paciente, traduccion_var)

# ----- G R Á F I C O S -----
# Vamos a realizar las gráficas de barras con los datos analizados hasta ahora.

graficas(seguimiento_online(pacientes), False)
graficas(tipos_ciudades(pacientes), False)
graficas(tipo_trabajo(pacientes), True)
graficas(cantidad_ingresos(pacientes), False)
graficas(edades_o_educacion(pacientes, "Edad"), False)
graficas(edades_o_educacion(pacientes, "Educación"), False)
