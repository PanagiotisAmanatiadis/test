using System.Net.Sockets;
using System.Text;

namespace Lab9.Client;

/// <summary>
/// Interactive TCP client for the text-transform and calculator servers.
///
/// Connects to <paramref name="host"/>:<paramref name="port"/>, reads the
/// server's greeting, then enters a read-eval loop: the user types commands
/// that are sent to the server and the response is printed.
///
/// Type <c>quit</c> to close the connection.
/// </summary>
internal sealed class TcpCommandClient
{
    private readonly string _host;
    private readonly int    _port;

    public TcpCommandClient(string host, int port)
    {
        _host = host;
        _port = port;
    }

    public void Connect()
    {
        using var client = new TcpClient(_host, _port);
        using var stream = client.GetStream();
        using var reader = new StreamReader(stream, Encoding.UTF8);
        using var writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true };

        // Print server greeting
        Console.WriteLine(reader.ReadLine());

        while (true)
        {
            Console.Write("> ");
            string? input = Console.ReadLine();
            if (input == null) break;

            writer.WriteLine(input);

            if (input.Equals("quit", StringComparison.OrdinalIgnoreCase)) break;

            string? response = reader.ReadLine();
            Console.WriteLine($"< {response}");
        }

        Console.WriteLine("Connection closed.");
    }
}
