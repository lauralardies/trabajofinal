import matplotlib.pyplot as plt

# Primero analizamos el fichero y creamos una lista de diccionarios.

try:
    f = open("healthcare-analytics\Train\Patient_Profile.csv")

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
        if linea or any(linea) or any(field.strip() for field in linea):            
            paciente = {}
            linea = linea.strip()
            campos = linea.split(",")
            for i in range(len(columnas)):
                if columnas[i] in seleccion:
                    paciente[traduccion[columnas[i]]] = campos[i]
                pacientes.append(paciente)

    # Ahora analizamos los datos ordenados.

    n = len(pacientes) # Número de pacientes en total.

    print ("Numero de pacientes:" + str(n))
    m = 0 # Número de pacientes que siguen online a MedCamp.
    l = 0 # Número de pacientes que siguen en LinkedIn a MedCamp.
    t = 0 # Número de pacientes que siguen en Twitter a Medcamp.
    f = 0 # Número de pacientes que siguen en Facebook a Medcamp.
    ciudades = {} # Diccionario de las ciudades con el número de pacientes que vive en cada una de ellas.
    trabajo = {} # Diccionario de los trabajos con el número de pacientes que se dedican a ello.
    
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
        
    del ciudades[""] # Eliminamos aquellos casos en los que no esté especificada la ciudad del paciente.
    del trabajo[""] # Eliminamos aquellos casos en los que no esté especificado el trabajo del paciente.

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
    plt.ylabel("Trabajos") # Título que explica los datos del eje Y.
    plt.xlabel("Número de pacientes") # Título que explica los datos del eje X.
    plt.title("Relación Paciente - Trabajo") # Título de la gráfica.
    plt.show()

    # A parir de ahora, las variables que vamos a analizar las guardaremos en diccionarios que tienen rangos (Ej. de 60 a 70 años va a ser una entrada del diccionario "edades").
    # Por lo tanto, para determinar estos rangos vamos a tener que calcular el mínimo y máximo de estas variables.

    #valores = [paciente["Edad"] for paciente in pacientes] # Aquí guardamos una lista con todas las edades de los pacientes.
    #valores[:] = (valor for valor in valores if valor != "None") # Eliminamos todas las edades desconocidas, que en nuestro archivo .csv están marcadas como "None".
    #edad_min = int(min(valores))
    #edad_max = int(max(valores))

    # Quiero hacer 5 rangos.
    #rango = (edad_max - edad_min)//5
    #x = edad_min
    #keys = [] # Creamos una lista vacía con los rangos

    #for i in range(5):
    #    key = "[" + str(x) + "-" + str(x+rango) + "]"
    #    x = x + rango
    #    keys.append(key)

    #values = [0, 0, 0, 0, 0]

    #for valor in valores:
    #    for i in range(5):
    #        if int(valor) < (edad_min + (i + 1)*rango):
    #            values[i] = values[i] + 1
    #            break
    
    #print(keys)
    #print(values)
    print(n)