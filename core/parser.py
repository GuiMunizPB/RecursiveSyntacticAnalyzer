class JSONParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def parse(self):
        return self.parse_value()

    def parse_value(self):
        if self.current_token.type == 'LBRACE':
            return self.parse_object()
        elif self.current_token.type == 'LBRACKET':
            return self.parse_array()
        elif self.current_token.type == 'STRING':
            value = self.current_token.value
            self.next_token()
            return value
        elif self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.next_token()
            return value
        elif self.current_token.type == 'TRUE':
            self.next_token()
            return True
        elif self.current_token.type == 'FALSE':
            self.next_token()
            return False
        elif self.current_token.type == 'NULL':
            self.next_token()
            return None
        else:
            raise Exception(f"Unexpected token {self.current_token}")

    def parse_object(self):
        self.next_token()  # Consumes '{'
        obj = {}
        while self.current_token and self.current_token.type != 'RBRACE':
            key = self.parse_value()
            if self.current_token.type != 'COLON':
                raise Exception(f"Expected ':' after key, got {self.current_token}")
            self.next_token()  # Consumes ':'
            value = self.parse_value()
            obj[key] = value
            if self.current_token.type == 'COMMA':
                self.next_token()  # Consumes ','
        self.next_token()  # Consumes '}'
        return obj

    def parse_array(self):
        self.next_token()  # Consumes '['
        array = []
        while self.current_token and self.current_token.type != 'RBRACKET':
            value = self.parse_value()
            array.append(value)
            if self.current_token.type == 'COMMA':
                self.next_token()  # Consumes ','
        self.next_token()  # Consumes ']'
        return array