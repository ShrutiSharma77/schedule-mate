import discord
from discord.ext import commands
import datetime
import sqlite3
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guild_messages = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def add_task(ctx, *, task):
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)')
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    connection.commit()
    connection.close()

    await ctx.send("Task added successfully.")

@bot.command()
async def list_tasks(ctx):
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    connection.close()

    if tasks:
        task_list = "\n".join([f"{task[0]}. {task[1]}" for task in tasks])
        await ctx.send(f"Tasks:\n{task_list}")
    else:
        await ctx.send("No tasks found.")

@bot.command()
async def remove_task(ctx, task_id: int):
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    connection.commit()
    connection.close()

    await ctx.send("Task removed successfully.")

def time_converter(time_str):
    try:
        parsed_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        print("Parsed time:", parsed_time)
        return parsed_time
    except ValueError:
        raise commands.BadArgument("Please provide the time in the format: YYYY-MM-DD HH:MM.")

@bot.command()
async def set_reminder(ctx, date: str, time: str, *, reminder):
    time_str = f"{date} {time}"
    remind_time = time_converter(time_str)
    
    current_time = datetime.datetime.now()

    if remind_time <= current_time:
        await ctx.send("Please provide a valid future time for the reminder.")
    else:
        time_difference = remind_time - current_time
        reminder_seconds = time_difference.total_seconds()
        await asyncio.sleep(reminder_seconds)
        await ctx.send(f"Reminder: {reminder}")

bot.run(os.getenv('BOT_TOKEN'))


