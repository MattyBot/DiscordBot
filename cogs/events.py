import discord
from discord import app_commands, ui,  Interaction, Embed, SelectOption, Color
from discord.ext import commands
from matty_db import Database
from modals import AddEventModal



class EventCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = Database()


    @app_commands.command(name="addevent", description="Add a new event")
    async def addevent(self, interaction: Interaction):
        await interaction.response.send_modal(AddEventModal())


    @app_commands.command(name="clearallevents", description="Clear all events from the database")
    async def clearallevents(self, interaction: Interaction):
        self.db.query("DELETE FROM events_db")
        embed = Embed(title="Clear all events", description="Success! All events have been cleared from the database", color=Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="deleteevent", description = "Delete an event from the database")
    async def deleteevent(self, interaction: discord.Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=ViewEventsView(server_id, call='delete'), ephemeral=True)

    @app_commands.command(name="listevents", description="View a list of all events")
    async def listevents(self, interaction: Interaction):
        server_id = interaction.guild_id
        rows = self.db.query_fetch("SELECT event_name, date, time FROM events_db WHERE server_id = ?", (server_id,))
        if rows:
            embed = Embed(title="List of all events", description="For more information about an event, type command **/viewevents**", color = Color.orange())
            count = 1
            for row in rows:
                event_name = row[0]
                date = row[1]
                time = row[2]
                embed.add_field(name=f"{count}- {event_name}", value=f"{date} at {time}", inline= False)
                count += 1
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed2 = Embed(title="List of all events", description ="There are currently no events", color=Color.orange())
            await interaction.response.send_message(embed=embed2, ephemeral=True)


    @app_commands.command(name="viewevents", description="View all events")
    async def viewevents(self, interaction: Interaction):
        server_id = interaction.guild_id
        await interaction.response.send_message(view=ViewEventsView(server_id, call='view'), ephemeral=True)



class ViewEventsMenu(ui.Select):
    def __init__(self, server_id, call):
        self.db = Database()
        self.call = call
        rows = self.db.query_fetch("SELECT event_name, event_id FROM events_db WHERE server_id = ?", (server_id,))
        if rows:
            options = [SelectOption(label=row[0], value=row[1]) for row in rows]
        else:
            options = [SelectOption(label="There are currently no events", value="none")]  

        if call == 'view':
            super().__init__(placeholder="Select an event to view the event details", options=options)
        else: 
            super().__init__(placeholder="Select an event to delete", options=options)
    
    async def callback(self, interaction: Interaction):
        if self.values[0] == "none":
            await interaction.response.defer()
            return
        selection = self.db.query_fetch('''
            SELECT event_name, date, time, location, description, creator, datecreated FROM events_db WHERE event_id = ?
            ''', (self.values[0],))
        
        if selection:
            event_name = selection[0][0]
            date = selection[0][1]
            time = selection[0][2]
            location = selection[0][3]
            description = selection [0][4]
            creator = selection [0][5]
            datecreated = selection[0][6]
            if self.call == 'view':
                embed = Embed(title=event_name, description=description, color = discord.Color.blue())
                embed.add_field(name="When", value=f"{date} at {time}", inline = True)
                embed.add_field(name="Where", value=location, inline = False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name="Attending ✅ ", value=" ", inline = True)
                embed.add_field(name="Can't Go ❌", value=" ", inline = True)
                embed.add_field(name="Maybe ❔", value=" ", inline = True)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.add_field(name=" ", value=" ", inline=False)
                embed.set_footer(text=f"Created by {creator} on {datecreated}")
                await interaction.response.edit_message(embed=embed)
            else: 
                self.db.query("DELETE FROM events_db WHERE event_id = ?", self.values[0])
                await interaction.response.send_message(content="Event deleted!", ephemeral=True)
        else:
            await interaction.response.send_message(content="Oops! Something went wrong", ephemeral=True)


class ViewEventsView(ui.View):
     def __init__(self, server_id, call, *, timeout = 180):
         super().__init__(timeout=timeout)
         self.add_item(ViewEventsMenu(server_id, call))



async def setup(client: commands.Bot) -> None:
    await client.add_cog(EventCommands(client))