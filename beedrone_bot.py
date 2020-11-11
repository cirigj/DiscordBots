#invite link: https://discordapp.com/oauth2/authorize?client_id=675234599504445441&scope=bot&permissions=3072

from discord.ext import commands
from pprint import pprint
import re
import asyncio
import yaml
from source.bot_utils.parsing_utils import ParserUtils
from source.bot_utils.message_utils import MessageHelper
from source.bot_utils.run_utils import RunUtils
from source.beebot.bee_message import BeeMessageHelper, BeeMessage, BeeMessageCtx

import sys

prefix = '!'
bot = commands.Bot(command_prefix=prefix)

bot.remove_command('help')

@bot.event
async def on_ready():
    print("\nBee Bot, reporting for duty!\n")
    bot.bee_message = BeeMessageHelper(bot.user)
    bot.realtalk_mode = False
    bot.parser_utils = ParserUtils()
    bot.pear_gang_recent = False
    bot.mods_cute_recent = False

@bot.command(aliases=['e'])
async def echo(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nECHO command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()

    pos_args = ['msg']

    args = bot.parser_utils.parse_arguments(raw_args, pos_args)
    if args is None:
        print(f'Error parsing ECHO command!', file=output)
        await output.send(ctx)
        return

    msg = args['pos']['msg']

    print(msg, file=output)

    await output.send(ctx)

@bot.command(aliases=['h'])
async def help(ctx):
    message = ctx.message.content
    print(f'\nHELP command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()

    print('Help command coming soon! Thanks for using Bee Bot! <:pixelbee:693561005975797861>', file=output)

    await output.send(ctx.author, raw=True)

@bot.command(aliases=['rt'])
async def realtalk(ctx):
    message = ctx.message.content
    print(f'\nREALTALK command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()

    if bot.realtalk_mode:
        print('Realtalk mode is already active.', file=output)
    else:
        bot.realtalk_mode = True
        print('Realtalk mode activated. "be" to "bee" interjections supressed.', file=output)

    await output.send(ctx)

@bot.command(aliases=['rto'])
async def realtalkoff(ctx):
    message = ctx.message.content
    print(f'\nREALTALKOFF command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()

    if bot.realtalk_mode:
        bot.realtalk_mode = False
        print('Realtalk mode deactivated. Resuming obnoxious interjections.', file=output)
    else:
        print('Realtalk mode is already off.', file=output)

    await output.send(ctx)

@bot.command(aliases=['re'])
async def restrictemoji(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nRESTRICTEMOJI command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()

    pos_args = ['emoji']

    args = bot.parser_utils.parse_arguments(raw_args, pos_args)
    if args is None:
        print(f'Error parsing command!', file=output)
        await output.send(ctx)
        return

    e = args['pos']['emoji']

    for emoji in ctx.message.guild.emojis:
        if str(emoji) == e:
            for role in ctx.message.guild.roles:
                if role.id == 694665193019408404:
                    print('HIT')
                    await emoji.edit(roles=[])

    #await output.send(ctx)

def on_message_post_process(message):
    if message.author == bot.user:
        bot.bee_message.authored_last_message = True
    else:
        bot.bee_message.authored_last_message = False

async def pear_gang_cooldown():
    bot.pear_gang_recent = True
    await asyncio.sleep(600)
    bot.pear_gang_recent = False

async def mods_cute_cooldown():
    bot.mods_cute_recent = True
    await asyncio.sleep(600)
    bot.mods_cute_recent = False

@bot.event
async def on_message(message):
    if message.author == bot.user:
        on_message_post_process(message)
        return

    await bot.process_commands(message)

    if bot.realtalk_mode:
        return

    output = MessageHelper()

    ctx = BeeMessageCtx(message, output, bot.bee_message)
    for command in bot.beebot_commands:
        if await command.parse_context(ctx):
            return

    if bot.bee_message.authored_last_message:
        if re.sub(r'\W+', '', message.content).isupper():
            on_message_post_process(message)
            await BeeMessageHelper.print_rage_detected(message, output)
            return
        elif re.match('^(ugh).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessageHelper.print_disapproval_detected(message, output)
            return

    if re.match('^(hey|hi|ok|okay)*( )*(bee) *(bot),*.*\\?', message.content.lower()):
        on_message_post_process(message)
        await BeeMessageHelper.respond_to_message(message, output)
        return

    if re.match('.*bee *bot.*', message.content.lower()):
        if re.sub(r'\W+', '', message.content).isupper():
            on_message_post_process(message)
            await BeeMessageHelper.print_rage_detected(message, output)
            return

    if re.match('.*69.*', message.content.lower()) and not re.match('.*<.*69.*>.*', message.content.lower()):
        on_message_post_process(message)
        await BeeMessageHelper.print_69(message, output)
        return

    if re.match('.*(pear) *(gang).*', message.content.lower()) and not bot.pear_gang_recent:
        on_message_post_process(message)
        await BeeMessageHelper.print_pear_gang(message, output)
        await pear_gang_cooldown()
        return

    if re.match('.*( |^)(mods)( |$).*', message.content.lower()) and not bot.pear_gang_recent:
        on_message_post_process(message)
        await BeeMessageHelper.print_mods_cute(message, output)
        await mods_cute_cooldown()
        return

    found_corrections = bot.bee_message.get_corrections(message)
    if found_corrections != []:
        print(', '.join(found_corrections) + '* <:pixelbee:693561005975797861>', file=output)
    else:
        on_message_post_process(message)
        return

    on_message_post_process(message)

    await output.send(message.channel)

def main():
    commands_file = sys.argv[1]

    bot.beebot_commands = []

    with open(commands_file, 'r') as commands:
        raw_commands = yaml.load(commands, Loader=yaml.FullLoader)
        for raw_command in raw_commands:
            if 'reactions' not in raw_command:
                raw_command['reactions'] = None
            if 'responses' not in raw_command:
                raw_command['responses'] = None
            try:
                bot.beebot_commands.append(BeeMessage(raw_command['conditions'], raw_command['pattern'], raw_command['responses'], raw_command['reactions']))
            except e:
                print(f"Malformed command detected in yaml file. {e}")

    bot.run(RunUtils().GetToken('beebot'))

if __name__ == '__main__':
    main()