import disnake
from disnake.ext import commands
import os
import json
import sys

from dotenv import load_dotenv
load_dotenv()

# --- Конфигурация ---
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print("config.json not found. Creating default config.")
    config = {
        'token': '',
        'prefix': '!',
        'test_guilds': [1337101541588602952]
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Please edit config.json with your bot token and guild ID.")
    sys.exit()


# --- Бот ---
def get_prefix(bot, message):
    """Возвращает префикс для данного сервера"""
    return commands.when_mentioned_or(config['prefix'])(bot, message)


bot = commands.Bot(command_prefix=get_prefix, intents=disnake.Intents.all(), test_guilds=config['test_guilds'])
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} запущен!")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


# --- Cogs ---

# --- Calculator Cog ---
class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, ctx, expression: str):
        """Простой калькулятор."""
        try:
            result = eval(expression)
            await ctx.send(str(result))
        except Exception as ex:
            await ctx.send(f"Произошла ошибка: {ex}")


# --- Help Cog ---
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.slash_command(name="help", description="Показывает список команд и информацию о боте")
    async def help_command(
            self,
            inter: disnake.ApplicationCommandInteraction,
            command_name: str = commands.Param(default=None, description="Название команды для получения информации"),
    ):
        """
        Показывает список команд и информацию о боте (slash-команда).

        Args:
            inter: Объект взаимодействия с slash-командой.
            command_name: (Опционально) Название команды для получения подробной информации.
        """
        try:
            if command_name:  # Если указано имя команды
                command = self.bot.get_slash_command(command_name) or self.bot.get_command(command_name)
                if command:
                    embed = disnake.Embed(
                        title=f"Справка по команде: {command.name}",
                        description=command.description,
                        color=0x00ff00,
                    )
                    if isinstance(command, commands.SlashCommand):
                        embed.add_field(
                            name="Использование", value=f"`/{command.name} {command.signature}`", inline=False
                        )
                    else:
                        prefix = self.bot.command_prefix(self.bot, inter.message)[0]
                        embed.add_field(
                            name="Использование", value=f"`{prefix}{command.name} {command.signature}`", inline=False
                        )
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    await inter.response.send_message(f"Команда '{command_name}' не найдена.", ephemeral=True)
            else:  # Если имя команды не указано, показываем список всех команд
                embed = disnake.Embed(
                    title="Список команд", description="Доступные команды:", color=0x00ff00
                )
                for command in list(self.bot.slash_commands):  # Преобразуем в список
                    embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
                for command in self.bot.commands:  # Add prefix commands
                    embed.add_field(name=f"!{command.name}", value=command.description, inline=False)
                embed.set_footer(
                    text="Для получения подробной информации о команде, используйте !help <название_команды>"
                )
                await inter.response.send_message(embed=embed, ephemeral=True)

        except Exception as ex:
            await inter.response.send_message(
                f"Произошла ошибка при выполнении команды help: {ex}", ephemeral=True
            )

    @commands.command()
    async def help(self, ctx, command_name: str = None):
        """Показывает список команд и информацию о боте (для команд с префиксом)."""
        try:
            if command_name:  # Если указано имя команды
                command = self.bot.get_slash_command(command_name) or self.bot.get_command(command_name)
                if command:
                    embed = disnake.Embed(
                        title=f"Справка по команде: {command.name}",
                        description=command.description,
                        color=0x00ff00,
                    )
                    if isinstance(command, commands.SlashCommand):
                        embed.add_field(
                            name="Использование", value=f"`/{command.name} {command.signature}`", inline=False
                        )
                    else:
                        prefix = self.bot.command_prefix(self.bot, ctx.message)[0]
                        embed.add_field(
                            name="Использование", value=f"`{prefix}{command.name} {command.signature}`", inline=False
                        )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"Команда '{command_name}' не найдена.")
            else:  # Если имя команды не указано, показываем список всех команд
                embed = disnake.Embed(
                    title="Список команд", description="Доступные команды:", color=0x00ff00
                )
                for command in list(self.bot.slash_commands):  # Преобразуем в список
                    embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
                for command in self.bot.commands:  # Add prefix commands
                    embed.add_field(name=f"!{command.name}", value=command.description, inline=False)
                embed.set_footer(
                    text="Для получения подробной информации о команде, используйте !help <название_команды>"
                )
                await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f"Произошла ошибка при выполнении команды help: {ex}")


# --- Restart Cog ---
class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()  # Ограничение: только владелец бота может использовать
    async def restart(self, ctx):
        """Перезапускает бота."""
        await ctx.send("Бот перезапускается...")
        os.execv(sys.executable, ['python'] + sys.argv)  # Перезапуск


# --- Git Cog ---
class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def git(self, ctx):
        await ctx.send(
            "Вот ссылка на репозиторий: https://github.com/KiTiKeT9/pandoras-box")


# --- Load Cogs ---
def load_cogs(bot):
    bot.add_cog(Calculator(bot))
    print("Cog 'Calculator' loaded")
    bot.add_cog(Help(bot))
    print("Cog 'Help' loaded")
    bot.add_cog(Restart(bot))
    print("Cog 'Restart' loaded")
    bot.add_cog(Git(bot))
    print("Cog 'Git' loaded")


# --- Запуск бота ---
load_cogs(bot)
bot.run(config['token'])