#invite link: https://discordapp.com/oauth2/authorize?client_id=675234599504445441&scope=bot&permissions=3072

from discord.ext import commands
from pprint import pprint
import re
import asyncio
from source.bot_utils.parsing_utils import ParserUtils
from source.bot_utils.message_utils import MessageHelper
from source.bot_utils.run_utils import RunUtils
from source.beebot.bee_message import BeeMessage

import sys

prefix = '!'
bot = commands.Bot(command_prefix=prefix)

bot.remove_command('help')

@bot.event
async def on_ready():
    print("\nBee Bot, reporting for duty!\n")
    bot.realtalk_mode = False
    bot.parser_utils = ParserUtils()
    bot.authored_last_message = False
    bot.pear_gang_recent = False

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

def on_message_post_process(message):
    if message.author == bot.user:
        bot.authored_last_message = True
    else:
        bot.authored_last_message = False

async def pear_gang_cooldown():
    bot.pear_gang_recent = True
    await asyncio.sleep(600)
    bot.pear_gang_recent = False

@bot.event
async def on_message(message):
    if message.author == bot.user:
        on_message_post_process(message)
        return

    await bot.process_commands(message)

    if bot.realtalk_mode:
        return

    output = MessageHelper()

    if bot.authored_last_message:
        if re.match('.*(ily|ilu|love|luv|good).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_love(message, output)
            return
        elif re.match('.*(thank|thx|thnx).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_thumbsup(message, output)
            return
        elif re.sub(r'\W+', '', message.content).isupper():
            on_message_post_process(message)
            await BeeMessage.print_rage_detected(message, output)
            return
        elif re.match('.*(sorry|sry).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_apology_detected(message, output)
            return
        elif re.match('^(ugh).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_disapproval_detected(message, output)
            return

    if re.match('^(hey|hi|ok|okay)*( )*(bee) *(bot),*.*\\?', message.content.lower()):
        on_message_post_process(message)
        await BeeMessage.respond_to_message(message, output)
        return

    if re.match('.*bee *bot.*', message.content.lower()):
        if re.match('.*(night|nini).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_goodnight(message, output)
            return
        elif re.match('.*(ily|ilu|love|luv|good).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_love(message, output)
            return
        elif re.match('.*(thank|thx|thnx).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_thumbsup(message, output)
            return
        elif re.sub(r'\W+', '', message.content).isupper():
            on_message_post_process(message)
            await BeeMessage.print_rage_detected(message, output)
            return
        elif re.match('.*(sorry|sry).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_apology_detected(message, output)
            return
        elif re.match('.*(despacito).*', message.content.lower()):
            on_message_post_process(message)
            await BeeMessage.print_despacito(message, output)
            return

    if re.match('.*bee *bot *cute.*', message.content.lower()):
        on_message_post_process(message)
        await BeeMessage.print_reverse(message, output)
        return

    if re.match('.*69.*', message.content.lower()) and not re.match('.*<(:.*:|@!).*69.*>.*', message.content.lower()):
        on_message_post_process(message)
        await BeeMessage.print_69(message, output)
        return

    if re.match('.*(pear) *(gang).*', message.content.lower()) and not bot.pear_gang_recent:
        on_message_post_process(message)
        await BeeMessage.print_pear_gang(message, output)
        await pear_gang_cooldown()
        return

    found_corrections = BeeMessage.get_corrections(message)
    if found_corrections != []:
        print(', '.join(found_corrections) + '* <:pixelbee:693561005975797861>', file=output)
    else:
        on_message_post_process(message)
        return

    on_message_post_process(message)

    await output.send(message.channel)

bot.run(RunUtils().GetToken('beebot'))