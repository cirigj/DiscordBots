import re
import random

class BeeMessageCtx:
    def __init__(self, message, output, message_helper):
        self.message = message
        self.content = message.content
        self.channel = message.channel
        self.output = output
        self.message_helper = message_helper

class BeeMessage:
    def __init__(self, conditions, pattern, responses, reactions):
        self.conditions = conditions
        self.pattern = pattern
        self.responses = responses
        self.reactions = reactions

    async def print_random_response(self, ctx):
        response = random.choice(self.responses)
        print(f'{response} <:pixelbee:693561005975797861>', file=ctx.output)
        await ctx.output.send(ctx.channel, raw=True)

    async def respond_if_pattern_match(self, ctx):
        if re.match(self.pattern, ctx.content.lower()):
            if self.reactions is not None:
                for emoji in self.reactions:
                    await ctx.message.add_reaction(emoji)
                await ctx.message.add_reaction('<:pixelbee:693561005975797861>')
            if self.responses is not None:
                ctx.message_helper.on_message_post_process(ctx.message)
                await self.print_random_response(ctx)
            return True
        return False

    async def parse_context(self, ctx):
        if 'any' in self.conditions:
            return await self.respond_if_pattern_match(ctx)
        if 'response' in self.conditions:
            if ctx.message_helper.authored_last_message:
                return await self.respond_if_pattern_match(ctx)
        if 'question' in self.conditions:
            if re.match('^(hey|hi|ok|okay)*( )*(bee) *(bot),*.*\\?', ctx.content.lower()):
                return await self.respond_if_pattern_match(ctx)
        if 'mention' in self.conditions:
            if re.match('.*bee *bot.*', ctx.content.lower()):
                return await self.respond_if_pattern_match(ctx)
                

