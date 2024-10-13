import re
class Token:
  def __init__(self, type, lexeme, value, position, line, column):
      self.type = type  # tipo do token, os citados na especificação, como número, string, '{}', ...
      self.lexeme = lexeme  # lexema original do token
      self.value = value  # valor do token
      self.position = position  # posição do token na string de entrada para representar os erros
      self.line = line # a linha do token no json
      self.column = column # a coluna do token no json
  def __repr__(self):
      return f"Token(tipo='{self.type}', lexema='{self.lexeme}', valor={self.value}, posição={self.position}, linha={self.line}, coluna={self.column})"

class LexerError(Exception):
    def __init__(self, position, message, line, column):
        super().__init__(f"Erro Léxico na linha {line}, coluna {column} (posição {position}): {message}")
        self.position = position
        self.line = line
        self.column = column

class Lexer:
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),  # números inteiros ou decimais
        ('STRING', r'"([^"\\]|\\.)*"'),  # strings em aspas duplas
        ('TRUE', r'true'),  # identificador true
        ('FALSE', r'false'),  # identificador false
        ('NULL', r'null'),  # identificador null
        ('LBRACE', r'\{'),  # abertura das chaves {
        ('RBRACE', r'\}'),  # fechamento das chaves }
        ('LBRACKET', r'\['),  # abertura dos colchetes [
        ('RBRACKET', r'\]'),  # fechamento dos colchetes ]
        ('COLON', r':'),  # delimitador de valor
        ('COMMA', r','),  # separador de valores
        ('WHITESPACE', r'\s+'),  # espaços em branco
        ('MISMATCH', r'.')  # outros caracteres
    ]

    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

    def __init__(self, json_string):
        self.json_string = json_string
        self.current_position = 0
        self.line = 1
        self.column = 1
        self.stack = []  # para rastrear chaves e colchetes

    def generate_tokens(self):
        tokens = []
        last_token_type = None  # para rastrear o tipo do último token
        last_token = None  # para armazenar o último token gerado

        for match in re.finditer(self.token_regex, self.json_string):
            type = match.lastgroup
            lexeme = match.group()
            start = match.start()
            end = match.end()

            if type == 'WHITESPACE':
                self._update_position(lexeme)
                continue
            elif type == 'MISMATCH':
                raise LexerError(self.current_position, f"Caractere Inesperado '{lexeme}'", self.line, self.column)

            # verifica vírgulas e valores faltantes
            if type == 'COMMA':
                if last_token_type in {'COLON', 'COMMA', 'LBRACE', 'LBRACKET', None}:
                    raise LexerError(self.current_position, "Vírgula inesperada", self.line, self.column)
            else:
                # verifica se a vírgula está faltando após um valor de objeto ou array fechado
                if last_token_type in {'RBRACE', 'RBRACKET'}:
                    if type not in {'COMMA', 'RBRACE', 'RBRACKET', None}:
                        raise LexerError(self.current_position, "Vírgula faltando após o fechamento de '}' ou ']'", self.line, self.column)

            # verifica falta de ':' após uma string que é chave
            if last_token_type == 'STRING':
                if type not in {'COLON', 'COMMA', 'RBRACE', 'RBRACKET', None}:
                    raise LexerError(self.current_position, "Faltando ':' após a chave", self.line, self.column)

            # verifica se um valor está faltando para uma chave
            if last_token_type == 'COLON':
                if type in {'COMMA', 'RBRACE', 'RBRACKET', None}:
                    raise LexerError(self.current_position, "Valor esperado após ':'", self.line, self.column)

            # verifica balanceamento de chaves e colchetes
            if type in {'LBRACE', 'LBRACKET'}:
                self.stack.append(type)
            elif type in {'RBRACE', 'RBRACKET'}:
                if not self.stack:
                    raise LexerError(self.current_position, f"Fechamento de {type} sem abertura correspondente", self.line, self.column)
                last_open = self.stack.pop()
                if (last_open == 'LBRACE' and type != 'RBRACE') or (last_open == 'LBRACKET' and type != 'RBRACKET'):
                    raise LexerError(self.current_position, f"Fechamento de {type} não corresponde ao último aberto", self.line, self.column)

            value = self.interpret_value(type, lexeme)
            token = Token(type, lexeme, value, start, self.line, self.column)
            tokens.append(token)
            self._update_position(lexeme)
            last_token_type = type
            last_token = token

        # verifica se ainda há chaves ou colchetes não fechados
        if self.stack:
            last_open = self.stack[-1]
            raise LexerError(self.current_position, f"{last_open} não foi fechado", self.line, self.column)

        return tokens

    def interpret_value(self, type, lexeme):
        if type == 'NUMBER':
            return float(lexeme) if '.' in lexeme else int(lexeme)
        elif type == 'STRING':
            return lexeme[1:-1]
        elif type == 'TRUE':
            return True
        elif type == 'FALSE':
            return False
        elif type == 'NULL':
            return None
        return None

    def _update_position(self, lexeme):
        lines = lexeme.splitlines()
        if len(lines) > 1:
            self.line += len(lines) - 1
            self.column = len(lines[-1]) + 1
        else:
            self.column += len(lexeme)
        self.current_position += len(lexeme)