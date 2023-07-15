import discord
from discord.ext import commands
import datetime
import sqlite3

bot = commands.Bot(command_prefix='!')

@bot.command()
async def add_task(ctx, *, task):
    # Save the task to a database or data structure
    # You can use an SQLite database for simplicity
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)')
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    connection.commit()
    connection.close()

    await ctx.send("Task added successfully.")

