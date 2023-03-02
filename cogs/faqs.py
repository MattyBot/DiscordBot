import discord
from discord import app_commands, ui,  Interaction, Embed, SelectOption, Color
from discord.ext import commands
from matty_db import Database
from modals import AddFaqModal



class FAQCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()


    @app_commands.command(name="addfaq", description="Add a question & answer to FAQs")
    async def addfaq(self, interaction: Interaction):
        await interaction.response.send_modal(AddFaqModal())


    @app_commands.command(name="clearallfaq", description="Clear all FAQs from the database")
    async def clearallfaq(self, interaction: Interaction):
        self.db.query("DELETE FROM faqs_db")
        embed = Embed(title="Clear all FAQs", description="Success! All FAQs have been cleared from the database", color=Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="deletefaq", description = "Delete a FAQ from the database")
    async def deletefaq(self, interaction: discord.Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=ViewFaqView(server_id, call='delete'), ephemeral=True)


    @app_commands.command(name="listfaq", description="View a list of all FAQs")
    async def listfaq(self, interaction: Interaction):
        server_id = interaction.guild_id
        rows = self.db.query_fetch("SELECT question FROM faqs_db WHERE server_id = ?", (server_id,))
        if rows:
            embed = Embed(title="List of all FAQ", description="To see all FAQs, type command **/viewFAQ**", color = Color.orange())
            count = 1
            for row in rows:
                question = row[0]
                embed.add_field(name=f"{count} - {question}", value="\n", inline= False)
                count += 1
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed2 = Embed(title="List of all FAQ", description ="There are currently no FAQ", color=Color.orange())
            await interaction.response.send_message(embed=embed2, ephemeral=True)


    @app_commands.command(name="viewfaq", description="View all FAQs")
    async def viewfaq(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=ViewFaqView(server_id, call='view'), ephemeral=True)
        

class ViewFaqMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call

        rows = self.db.query_fetch("SELECT question, faq_id FROM faqs_db WHERE server_id = ?", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no FAQ", value="none")] 

        if call == 'view':
            super().__init__(placeholder="Select a question to view the answer", options=options)
        else: 
            super().__init__(placeholder="Select an FAQ to delete", options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        selection = self.db.query_fetch("SELECT question, answer, creator, datecreated FROM faqs_db WHERE faq_id = ?", (self.values[0],))

        if selection:
            question = selection[0][0]
            answer = selection[0][1]
            creator = selection[0][2]
            datecreated = selection[0][3]
            if self.call == 'view':
                embed = Embed(title=question, description=answer, color=Color.orange())
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)
            else: 
                self.db.query("DELETE FROM faqs_db WHERE faq_id = ?", self.values[0])
                await interaction.response.send_message(content="FAQ deleted!", ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)


class ViewFaqView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(ViewFaqMenu(server_id, call))



async def setup(client: commands.Bot) -> None:
    await client.add_cog(FAQCommands(client))