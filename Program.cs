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
        _client = new DiscordSocketClient();

        _client.Log += Log;
        _client.MessageReceived += MessageReceivedAsync;

        // Замените "YOUR_BOT_TOKEN" на токен вашего бота
        await _client.LoginAsync(TokenType.Bot, "MTM0NTMxODMwMTkyODEyODYwNQ.Gv9m94.PLq78zt7VevijvzShOm2KAbveZoDRBHSG6tpl0");
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
