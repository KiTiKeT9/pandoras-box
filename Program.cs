using Discord;
using Discord.WebSocket;
using System;
using System.Threading.Tasks;

class Program
{
	private DiscordSocketClient _client;

	public static async Task Main(string[] args) => await new Program().RunBotAsync();

	public async Task RunBotAsync()
	{
		_client = new DiscordSocketClient(new DiscordSocketConfig()
		{
			GatewayIntents = GatewayIntents.Guilds |
							 GatewayIntents.GuildMessages |
							 GatewayIntents.MessageContent
		});

		_client.Log += Log;
		_client.MessageReceived += MessageReceivedAsync;

		// Получаем токен из переменной окружения
		string token = Environment.GetEnvironmentVariable("DISCORD_TOKEN");

		if (string.IsNullOrEmpty(token))
		{
			Console.WriteLine("Ошибка: переменная окружения DISCORD_TOKEN не установлена!");
			return;
		}

		await _client.LoginAsync(TokenType.Bot, token);
		await _client.StartAsync();

		// Ждем завершения работы
		await Task.Delay(-1);
	}

	private Task Log(LogMessage arg)
	{
		Console.WriteLine(arg);
		return Task.CompletedTask;
	}

	private async Task MessageReceivedAsync(SocketMessage message)
	{
		// Игнорируем сообщения от бота
		if (message is not SocketUserMessage userMessage || message.Author.IsBot)
			return;

		
		if (userMessage.Content == "!hello")
		{
			// Отправляем ответ
			await message.Channel.SendMessageAsync("Привет, мир!");
		}

	}
}
