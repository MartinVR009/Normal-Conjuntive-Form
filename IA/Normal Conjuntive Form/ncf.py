#1.Define KB structure (Knowledge Base)
#2.Base input management
#3.Resolution Operation
#4.Contradiction Operations
#5.Unification (If Necessary)
#6.Question management
#7.Main program cycle

import sys
import os 
import re

pattern_rule = r'^[0-9]+\.\s*(\w+)(\([\w,]+\)) *$'
pattern_knowledge = r'[0-9]+\. *(\w+\([\w,]+\))( * ∨ *(\w+\([\w,]+\)))*'
pattern_question = r'^Q: *(\w+)(\([\w,]+\))$'

KB = list() #List of rules

class Rule:
    def __init__(self, name, arguments):
        self.name = name
        self.argument = arguments 

class Knowledge:
    def __init__(self, rules):
        self.rules = rules
    

class Question:
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

def main():
    read_file(sys.argv[1])

def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            for line in file:
                rule = line.split('.')
                read_statement(line)
    except FileNotFoundError:
        print(f"Error, el archivo {file_name} no pudo ser abierto")
        sys.exit(1)   

def read_statement(statement):
    #Verify if is Rule
    if re.match(pattern_rule, statement):
        process_rule(statement)
    #Verify if is Knowledge
    if re.match(pattern_knowledge, statement):
        process_knowledge(statement)
    #Verify if is Question
    if re.match(pattern_rule, statement):
        process_question(statement)

def process_rule(statement):
    # Extract Name and Argument of Rule
    match = re.match(pattern_rule, statement)
    if match:
        name = match.group(1)  # Rule name
        argument = match.group(2)  # Rule argument
        if re.search(r',', argument):
            argument = argument.split(',') 
        rule = Rule(name, argument)
        KB.append(rule)
        print(f"Regla procesada: {rule}")

def process_knowledge(statement):
    # Find all Rules separated by ∨
    matches = re.findall(r'(\w+)\(([\w, ]+)\)', statement)

    rules = list() 

    if matches:
        for name, args in matches:
            rule = Rule(name, args)
            rules.append(rule)

        knowledge = Knowledge(rules)
        
        KB.append(knowledge)
        
        print(f"Conocimiento procesado: {knowledge}")


def process_question(statement):
    # Extraer el nombre y argumento de la pregunta
    match = re.match(pattern_question, statement)
    if match:
        name = match.group(1)  # Question Name
        argument = match.group(2)  # Question Argument
        question = Question(name, argument)
        print(f"Pregunta procesada: {question}")
        # Logica de empezar alguna funcion para llamar a la inferencia o demas
    else:
        print(f"Formato de pregunta inválido: {statement}")


if __name__ == "__main__":
    main()