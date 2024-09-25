import os
from fastapi import FastAPI
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from db import link_user_to_discord


# Initialize FastAPI app
app = FastAPI()
load_dotenv()

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Create a task to start the bot
async def start_bot():
    await bot.start(os.getenv("BOT_TOKEN"))


# Define a FastAPI startup event
@app.on_event("startup")
async def startup_event():
    print("Starting Discord bot...")
    asyncio.create_task(start_bot())


# Define a FastAPI shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Discord bot...")
    await bot.logout()


# Define a sample command for the bot
@bot.command()
async def link(ctx, token: str):
    discord_user_id = ctx.author.id

    success = link_user_to_discord(token, discord_user_id)
    if success:
        await ctx.send(f"Gelukt, je bent nu gelinkt")
    else:
        await ctx.send(f"Er is wat fout gegaan")


# Define a FastAPI route
@app.get("/")
async def root():
    return {"message": "Hello, this is the FastAPI server!"}


# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
