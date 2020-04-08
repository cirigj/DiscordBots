class MessageHelper:
    def __init__(self):
        self.message = ''

    def write(self, str):
        self.message += str

    async def send(self, ctx, raw=True):
        bookend = '' if raw else '```'
        message_lines = self.message.split('\n')
        message = ''
        while len(message_lines) > 0:
            new_message = message + f'\n{message_lines[0]}'
            if len(new_message) >= 1990:
                await ctx.send(f'{bookend}{message}{bookend}')
                message = ''
            message = message + f'\n{message_lines[0]}'
            message_lines.pop(0)
        await ctx.send(f'{bookend}{message}{bookend}')