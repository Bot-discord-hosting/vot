import discord



class Btn(discord.ui.Button):
    def __init__(self, options, i, used, counting):
        super().__init__(style=discord.ButtonStyle.blurple, label=options[i], custom_id=str(i))
        self.used = used
        self.counting = counting
        self.options = options
        self.i = i
    

    async def callback(self, interaction: discord.Interaction):
        if interaction.user in self.used:
            return await interaction.response.send_message("You've already voted", ephemeral=True)

        self.used.append(interaction.user)

        if not self.options[self.i] in self.counting:
            self.counting[self.options[self.i]] = 1
        else:
            self.counting[self.options[self.i]] += 1
        
        await interaction.response.send_message(f"You chose **{self.options[self.i]}**", ephemeral=True)


class votingView(discord.ui.View):
    def __init__(self, timeout, options, interaction):
        super().__init__(timeout=timeout)
        self.options = options
        self.interaction = interaction
        self.used = []
        self.counting = {}

        for i in range(len(self.options)):
            button = Btn(options=options, i=i, used=self.used, counting=self.counting)
            self.add_item(button)
        
    async def on_timeout(self):
        largest = 0
        winners = []

        for key, value in self.counting.items():
            if value > largest:
                largest = value
                winners.clear()
                winners.append(f"**{key}** Votes: [ `{value}` ]")
            elif value < largest:
                continue
            elif value == largest:
                winners.append(f"**{key}** Votes: [ `{value}` ]")

        embed = discord.Embed(title="Voting Results:", color=discord.Color.dark_gold())
        embed.description = "\n".join(x for x in winners)
        await self.interaction.edit_original_response(embed=embed, view=None)