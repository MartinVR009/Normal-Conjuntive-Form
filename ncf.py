import sys
import re

# Definición de patrones
pattern_rule = r'^[0-9]+\.\s*(~?\w+)\(([\w,?]+)\) *$'
pattern_knowledge = r'[0-9]+\. *(~?\w+\([\w,?]+\))( *[∨|or] *(~?\w+\([\w,?]+\)))*'
pattern_question = r'^Q: *(~?\w+)\(([\w,?]+)\)$'

KB = list()  # List of rules
questions = list()
answers = list()

class Rule:
    def __init__(self, name, arguments):
        self.name = name
        self.argument = arguments
    
    def __str__(self):
        return f"{self.name}({', '.join(self.argument)})" if isinstance(self.argument, list) else f"{self.name}({self.argument})"

class Knowledge:
    def __init__(self, rules):
        self.rules = rules
    
    def __str__(self):
        return " ∨ ".join(str(rule) for rule in self.rules)

class Question:
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument
    
    def __str__(self):
        return f"{self.name}({', '.join(self.argument)})" if isinstance(self.argument, list) else f"{self.name}({self.argument})"

def main():
    read_file(sys.argv[1])
    for k in KB:
        print(k)

def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()  # Eliminar espacios en blanco
                print(f"Línea a leer: {line}")
                read_statement(line)
    except FileNotFoundError:
        print(f"Error, el archivo {file_name} no pudo ser abierto")
        sys.exit(1)

def clean_arguments(argument):
    """Limpia los paréntesis y maneja variables con '?'"""
    # Remover paréntesis y dividir si hay comas
    cleaned_args = argument.replace('(', '').replace(')', '').split(',')
    return [arg.strip() for arg in cleaned_args]  # Limpiar espacios

def read_statement(statement):
    # Verificar si es una regla
    if re.match(pattern_rule, statement):
        print("Entró por RULE")
        process_rule(statement)
    # Verificar si es conocimiento
    elif re.match(pattern_knowledge, statement):
        print("Entró por KNOWLEDGE")
        process_knowledge(statement)
    # Verificar si es pregunta
    elif re.match(pattern_question, statement):
        print("Entró por QUESTION")
        process_question(statement)
    else:
        print(f"La línea: {statement} no tiene un formato permitido")

def process_rule(statement):
    # Extraer nombre y argumento de la regla
    match = re.match(pattern_rule, statement)
    if match:
        name = match.group(1)  # Nombre de la regla
        argument = match.group(2)  # Argumento de la regla
        argument = clean_arguments(argument)  # Limpiar paréntesis y espacios

        rule = Rule(name, argument)
        KB.append(rule)
        print(f"Regla procesada: {rule} \n")

def process_knowledge(statement):
    # Encontrar todas las reglas separadas por ∨
    matches = re.findall(r'(~?\w+)\(([\w,?]+)\)', statement)
    rules = list()

    if matches:
        for name, args in matches:
            args_cleaned = clean_arguments(args)  # Limpiar paréntesis y espacios
            rule = Rule(name, args_cleaned)
            rules.append(rule)

        knowledge = Knowledge(rules)
        KB.append(knowledge)
        print(f"Conocimiento procesado: {knowledge} \n")

def process_question(statement):
    # Extraer nombre y argumento de la pregunta
    match = re.match(pattern_question, statement)
    if match:
        name = match.group(1)  # Nombre de la pregunta
        argument = match.group(2)  # Argumento de la pregunta
        argument = clean_arguments(argument)  # Limpiar paréntesis y espacios

        question = Question(name, argument)
        print(f"Pregunta procesada: {question} \n")
        # Lógica para llamar al proceso de inferencia o resolución

def resolution(question):
    negated_question = negate(question)
    actual_clause = negated_question
    resolved = False

    KnowledgeBase = KB + actual_clause
    
    while actual_clause != None:
        for clause1 in KnowledgeBase:
            resolvent = resolve(actual_clause, actual_clause)
            
    
    return False  # No se resolvió la pregunta


def negate(question):
    if question.name.startswith("~"):
        return Question(question.name[1:], question.argument)
    else:
        return Question(f"~{question.name}", question.argument)

def resolve(question, clause2):
    # Try's to find literal and clauses to eliminate 
    if isinstance(question,Knowledge):
        for rule1 in question.rules:
            for rule2 in clause2.rules:
                if rule1.name == negate(rule2).name:
                    # Unification and elimination
                    new_clause = [r for r in question.rules if r != rule1] + [r for r in clause2.rules if r != rule2]
                    return new_clause
    return None


if __name__ == "__main__":
    main()
