try:
    f = open("healthcare-analytics\Train\Patient_Profile.csv")

except FileNotFoundError:
    print("El fichero no existe.")
    
else:
    lineas = f.readlines()
    f.close()

    columnas = lineas[0].split(",")
    seleccion = ["Patient_ID", "Online_Follower", "LinkedIn_Shared", "Twitter_Shared", "Facebook_Shared", "Income", "Education_Score", "Age", "First_Interaction", "City_Type", "Employer_Category"]
    traduccion = {"Patient_ID":"ID_Paciente", "Online_Follower":"Seguidor_Online", "LinkedIn_Shared":"Comparte_LinkedIn", "Twitter_Shared":"Comparte_Twitter", "Facebook_Shared":"Comparte_Facebook", "Income":"Ingresos", "Education_Score":"Educación", "Age":"Edad", "First_Interaction":"Primera_Iteracción", "City_Type":"Tipo_Ciudad", "Employer_Category":"Categoría_Empleado"}

    pacientes = []

    for linea in lineas[1:]:
            paciente = {}
            campos = linea.split(",")
            for i in range(len(columnas)):
                if columnas[i] in seleccion:
                    paciente[traduccion[columnas[i]]] = campos[i]
            pacientes.append(paciente)

    print(pacientes)