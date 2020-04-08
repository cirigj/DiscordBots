import yaml
import io

token_file = ".secret/bot_tokens.yaml"

class RunUtils:
    def __init__(self):
        with open(token_file, 'r') as tokens_file:
            self.tokens = yaml.load(tokens_file, Loader=yaml.BaseLoader)

    def GetToken(self, key):
        if key in self.tokens:
            return self.tokens[key]
        else:
            print(f'Unknown bot token key "{key}"')
            return None
