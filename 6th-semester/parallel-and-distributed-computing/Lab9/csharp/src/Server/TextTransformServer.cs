using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Lab9.Server;

/// <summary>
/// Exercise 1 — Text-transform TCP server (single-threaded).
///
/// Protocol:
///   Client sends:  &lt;command&gt; &lt;text&gt;\n
///   Commands:      upper | lower | reverse | length
///   Server replies with the transformed text.
///   Sending "quit" closes the connection.
///
/// Only one client can connect at a time in this single-threaded version.
/// </summary>
internal sealed class TextTransformServer
{
    private readonly int _port;

    public TextTransformServer(int port) => _port = port;

    public void Start()
    {
        var listener = new TcpListener(IPAddress.Any, _port);
        listener.Start();
        Console.WriteLine($"[TextTransform] Listening on port {_port} ...");

        while (true)
        {
            using var client = listener.AcceptTcpClient();
            Console.WriteLine($"[TextTransform] Client connected: {client.Client.RemoteEndPoint}");
            HandleClient(client);
            Console.WriteLine($"[TextTransform] Client disconnected.");
        }
    }

    private static void HandleClient(TcpClient client)
    {
        using var stream = client.GetStream();
        using var reader = new StreamReader(stream, Encoding.UTF8);
        using var writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true };

        writer.WriteLine("Welcome! Commands: upper <text> | lower <text> | reverse <text> | length <text> | quit");

        string? line;
        while ((line = reader.ReadLine()) != null)
        {
            if (line.Equals("quit", StringComparison.OrdinalIgnoreCase)) break;

            string response = Process(line);
            writer.WriteLine(response);
        }
    }

    private static string Process(string line)
    {
        int space = line.IndexOf(' ');
        if (space < 0) return "ERROR: expected '<command> <text>'";

        string cmd  = line[..space].ToLowerInvariant();
        string text = line[(space + 1)..];

        return cmd switch
        {
            "upper"   => text.ToUpperInvariant(),
            "lower"   => text.ToLowerInvariant(),
            "reverse" => new string(text.Reverse().ToArray()),
            "length"  => text.Length.ToString(),
            _         => $"ERROR: unknown command '{cmd}'"
        };
    }
}
