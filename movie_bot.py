#invite link: https://discordapp.com/oauth2/authorize?client_id=675234599504445441&scope=bot&permissions=3072

from discord.ext import commands
from pprint import pprint
import re
import asyncio
import yaml
from source.bot_utils.parsing_utils import ParserUtils
from source.bot_utils.message_utils import MessageHelper
from source.bot_utils.run_utils import RunUtils

import sys

prefix = '!'
bot = commands.Bot(command_prefix=prefix)

bot.remove_command('help')

@bot.event
async def on_ready():
    bot.setup_done = False
    bot.parser_utils = ParserUtils()
    print("\nLoading Suggestions File...")
    with open(bot.output_file, 'r') as suggestions_file:
        bot.suggestions = yaml.load(suggestions_file, Loader=yaml.SafeLoader)
    if bot.suggestions is None:
        bot.suggestions = dict()
    print("\nProcessing Message History...")
    channel = bot.get_channel(bot.suggestion_channel_id)
    await parse_channel_messages(channel)
    print("\nMovie Bot Ready.\n")
    bot.setup_done = True

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

#@bot.command(aliases=['h'])
#async def help(ctx):
#    message = ctx.message.content
#    print(f'\nHELP command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
#
#    output = MessageHelper()
#
#    print('Help command coming soon!', file=output)
#
#    await output.send(ctx.author, raw=True)

async def parse_channel_messages(channel):
    messages = await channel.history(limit=200).flatten()
    for msg in messages:
        if message_is_suggestion(msg):
            await update_message(msg)

    write_to_file()

def write_to_file():
    with open(bot.output_file, 'w') as suggestions_file:
        yaml.dump(bot.suggestions, suggestions_file, Dumper=yaml.SafeDumper)

def message_is_suggestion(msg):
    return msg.channel.id == bot.suggestion_channel_id and re.match('^.*?s:.+', msg.content.lower())

async def update_message(msg):
    reactions = dict()
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
    interactions = 0
    for reaction in msg.reactions:
        if reaction.emoji == '👍':
            reactions['up'] = reaction.count
        elif reaction.emoji == '👎':
            reactions['down'] = reaction.count
        interactions += reaction.count
    reactions['interactions'] = interactions
    reactions['title'] = msg.content.split(':', 1)[1].split('\n', 1)[0].strip()
    suggestion_key = msg.id
    bot.suggestions[suggestion_key] = reactions

async def update_from_payload(payload):
    if payload.channel_id != bot.suggestion_channel_id:
        return
        
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if message_is_suggestion(message):
        await update_message(message)
        write_to_file()

async def wait_for_setup():
    while (not bot.setup_done):
        await asyncio.sleep(5)

def print_top_results(output):
    most_liked = []
    max_likes = 0
    best_rated = []
    max_rating = -1000
    most_interacted = []
    max_interactions = 0
    for suggestion in bot.suggestions:
        data = bot.suggestions[suggestion]

        if data['up'] > max_likes:
            most_liked = []
            max_likes = data['up']
        if data['up'] == max_likes:
            most_liked.append(data['title'])
        
        rating = data['up'] - data['down']
        if rating > max_rating:
            best_rated = []
            max_rating = rating
        if rating == max_rating:
            best_rated.append(data['title'])

        if data['interactions'] > max_interactions:
            most_interacted = []
            max_interactions = data['interactions']
        if data['interactions'] == max_interactions:
            most_interacted.append(data['title'])

    print('Here are the results:', file=output)
    print('Highest Rated:', file=output)
    for title in best_rated:
        print(f' - {title}', file=output)
    print('Most Upvotes:', file=output)
    for title in most_liked:
        print(f' - {title}', file=output)
    print('Most Interactions:', file=output)
    for title in most_interacted:
        print(f' - {title}', file=output)

@bot.command(aliases=['update'])
async def init(ctx):
    message = ctx.message.content
    print(f'\nINIT command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    if ctx.channel.id == bot.suggestion_channel_id:
        await parse_channel_messages(ctx.channel)
        
    await ctx.message.delete()

@bot.command(aliases=['r'])
async def results(ctx):
    message = ctx.message.content
    print(f'\nRESULTS command triggered! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()

    print_top_results(output)

    await output.send(ctx)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await wait_for_setup()

    await bot.process_commands(message)
    
    if message_is_suggestion(message):
        print('suggestion added')
        await update_message(message)
        write_to_file()

@bot.event
async def on_raw_message_edit(payload):
    await wait_for_setup()
    print('suggestion updated')
    await update_from_payload(payload)

@bot.event
async def on_raw_reaction_add(payload):
    await wait_for_setup()
    print('suggestion reaction added')
    await update_from_payload(payload)

@bot.event
async def on_raw_reaction_remove(payload):
    await wait_for_setup()
    print('suggestion reaction removed')
    await update_from_payload(payload)

def main():
    bot.suggestion_channel_id = int(sys.argv[1])
    bot.output_file = sys.argv[2]
    bot.run(RunUtils().GetToken('moviebot'))

if __name__ == "__main__":
    main()