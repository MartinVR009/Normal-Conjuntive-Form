import re

# Definición del patrón
pattern_knowledge = r'^Q: *(~*\w+)(\([\w,]+\))$'

# Cadena de prueba
test_string = 'Q:Odia(Marco,Cesar)'

# Mostrar resultados
if re.match(pattern_knowledge, test_string):
    # match[0] contiene la parte capturada de la expresión regular
    print("Coincide:")  # La parte principal de la captura
else:
    print("No coincide.")
