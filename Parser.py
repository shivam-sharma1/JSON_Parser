import re

class JSONTokenizer:
    def __init__(self, json_str):
        self.json_str = json_str
        self.position = 0
        self.tokens = []

        # Define regex patterns for JSON tokens
        self.patterns = {
            'STRING': r'"(.*?)"',  # Matches strings like "..."
            'NUMBER': r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?',  # Matches integers or floats
            'TRUE': r'\btrue\b',
            'FALSE': r'\bfalse\b',
            'NULL': r'\bnull\b',
            'LBRACE': r'\{',
            'RBRACE': r'\}',
            'LBRACKET': r'\[',
            'RBRACKET': r'\]',
            'COLON': r':',
            'COMMA': r',',
            'WHITESPACE': r'\s+',  # Match whitespaces but discard them
        }

        self.token_types = {v: k for k, v in self.patterns.items()}

    def tokenize(self):
        while self.position < len(self.json_str):
            match = None

            for token_type, pattern in self.patterns.items():
                regex = re.compile(pattern)
                match = regex.match(self.json_str, self.position)

                if match:
                    value = match.group(0)
                    self.position = match.end()

                    if token_type != 'WHITESPACE':  # Ignore whitespace
                        self.tokens.append((token_type, value))

                    break

            if not match:
                raise ValueError(f"Unexpected character at position {self.position}: {self.json_str[self.position]}")
        
        return self.tokens

class JSONParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        else:
            return None  # Out of bounds

    def next_token(self):
        self.current_token_index += 1
        return self.current_token()

    def parse(self):
        return self.parse_value()

    def parse_value(self):
        token = self.current_token()

        if token is None:
            raise SyntaxError("Unexpected end of input")

        token_type, value = token

        if token_type == 'LBRACE':  # '{'
            return self.parse_object()
        elif token_type == 'LBRACKET':  # '['
            return self.parse_array()
        elif token_type == 'STRING':
            self.next_token()
            return value.strip('"')
        elif token_type == 'NUMBER':
            self.next_token()
            if '.' in value or 'e' in value or 'E' in value:
                return float(value)
            else:
                return int(value)
        elif token_type == 'TRUE':
            self.next_token()
            return True
        elif token_type == 'FALSE':
            self.next_token()
            return False
        elif token_type == 'NULL':
            self.next_token()
            return None
        else:
            raise SyntaxError(f"Unexpected token {value}")

    def parse_object(self):
        obj = {}
        self.next_token()  # Skip '{'
        
        if self.current_token()[0] == 'RBRACE':  # Empty object case
            self.next_token()  # Skip '}'
            return obj

        while True:
            key = self.parse_value()  # Parse key (should be a string)
            if self.current_token()[0] != 'COLON':
                raise SyntaxError("Expected ':' after key in object")
            self.next_token()  # Skip ':'
            value = self.parse_value()  # Parse value

            obj[key] = value

            if self.current_token()[0] == 'COMMA':
                self.next_token()  # Skip ','
            elif self.current_token()[0] == 'RBRACE':
                self.next_token()  # Skip '}'
                break
            else:
                raise SyntaxError(f"Unexpected token in object: {self.current_token()}")

        return obj

    def parse_array(self):
        arr = []
        self.next_token()  # Skip '['

        if self.current_token()[0] == 'RBRACKET':  # Empty array case
            self.next_token()  # Skip ']'
            return arr

        while True:
            arr.append(self.parse_value())

            if self.current_token()[0] == 'COMMA':
                self.next_token()  # Skip ','
            elif self.current_token()[0] == 'RBRACKET':
                self.next_token()  # Skip ']'
                break
            else:
                raise SyntaxError(f"Unexpected token in array: {self.current_token()}")

        return arr

# if __name__ == "__main__":
#     json_string = '{"name": "John", "age": 30, "isStudent": false, "courses": ["Math", "Physics"]}'

#     tokenizer = JSONTokenizer(json_string)
#     tokens = tokenizer.tokenize()

#     parser = JSONParser(tokens)
#     parsed_object = parser.parse()

#     print(parsed_object)
#     # Output: {'name': 'John', 'age': 30, 'isStudent': False, 'courses': ['Math', 'Physics']}
