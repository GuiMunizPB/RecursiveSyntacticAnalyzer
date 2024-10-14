# Recursive Syntactic Analyzer

## Parte do Projeto 1 (Sobre o Lexer):

### Definição dos tokens JSON:

* numbers, strings, '{}', '[]', ':', ',', true, false e null

Regex:

* utilização de expressões regulares para identificar os tokens.

Identificar erros léxicos e/ou de formatação:

* implementar o lexer com o regex, classificando tokens, e listando os possíveis erros de formatação do JSON de entrada ( no caso reportaremos o primeiro erro léxico encontrando ).

### Estudo da biblioteca re:
Implementação utilizando a biblioteca re do python
Estudo da biblioteca: Regular Expression Operations
https://docs.python.org/3/library/re.html

* The module supports both Unicode strings (str) and 8-bit strings (bytes), but these cannot be mixed.

* Special Characters: Characters like . (dot), ^ (caret), $ (dollar), * (asterisk), + (plus), ? (question mark), [] (brackets), () (parentheses), and | (pipe)

* Quantifiers: Symbols like *, +, and {m,n} control the number of times an element in the pattern can be repeated

* To avoid confusion with escape sequences in regular expressions, Python supports "raw strings," denoted by an r before the string

## Analisador Sintático:

Utilizando o lexer da primeira parte do projeto,  o Analisador Sintático irá usar os tokens produzidos para determinar a estrutura sintática da entrada, de acordo com a gramática da linguagem. 

Após a validação, o JSON será transformado em uma estrutura de dados na forma de objetos Python, como PatientRecord, PatientInfo, MedicalHistory, e Consultation. Essa conversão facilitará o acesso e a manipulação das informações do paciente.


### Gramática:

Valor -> Obj | Array | num | string |  ‘true’ |  ‘false’ |  ‘null’

Array -> ‘[‘ ListaValores ’]’

ListaValores -> Valor | Valor ‘,’ ListaValores | ‘ ’

Obj -> ‘{‘ Pares ‘}’

Pares -> Par | Par ‘,’ Pares | ‘ ’

Par -> string ‘:’ Valor

### Registro de Saúde Referenciado:

**(PatientInfo):**
Contém os dados pessoais do paciente, como nome, idade, gênero e um identificador único do paciente.

**(MedicalHistory):**
Consiste em uma lista de condições médicas que o paciente teve ou possui. Cada condição inclui o diagnóstico, a data em que foi diagnosticada e seu estado atual.

**(Consultation):**
Uma lista de consultas médicas que o paciente realizou, contendo a data da consulta, o médico responsável, os sintomas relatados e o diagnóstico fornecido.

### Parsing Expressions ( Estudo do Analisador Descendente Recursivo):

O **analisador descendente recursivo** é uma técnica simples e eficaz para a construção de parsers, que não requer ferramentas complexas. Essa abordagem permite que o código seja escrito de forma manual e direta, resultando em parsers rápidos e robustos, capazes de lidar com erros de maneira sofisticada. Implementações de linguagens consagradas, como GCC, utilizam essa técnica devido à sua eficácia.


O funcionamento do analisador descendente é baseado em regras gramaticais, onde cada regra é traduzida em uma função. As regras são processadas de cima para baixo, começando pela regra mais externa (como uma expressão) e descendo até as subexpressões. Essa estrutura é chamada de "descendente" porque o parser caminha pela gramática, utilizando chamadas recursivas para funções que representam regras não-terminais.
