import sys
import re

# Definición de patrones
pattern_rule = r'^[0-9]+\.\s*(~?\w+)\(([\w,?]+)\) *$'
pattern_knowledge = r'[0-9]+\. *(~?\w+\([\w,?]+\))( *[∨|or] *(~?\w+\([\w,?]+\)))*'
pattern_question = r'^Q: *(~?\w+)\(([\w,?]+)\)$'

KB = list()  # List of rules
questions = list()

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
    print("Resolver Preguntas:")
    for q in questions:
        print(f"Resolviendo pregunta: {q}")
        result = resolution(q)
        print(f"Resultado:" , "Verdadero" if result else "Falso")

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
        questions.append(question)
        print(f"Pregunta procesada: {question} \n")
        # Lógica para llamar al proceso de inferencia o resolución

def resolution(question):
    negated_question = negate_q(question)
    clauses = KB + [negated_question]
    resolved = False

    
    while not resolved:
        new_clauses = []
        for clause1 in clauses:
            for clause2 in clauses:
                resolvent = resolve(clause1, clause2)
                if resolvent == []:
                    resolved = True
                    return True
                if resolvent:
                    new_clauses.append(resolvent)
        if not new_clauses:
            resolved = True
            return False
        clauses.extend(new_clauses)
            
    return False  # No se resolvió la pregunta


def negate(statement):
    return f"~{statement}" if not statement.startswith("~") else statement[1:]

def negate_q(question):
    negated = f"{question.name}" if not question.name.startswith("~") else question.name[1:]
    return Question(negated, question.argument)

def resolve(question, clause2):
    resolvents = []

    # Tries to find literal and clauses to eliminate 
    if isinstance(question,Knowledge):
        c1_rules = question.rules
    else:
        c1_rules = [question]

    if isinstance(question, Knowledge):
        c2_rules = clause2.rules
    else:
        c2_rules = [clause2]

    for c1 in c1_rules:
        for c2 in c2_rules:

            if c1.name == negate(c2.name):
                substitution = unify(c1.arguments, c2.arguments)
                if substitution != None:
                    new_clause = apply_substitution(question, clause2, substitution)
                    if isinstance(new_clause, Knowledge) and len(new_clause.rules) == 0:
                        return []
                    resolvents.append(new_clause)
    return resolvents

def apply_substitution(clause1, clause2, substitution):
    def substitute(argument):
        return substitution.get(argument, argument)

    new_clause_rules = []

    # Aplicar sustitución a todas las reglas de las cláusulas originales
    clause1_rules = clause1.rules if isinstance(clause1, Knowledge) else [clause1]
    clause2_rules = clause2.rules if isinstance(clause2, Knowledge) else [clause2]

    for rule in clause1_rules + clause2_rules:
        new_arguments = [substitute(arg) for arg in rule.arguments]
        # Evitar incluir la regla que se resolvió (negada)
        if rule.name not in [negate(rule.name) for rule in clause1_rules + clause2_rules]:
            new_clause_rules.append(Rule(rule.name, new_arguments))

    # Si hay más de una regla, devolver un Knowledge, de lo contrario devolver la única regla
    if len(new_clause_rules) == 1:
        return new_clause_rules[0]
    else:
        return Knowledge(new_clause_rules)
    
# Function to unify same len arg's and replace ? with arg's of the other
def unify(args1, args2):
    if len(args1) != len(args2):
        return None  # If they don't receive same number of args, they can't unify
    substitution = {}
    for a1, a2 in zip(args1, args2):
        if is_variable(a1):
            substitution[a1] = a2
        elif is_variable(a2):
            substitution[a2] = a1
        elif a1 != a2:
            return None  # Not unifiable
    return substitution

def is_variable(arg):
    return arg.startswith('?')

if __name__ == "__main__":
    main()
