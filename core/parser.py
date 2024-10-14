class JSONParser:
    def __init__(self, tokens):
        self.tokens = tokens  # lista de tokens fornecida pelo analisador léxico
        self.current_token = None  
        self.next_token() 

    def next_token(self):
        # avança para o próximo token na lista
        if self.tokens:
            self.current_token = self.tokens.pop(0)  # pega o próximo token
        else:
            self.current_token = None  # se não houver mais tokens, define como None

    def parse(self):
        # começa o processo de parsing a partir de um valor, seja objeto, array, número, etc.
        return self.parse_value()

    def parse_value(self):
        # identifica o tipo do valor atual e chama a função de parsing correspondente
        if self.current_token.type == 'LBRACE':
            return self.parse_object()  # se encontrar '{', começa a parsear um objeto
        elif self.current_token.type == 'LBRACKET':
            return self.parse_array()  # se encontrar '[', começa a parsear um array
        elif self.current_token.type == 'STRING':
            # parseia uma string e avança para o próximo token
            value = self.current_token.value
            self.next_token()
            return value
        elif self.current_token.type == 'NUMBER':
            # parseia um número e avança para o próximo token
            value = self.current_token.value
            self.next_token()
            return value
        elif self.current_token.type == 'TRUE':
            # parseia um valor booleano 'true'
            self.next_token()
            return True
        elif self.current_token.type == 'FALSE':
            # parseia um valor booleano 'false'
            self.next_token()
            return False
        elif self.current_token.type == 'NULL':
            # parseia o valor nulo 'null'
            self.next_token()
            return None
        else:
            # se o token for inesperado, lança uma exceção
            raise Exception(f"Unexpected token {self.current_token}")

    def parse_object(self):
        # método para parsear um objeto JSON
        self.next_token()  # consome '{'
        obj = {}
        while self.current_token and self.current_token.type != 'RBRACE':
            key = self.parse_value()  # parseia a chave do objeto
            if self.current_token.type != 'COLON':
                raise Exception(f"Expected ':' after key, got {self.current_token}")
            self.next_token()  # consome ':'
            value = self.parse_value()  # parseia o valor associado à chave
            obj[key] = value  # adiciona o par chave-valor ao dicionário
            if self.current_token.type == 'COMMA':
                self.next_token()  # consome ',' para separar pares chave-valor
        self.next_token()  # consome '}'
        return obj  # retorna o dicionário representando o objeto

    def parse_array(self):
        # método para parsear um array JSON
        self.next_token()  # consome '['
        array = []
        while self.current_token and self.current_token.type != 'RBRACKET':
            value = self.parse_value()  # parseia o valor do array
            array.append(value)  # adiciona o valor à lista
            if self.current_token.type == 'COMMA':
                self.next_token()  # consome ',' para separar os elementos
        self.next_token()  # consome ']'
        return array  # retorna a lista representando o array
