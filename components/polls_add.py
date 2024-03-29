import discord
from discord import app_commands, ui,  Interaction, Embed, TextStyle, Color
from discord.ext import commands
from matty_db import Database
from datetime import datetime



class AddPoll(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.db = Database()


class Modal1(ui.Modal, title="Add a Poll (Page 1 of 2)"):
    poll_title = ui.TextInput(label="Poll Title", style=TextStyle.short, required=True)
    description = ui.TextInput(label="Description", style=TextStyle.long, required=True)
    
    async def on_submit(self, interaction: Interaction):
        embed = Embed(title="Is this event information is correct? (Page 1 of 2)", description="", color=discord.Color.green())
        embed.add_field(name="Poll Title", value=f"`{self.poll_title}`", inline=False)
        embed.add_field(name="Description", value=self.description, inline=False)
        
        view = Buttons1(self.poll_title, self.description, interaction)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class Buttons1(ui.View):
    def __init__(self, poll_title, description, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.poll_title = poll_title
        self.description = description
        self.interaction = interaction

    @discord.ui.button(label="Yes, continue", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        poll_title = self.poll_title
        description = self.description
        await interaction.response.send_modal(Modal2(poll_title, description))
        
    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"Poll was not created because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self) 


class Modal2(ui.Modal, title="Add a Poll (Page 2 of 2)"):
    def __init__(self, poll_title, description, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.poll_title = poll_title
        self.description= description
  
    start_date = ui.TextInput(label="Start Date in YYYY-MM-DD (e.g. 2023-05-19)", style=TextStyle.short, required=True, min_length=10, max_length=10, placeholder="YYYY-MM-DD")
    start_time = ui.TextInput(label="Start Time in HH:MM (e.g. 08:00 = 8:00 AM)", style=TextStyle.short, required=True, min_length=5, max_length=5, placeholder= "HH:MM")
    end_date = ui.TextInput(label="End Date in YYYY-MM-DD", style=TextStyle.short, required=True, min_length=10, max_length=10, placeholder= "YYYY-MM-DD")
    end_time = ui.TextInput(label="End Time in HH:MM (e.g. 16:00 = 4:00 PM)", style=TextStyle.short, required=True, min_length=5, max_length=5, placeholder="HH:MM")

    async def on_submit(self, interaction: Interaction):
        embed2 = Embed(title="Is this poll information correct? (Page 2 of 2)", description="", color=discord.Color.green())
        embed2.add_field(name="📅 Start date", value=self.start_date, inline=True)
        embed2.add_field(name="⏰ Start time", value=self.start_time, inline=True)
        embed2.add_field(name=" ", value=" ", inline=False)
        embed2.add_field(name=" ", value=" ", inline=False)
        embed2.add_field(name="📅 End date", value=self.end_date, inline=True)
        embed2.add_field(name="⏰ End time", value=self.end_time, inline=True)
        view2 = Buttons2(self.poll_title, self.description, self.start_date, self.start_time, self.end_date, self.end_time, interaction)
        await interaction.response.edit_message(embed=embed2, view=view2)


class Buttons2(ui.View):
    def __init__(self, poll_title, description, start_date, start_time, end_date, end_time, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.poll_title = poll_title
        self.description = description
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.interaction = interaction

    @discord.ui.button(label="Yes, continue", style=discord.ButtonStyle.green)
    async def next(self, interaction: Interaction, button: ui.Button):
        poll_title = self.poll_title
        description = self.description
        start_date = self.start_date
        start_time = self.start_time
        end_date = self.end_date
        end_time = self.end_time
        
        embed3 = Embed(title=f"Are all the poll details correct?", description="", color=discord.Color.green())
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=f"`{poll_title}`", value=description, inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="📅 Start date", value=start_date, inline=True)
        embed3.add_field(name="⏰ Start time", value=start_time, inline=True)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name=" ", value=" ", inline=False)
        embed3.add_field(name="📅 End date", value=end_date, inline=True)
        embed3.add_field(name="⏰ End time", value=end_time, inline=True)
        view3 = Buttons3(self.poll_title, self.description, self.start_date, self.start_time, self.end_date, self.end_time, interaction)
        await interaction.response.edit_message(embed=embed3, view=view3)

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"Poll was not created because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self) 


class Buttons3(ui.View):
    def __init__(self, poll_title, description, start_date, start_time, end_date, end_time, interaction, *, timeout=None):
        super().__init__(timeout=timeout)
        self.db = Database()
        self.poll_title = poll_title
        self.description = description
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.interaction = interaction
        
    @discord.ui.button(label="Yes, add this poll", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        server_id = interaction.guild_id
        creator = interaction.user.name
        timestamp = datetime.now()
        datecreated = timestamp.strftime(f"%m/%d/%Y")

        try:  
    
            sql = "INSERT INTO polls_db(polls_id, server_id, poll_title, description, start_date, start_time, end_date, end_time, poll_link, creator, datecreated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (server_id, self.poll_title.value, self.description.value, self.start_date.value, self.start_time.value, self.end_date.value, self.end_time.value, creator, datecreated)
            self.db.query_input(sql,val)


            embed4 = Embed(title="Success! A new event has been added.", description="To send an invitation to this poll, type command **/poll-- invite**",color = Color.green())
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=f"`{self.poll_title}`", value=self.description, inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="📅 Start date", value=self.start_date, inline=True)
            embed4.add_field(name="⏰ Start time", value=self.start_time, inline=True)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name="📅 End date", value=self.end_date, inline=True)
            embed4.add_field(name="⏰ End time", value=self.end_time, inline=True)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.add_field(name=" ", value=" ", inline=False)
            embed4.set_footer(text=f"Created by {creator} on {datecreated}")

            for child in self.children: 
                child.disabled = True
            await interaction.response.edit_message(embed=embed4, view=self)

        except Exception as error:
            print(f"Error occurred while executing query: {error}")
            embed5 = Embed(title="Oops! Something went wrong while adding a new poll.", description="",color = Color.red())
            embed5.add_field(name=" ", value="Check that the date and times are correctly formatted.", inline=False)
            embed5.add_field(name=" ", value="Ensure that the start date and time does not occur after the end date and time.", inline=False)
            embed5.add_field(name=" ", value=" ", inline=False)
            embed5.add_field(name=" ", value=" ", inline=False)
            embed5.add_field(name="Please try again. If the problem persists, contact support.", value=" ", inline=False)
            for child in self.children: 
                child.disabled = True
            await interaction.response.edit_message(embed=embed5, view=self)
        

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        embed = Embed(title="", description=f"Poll was not created because the action was cancelled.", color = discord.Color.red())
        for child in self.children: #disables all buttons when one is pressed
            child.disabled = True 
        await interaction.response.edit_message(embed=embed, view=self) 
        


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AddPoll(client))