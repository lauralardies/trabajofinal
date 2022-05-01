import matplotlib.pyplot as plt

# ----- L E C T U R A   D E   A R C H I V O -----
# Primero analizamos el fichero y creamos una lista de diccionarios.

try:
    f = open("health-care analytics\Train\Patient_Profile.csv")

except FileNotFoundError:
    print("El fichero no existe.")

else:
    lineas = f.readlines()
    f.close()

    linea = lineas[0].strip()
    columnas = linea.split(",")
    seleccion = ["Patient_ID", "Online_Follower", "LinkedIn_Shared", "Twitter_Shared", "Facebook_Shared", "Income", "Education_Score", "Age", "First_Interaction", "City_Type", "Employer_Category"]
    traduccion = {"Patient_ID":"ID_Paciente", "Online_Follower":"Seguidor_Online", "LinkedIn_Shared":"Comparte_LinkedIn", "Twitter_Shared":"Comparte_Twitter", "Facebook_Shared":"Comparte_Facebook", "Income":"Ingresos", "Education_Score":"Educación", "Age":"Edad", "First_Interaction":"Primera_Iteracción", "City_Type":"Tipo_Ciudad", "Employer_Category":"Categoria_Empleado"}

    pacientes = []

    for linea in lineas[1:]:
        paciente = {}
        linea = linea.strip()
        campos = linea.split(",")
        for i in range(len(columnas)):
            if columnas[i] in seleccion:
                paciente[traduccion[columnas[i]]] = campos[i]
        pacientes.append(paciente)

    # Ahora analizamos los datos ordenados.

    n = len(pacientes) # Número de pacientes en total.

    # ----- A N Á L I S I S   D E   R E D E S   S O C I A L E S ,   C I U D A D E S,   T R A B A J O   E   I N G R E S O S -----

    m = 0 # Número de pacientes que siguen online a MedCamp.
    l = 0 # Número de pacientes que siguen en LinkedIn a MedCamp.
    t = 0 # Número de pacientes que siguen en Twitter a Medcamp.
    f = 0 # Número de pacientes que siguen en Facebook a Medcamp.
    ciudades = {} # Diccionario de las ciudades con el número de pacientes que vive en cada una de ellas.
    trabajo = {} # Diccionario de los trabajos con el número de pacientes que se dedican a ello.
    ingresos = {} # Diccionario de los ingresos de ccada paciente.

    for paciente in pacientes:
        # Análisis del seguimiento en redes sociales.
        if paciente["Seguidor_Online"] != "0":
            m = m + 1
        if paciente["Comparte_LinkedIn"] != "0":
            l = l + 1
        if paciente["Comparte_Twitter"] != "0":
            t = t + 1
        if paciente["Comparte_Facebook"] != "0":
            f = f + 1

        # Análisis de las ciudades.
        if paciente["Tipo_Ciudad"] not in ciudades:
            ciudades[paciente["Tipo_Ciudad"]] = 1
        else:
            ciudades[paciente["Tipo_Ciudad"]] = ciudades[paciente["Tipo_Ciudad"]] + 1

        # Análisis de los trabajos.
        if paciente["Categoria_Empleado"] not in trabajo:
            trabajo[paciente["Categoria_Empleado"]] = 1
        else:
            trabajo[paciente["Categoria_Empleado"]] = trabajo[paciente["Categoria_Empleado"]] + 1
        
        # Análisis de los ingresos.
        if paciente["Ingresos"] not in ingresos:
            ingresos[paciente["Ingresos"]] = 1
        else:
            ingresos[paciente["Ingresos"]] = ingresos[paciente["Ingresos"]] + 1
        
    del ciudades[""] # Eliminamos aquellos casos en los que no esté especificada la ciudad del paciente.
    del trabajo[""] # Eliminamos aquellos casos en los que no esté especificado el trabajo del paciente.
    del ingresos["None"] # Eliminamos aquellos casos en los que no estén especificado los ingresos del paciente.

    # ----- A N Á L I S I S   D E   E D A D E S   Y   E D U C A C I Ó N -----
    # A parir de ahora, las variables que vamos a analizar las guardaremos en diccionarios que tienen rangos (Ej. de 60 a 70 años va a ser una entrada del diccionario "edades").
    # Por lo tanto, para determinar estos rangos vamos a tener que calcular el mínimo y máximo de estas variables.

    valores_edad = [paciente["Edad"] for paciente in pacientes] # Aquí guardamos una lista con todas las edades de los pacientes.
    valores_edad[:] = (valor_edad for valor_edad in valores_edad if valor_edad != "None") # Eliminamos todas las edades desconocidas, que en nuestro archivo .csv están marcadas como "None".
    edad_min = int(min(valores_edad))
    edad_max = int(max(valores_edad))

    # Quiero hacer 5 rangos.
    rango = (edad_max - edad_min)//5
    x = edad_min
    keys = [] # Creamos una lista vacía con los rangos.

    for i in range(5): # En este bucle creamos los rangos de edades.
        key = str(x) + "-" + str(x+rango)
        x = x + rango
        keys.append(key)

    values = [0, 0, 0, 0, 0] # Lista del número de pacientes por rango (ponemos 5 ceros al haber establecido que queremos 5 rangos).

    for valor_edad in valores_edad: # Bucle que estudia la edad de cada paciente
        for i in range(5):
            if int(valor_edad) < (edad_min + (i + 1)*rango):
                values[i] = values[i] + 1
                break

    # ----- G R Á F I C O S -----
    # Vamos a realizar las gráficas de barras con los datos analizados hasta ahora.

    # 1º Gráfica del seguimiento Online.
    plt.bar(["Seguidor\n Online", "Comparte en\n LinkedIn", "Comparte en\n Twitter", "Comparte en\n Facebook"], [m, l, t, f]) # La información que aparecerá en los ejes.
    plt.xlabel("Actividad en las redes sociales") # Título que explica los datos del eje X.
    plt.ylim(0, (max(m, l, t, f)*1.5)) # Determinamos a nuestro gusto el límite del eje Y.
    plt.ylabel("Número de pacientes") # Título que explica los datos del eje Y.
    plt.title("Relación Paciente - Redes Sociales") # Título de la gráfica.
    plt.show() # Comando que muestra la gráfica.

    # 2º Gráfica de barras de las ciudades en relación con los pacientes.
    plt.bar(ciudades.keys(), ciudades.values(), color="green") # La información que aparecerá en los ejes.
    plt.xlabel("Tipos de Ciudades") # Título que explica los datos del eje X.
    plt.ylabel("Número de pacientes") # Título que explica los datos del eje Y.
    plt.title("Relación Paciente - Ciudad") # Título de la gráfica.
    plt.show()

    # 3º Gráfica de barras (horizontal) de los trabajos en relación con los pacientes.
    plt.barh(list(trabajo.keys()), trabajo.values(), color="pink") # La información que aparecerá en los ejes.
    plt.xlabel("Número de pacientes") # Título que explica los datos del eje X.
    plt.ylabel("Trabajos") # Título que explica los datos del eje Y.
    plt.title("Relación Paciente - Trabajo") # Título de la gráfica.
    plt.show()

    # 4º Gráfica de barras de los rangos de edades de los pacientes.
    plt.bar(keys, values, color="orange") # La información que aparecerá en los ejes.
    plt.xlabel("Edad") # Título que explica los datos del eje X.
    plt.ylabel("Número de pacientes") # Título que explica los datos del eje Y.
    plt.title("Relación Paciente - Edades") # Título de la gráfica.
    plt.show()

    # 5º Gráfica de barras de los ingresos de los pacientes.
    plt.bar(ingresos.keys(), ingresos.values(), color="purple") # La información que aparecerá en los ejes.
    plt.xlabel("Ingresos") # Título que explica los datos del eje X.
    plt.ylabel("Número de pacientes") # Título que explica los datos del eje Y.
    plt.title("Relación Paciente - Ingresos") # Título de la gráfica.
    plt.show()