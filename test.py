import re

# Definición del patrón
pattern_knowledge = r'(\w+)\(([\w, ]+)\)'

# Cadena de prueba
test_string = 'algo(example1,example2) algo(example1,example2) algo(example1,example2) algo(example1,example2)'

# Buscar coincidencias
matches = re.findall(pattern_knowledge, test_string)

str_test = "ejemplo1/ejemplo2"

print(str_test.split('/'))

# Mostrar resultados
if matches:
    # match[0] contiene la parte capturada de la expresión regular
    print("Coincide:", matches[0])  # La parte principal de la captura
else:
    print("No coincide.")
