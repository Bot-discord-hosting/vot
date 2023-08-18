import discord
from discord.ext import commands
from discord import app_commands, Interaction
from buttons.votingBtns import votingView
import sqlite3
conn = sqlite3.connect('levels.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS levels
             (user_id TEXT PRIMARY KEY, level INTEGER, exp INTEGER)''')

client = commands.Bot(command_prefix='a$', intents=discord.Intents.all())
tree = client.tree

@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"Synced {len(synced)} Command(s)")
    print(f"{client.user} is ready!")

@tree.command(name="vote", description="Create a new voting poll")
@app_commands.describe(title="title for the voting embed",
                       info="some info about this voting (Use / to make new line)",
                       options="Buttons under poll seperated by comma Ex: Test, Test 1, Test 2",
                       time="time in mins")
async def addPoll(interaction: Interaction, title: str, info: str, options: str, time: int):
    info = info.split('/')
    info = '\n'.join(x for x in info)
    
    embed = discord.Embed(title=title, description=info, color=discord.Color.dark_gold())
    embed.set_footer(text=f"{interaction.user} asked.")
    options = options.split(',')
    view = votingView(time * 3600, options, interaction)
    await interaction.response.send_message(embed=embed, view=view)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    c.execute('SELECT * FROM levels WHERE user_id=?', (user_id,))
    result = c.fetchone()

    if result is None:
        c.execute('INSERT INTO levels VALUES (?, ?, ?)', (user_id, 0, 0))
    else:
        exp = result[2] + 1
        level = result[1]
        if exp >= level * 100:
            exp = 0
            level += 1
            await message.channel.send(f'{message.author.mention} مستواك الجديد هو {level}!')
        c.execute('UPDATE levels SET level=?, exp=? WHERE user_id=?', (level, exp, user_id))

    conn.commit()
    await client.process_commands(message)


@client.command()
async def stats(ctx):
    user_id = str(ctx.author.id)
    c.execute('SELECT * FROM levels WHERE user_id=?', (user_id,))
    result = c.fetchone()

    if result is None:
        embed=discord.Embed(title="Levels", description="Show levels", color=0xdd0239)
        embed.add_field(name="Level", value="You hav not level now", inline=False)
        await ctx.send(embed=embed)
    else:
        level = result[1]
        exp = result[2]
        embed=discord.Embed(title="Levels", description="Show levels", color=0x0070df)
        embed.add_field(name="Level", value=f"***{level}***", inline=False)
        embed.add_field(name="Xp", value=f"***{exp}***", inline=True)
        await ctx.send(embed=embed)

@client.remove_command("help")
@tree.command(name="help", description="show commands")
async def help(interaction: Interaction):
    embed=discord.Embed(title="Help Command", description="show command of bot")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1093505126091735040/1112308803971584050/code-syntax-dark-minimal-4k-mr.jpg?width=375&height=250")
    embed.add_field(name="prefix", value="***!***", inline=True)
    embed.add_field(name="level", value="***stats***", inline=False)
    embed.add_field(name="Voting", value="/vote", inline=True)
    embed.set_footer(text="beata version")
    await interaction.response.send_message(embed=embed)



to = 'OTU2MTgyMTM5OTk1NTUzODQy'
kn = '0qdCpKEV1Wnulbl0rYXtEXeay8AWrbKpDQu9TE'
client.run(to +".GNUdJJ."+kn)