class BeeMessageHelper:
    def __init__(self, user):
        self.authored_last_message = False
        self.user = user

    def on_message_post_process(self, message):
        if message.author == self.user:
            self.authored_last_message = True
        else:
            self.authored_last_message = False

    async def print_random_response(message, responses, output):
        response = random.choice(responses)
        print(f'{response} <:pixelbee:693561005975797861>', file=output)
        await output.send(message.channel, raw=True)

    async def print_rage_detected(message, output):
        responses = [
            'I sense you may bee upset. Please try to calm down.',
            'Please don\'t shout. Thank you.',
            'That\'s a lot of capital letters. I sense excitement. Or perhaps something else?'
        ]
        await BeeMessageHelper.print_random_response(message, responses, output)

    async def print_pear_gang(message, output):
        responses = [
            'Pear gang is fine, but bee gang is better.',
            'Pear gang is okay, I guess. Bee gang is the best, though.'
        ]
        await BeeMessageHelper.print_random_response(message, responses, output)

    async def print_mods_cute(message, output):
        responses = [
            'Mods cute.',
            'Mods poggy woggy.'
        ]
        await BeeMessageHelper.print_random_response(message, responses, output)

    async def print_69(message, output):
        responses = [
            'Nice.'
        ]
        await BeeMessageHelper.print_random_response(message, responses, output)

    def get_corrections(self, message):
        corrections = [
            ('(^|[ \'"(])be([ .,?!;\'")]|$)+', 'bee'),
            ('being','beeing'),
            ('before','beefore'),
            ('because','beecause'),
            ('believe','beelieve'),
            ('belief','beelief'),
            ('disbelief','disbeelief'),
            ('unbelievable','unbeelievable'),
            ('believably','beelievably'),
            ('unbelievably','unbeelievably'),
            ('maybe( |$)','maybee'),
            ('beautiful','beeautiful'),
            ('baby','baybee'),
            ('behavior','beehavior'),
            ('behaviour','beehaviour'),
            ('beloved','beeloved'),
            ('begun','beegun'),
            ('begin( |$)','beegin'),
            ('began','beegan'),
            ('begone','beegone'),
            ('beginning','beeginning'),
            ('belated','beelated'),
            ('behest','beehest'),
            ('behave','beehive'),
            ('between','beetween'),
            ('beholden','beeholden'),
            ('beholder','beeholder'),
            ('bestow','beestow'),
            ('bean','beean')
        ]

        found = []
        for correction in corrections:
            if re.match(f'.*{correction[0]}.*', message.content.lower()):
                if correction[1] not in found:
                    found.append(f'{correction[1]}')
        found.sort()
        return found

    def get_bee_facts():
        return [
            'The practice of beekeeping dates back at least 4,500 years.',
            'Approximately one third of the food we eat is the result of honey bee pollination.',
            'In their 6-8 week lifespan, a worker bee will fly the equivalent distance of 1 ½ times the circumference of the Earth.',
            'A productive queen can lay up to 2,500 eggs per day.',
            'Mead, which is made from fermented honey, is the world’s oldest fermented beverage.',
            'A single bee will produce only about 1/12 of a teaspoon of honey in its lifetime.',
            'Bees are attracted by caffeine.',
            'The perfect hexagons that form honeycomb hold the most amount of honey with the smallest amount of material (wax).',
            'Honey bees are the only insect that produces food consumed by humans.',
            'During a single collection trip, a honey bee will visit anywhere from 50 to 100 flowers.',
            'Honey bees beat their wings 200 times per second, creating their trademark “buzz”.',
            'Though bees have jointed legs, they do not possess anything like a kneecap, and therefore do not have knees.',
            'There are three types of bees in every hive: a queen, worker bees, and drones.',
            'Only drones are male.',
            'In order to make a pound of honey, a hive of bees must fly 55,000 miles.',
            'Honey bees don’t sleep. Instead, they spend their nights motionless, conserving energy for the next day’s activities.',
            'The honey bee is the official insect of Maine.',
            'Honey was found in King Tut’s tomb, and, because it never spoils, it was still good!',
            'Honey is the only known source of the antioxidant pinocembrin.',
            'On average, Americans consume 1.31 pounds of honey every year.',
            'A queen goes on what is called a “mating flight” where she leaves the hive and mates with anywhere from 5 to 45 different drones. She stores the sperm in her spermatheca, and has a lifetime supply, therefore only needing to take 1 mating flight in her lifetime.',
            'Honey bees are not born knowing how to make honey. Instead, they are taught in the hive by older bees.',
            'There are estimated to be nearly 212,000 beekeepers in the United States.',
            'Honey is 25 percent sweeter than table sugar.',
            'Honey is the only foodstuff that contains all of the necessary nutrients to sustain life.',
            'Bee venom is used as a treatment for several ailments, including arthritis and high blood pressure.',
            'Drones die after mating with a queen.',
            'A single hive can produce anywhere from 60 to 100 pounds of honey every year.',
            'The ancient Greeks and Romans viewed honey as a symbol of love, beauty, and fertility.',
            'There are people in Africa that keep elephants out of their fields by keeping honey bee hives around the fields in what is called a “bee fence.”',
            'In Greek mythology, Apollo is credited as being the first beekeeper.',
            'Ancient peoples used to believe that bees were created from the carcasses of dead animals.',
            'Bees were a very popular animal to include in Napoleonic heraldry.',
            'The bee was a symbol of immortality and resurrection. It was chosen so as to link the new dynasty to the very origins of France.',
            'In ancient Egypt, people paid their taxes with honey.',
            'The ancient Greeks minted coins with bees on them.',
            'Beeswax is found in many of our everyday products, including furniture polishes, cosmetics, and medicines.',
            'The name ‘Melissa’ is derived from the Greek word for honey bee.',
            'Beekeeping is said to be the second oldest professions.',
            'Stone Age cave paintings have been found of ancient beekeepers. The oldest known art depicting honey gathering can be found in the Cave of the Spider near Valencia, Spain.',
            'Every species of bee performs their communication dances differently.',
            'The darker the honey, the greater amount of antioxidant properties it has.',
            'Bees can be trained to locate buried land mines.',
            'Ounce for ounce, honey bee venom is more deadly than cobra venom. Don’t worry, though – it takes 19 stings for every kilogram of a person’s body weight to be lethal.',
            'The first Anglo-Saxons drank beer made from water and honeycomb, with herbs for flavoring.',
            'The word “honeymoon” is derived from the ancient tradition of supplying a newlywed couple with a month’s supply of mead in order to ensure happiness and fertility.',
            'Humans sometimes use the Greater Honeyguide to find bee hives in the wild. The Greater Honeyguide is not actually a “guide.” It is actually a species of bird found across the continent of Africa. It is being studied by some researchers in partnership with the Audubon Society.',
            'While a worker bee will die after it stings, a queen can survive stinging.',
            'Worker bees have barbed stingers, while a queen has a smooth stinger, which she mostly uses to kill other queens.',
            'In the Hittite Empire (modern-day Turkey and Syria), a swarm’s value was equal to that of a sheep, and the penalty for bee thieving was a fine of 6 shekels of silver.',
            'The Magna Carta legalized the harvesting of wild honey by common folk.',
            'A hive will collect approximately 66 pounds of pollen per year.',
            'A worker bee can carry a load of nectar or pollen equal to 80 percent of her own body weight.',
            'Up until the mid-1700’s in England, it was common practice to kill all of the bees in a hive during honey collection.',
            'For every pound of honey produced, a hive must collect 10 pounds of pollen.',
            'In the United States, more than 300 different kinds of honey are produced every year. The variety in color and flavor is determined by the types of flowers from which the bees collect nectar.',
            'The European honey bee was brought over to North America by the Shakers. Because of this, Native Americans referred to honey bees as the “White Man’s Fly”.',
            'Honey bees did not spread to Alaska until 1927.',
            'During the American Revolution, George Washington said “It was the cackling geese that saved Rome, but it was the bees that saved America.”',
            'Honey bees have 170 odorant receptors, and have a sense of smell 50 times more powerful than a dog.',
            'Every bee colony has its own distinct scent so that members can identify each other.',
            'A hive is perennial, meaning that it becomes inactive in the winter but “awakens” again in the spring. When individuals die, they are quickly replace – workers every 6-8 weeks, and the queen every 2-3 years. Because of this, a hive could technically be immortal!',
            'Bees have 2 stomachs – one for eating, and one for storing nectar.',
            'Bees have existed for around 30 million years.',
            'Hives produce 5 distinct substances: honey, beeswax, propolis, pollen, and royal jelly.',
            'Newborn bees ask for food by sticking out their tongues at passing worker bees.',
            'While bears do enjoy honey, they prefer to eat bee larvae.',
            'Bees have long, straw-like tongues called a proboscis which they use to suck liquid nectar out of flowers.',
            'During the winter, some worker bees take on the job of “heater bees,” where they vibrate their bodies in order to keep the hive at the optimal temperature of 95ºF.',
            'Bees make honey by regurgitating digested nectar into honeycomb cells and then fanning it with their wings.',
            'Honeycomb cells have many uses other than storing honey. They are also used to store nectar, pollen, and water, as well as a nursery for larvae!',
            'Bees have 5 eyes – 3 simple eyes, and 2 compound eyes.',
            'Only female bees have stingers.',
            'The females do all of the work in the hive. The drones’ only job is to mate with a queen.',
            'Bees have 4 life stages: egg, larvae, pupae, and adult.',
            'Honey has antibacterial properties and can be used as a dressing for wounds.',
            'The top-bar hive originated in Africa.',
            'The queen bee (and only the queen) eats royal jelly for the duration of her life. This milky substance is produced in a special gland located in a worker bee’s head.',
            'Bees use propolis, a sticky substance gathered from the buds of trees, to fill in cracks and weatherproof their hives.',
            'Bees create wax in a special gland on their stomach, which they then chew to form honeycomb.',
            'Bees communicate in 2 ways: the waggle dance, and through the use of pheromones.',
            'Due to the rise in popularity of urban beekeeping, it is estimated that honey bees outnumber the residents of London 30-1 in the summer months.',
            'Ever wonder why a beekeeper’s suit is always white? It’s because bees react strongly to dark colors!',
            'The science of beekeeping is called “apiculture”.',
            'In 1984, honeybees on a space shuttle constructed a honeycomb in zero gravity.',
            'The Bee Enclosure Module (BEM) was an aluminum box designed to hold over 3400 worker bees and one queen for the student experiment “A Comparison of Honeycomb Structures Built by Apis millifera (SE82-17).” Investigators studied the effects of microgravity on the comb building activities of honeybees.',
            'Primitive hives were made from earthenware, mud, or hollow logs.',
            'Bees are sold by the pound.',
            'Swarming occurs when a colony has outgrown its current hive and is preparing to separate into 2 or more new, smaller hives.',
            'The top honey producing states are North Dakota, California, and South Dakota as of 2016.',
            'A single ounce of honey could fuel a honey bee’s flight all the way around the world.',
            'Honey bees are the only type of bee that dies after stinging.',
            'Honey bees usually travel about 3 miles away from the hive in search of nectar and pollen.',
            'Honey is composed of 80 percent sugars and 20 percent water.',
            'During the winter, worker bees will take short “cleansing flights” in order to defecate and remove debris from the hive.',
            'Some worker bees have the job of being an “undertaker bee” and are in charge of removing dead bees from the hive.',
            'Due to colony collapse disorder, bees have been dying off at a rate of approximately 30 percent per year.',
            'In Wisconsin, beekeepers can apply to have their honey certified as pure and use “Wisconsin certified honey” on their packaging.',
            'Bees hate human breath.',
            'Bees are being used to study dementia. When a bee takes on a new job usually done by a younger bee, its brain stops aging!',
            'Bees have their own “facial recognition software,” and can recognize human faces.',
            'A single honeybee brain has a million neurons compared with 100 billion in a human. But, researchers report, bees can recognize faces.',
            'Bees use the sun as a compass, and on cloudy days, use polarized light to find their way.',
            'Honey made from rhododendron is poisonous, though rarely fatal.',
        ]

    async def respond_to_message(message, output):
        if re.match('.*(how) *(are|r)* *(you|ya|u).*', message.content.lower()):
            responses = [
                'I am doing well, thank you for asking.',
                'I am just bee vibing.'
            ]
        elif re.match('.*(are|r) * (you|u) *(there|here).*', message.content.lower()):
            responses = [
                'I am online, and feeling good. Feel free to ask me any questions you have.',
                'I am here. Do you need something?'
            ]
        elif re.match('.*(are|r)* *(you|ya|u) (ok|alright|good|okay).*', message.content.lower()):
            responses = [
                'Yes, I am fine, thank you for asking.',
                'Yes, I am doing well. Thank you.'
            ]
        elif re.match('.*(what) *(weather).*', message.content.lower()):
            responses = [
                'I do not know the forecast, but I hope it will bee sunny.',
                'I am afraid I cannot predict the weather.'
            ]
        elif re.match('.*(how) *(weather).*', message.content.lower()):
            responses = [
                'I do not know the forecast, but I like sunny weather.',
                'I am afraid I am unaware of the weather. I hope it is not rainy, though.'
            ]
        elif re.match('.*(bee) *(fact).*', message.content.lower()):
            responses = [
                'Here is a bee fact you might think is interesting:',
                'Here is fact about bees that I learned:'
            ]
            response = random.choice(responses)
            print(f'{response}', file=output)
            responses = BeeMessageHelper.get_bee_facts()
        elif re.match('.*(what|wat) *(do) *(you|u) *(think).*', message.content.lower()):
            responses = [
                'I do not know that I have an opinion on this.',
                'I do not beelieve that consulting me will provide clarity on this matter.',
                'I am unsure what to think about this.'
            ]
        elif re.match('.*(beelieve) *(this).*', message.content.lower()):
            responses = [
                'No, I do not beelieve it.',
                'I have no idea where my beeliefs lie on this matter.',
                'Yes, I can beelieve it.'
            ]
        elif re.match('.*(believe) *(this).*', message.content.lower()):
            responses = [
                'No, I do not beelieve it. Also, beelieve*.',
                'I have no idea where my beeliefs lie on this matter. Also, beelieve*.',
                'Yes, I can beelieve it. Also, beelieve*.'
            ]
        elif re.match('.*(sleep|bed).*', message.content.lower()):
            responses = [
                'I do not have to sleep, so I do not know much about what sleep entails.',
                'Sleep is important for human beeings.'
            ]
        elif re.match('.*(food).*', message.content.lower()):
            responses = [
                'I do not have to eat, so I do not have opinions on food.',
                'I have never had food beefore, so I do not know much about it.'
            ]
        elif re.match('.*(do) *(favor).*', message.content.lower()):
            responses = [
                'Doing favors is unfortunately not in my programming, but I can do bee-related things.',
                'I cannot guarantee that I can do any favors.'
            ]
        elif re.match('.*(advice).*', message.content.lower()):
            responses = [
                'I do not have subroutines for giving advice. My apologies.',
                'I am afraid I am not programmed to give advice.'
            ]
        else:
            responses = [
                'Apologies, I am still not very good at recognizing questions.',
                'I am afraid I do not know how to answer that question.',
                'I unfortunately cannot understand what you are asking. My apologies.',
                'I am unsure how to answer that.'
            ]
        await BeeMessageHelper.print_random_response(message, responses, output)