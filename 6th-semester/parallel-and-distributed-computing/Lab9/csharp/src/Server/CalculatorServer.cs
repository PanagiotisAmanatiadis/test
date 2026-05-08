using System.Net;
using System.Net.Sockets;
using System.Text;

namespace Lab9.Server;

/// <summary>
/// Exercise 2 — Calculator TCP server (multithreaded, one thread per client).
///
/// Protocol:
///   Client sends:  &lt;operand1&gt; &lt;operator&gt; &lt;operand2&gt;\n
///   Operators:     + - * /
///   Server replies with the numeric result, or an error message.
///   Sending "quit" closes the connection.
///
/// Each accepted connection is handled by a dedicated thread so multiple
/// clients can be served concurrently.
/// </summary>
internal sealed class CalculatorServer
{
    private readonly int _port;

    public CalculatorServer(int port) => _port = port;

    public void Start()
    {
        var listener = new TcpListener(IPAddress.Any, _port);
        listener.Start();
        Console.WriteLine($"[Calculator] Listening on port {_port} ...");

        while (true)
        {
            TcpClient client = listener.AcceptTcpClient();
            Console.WriteLine($"[Calculator] Client connected: {client.Client.RemoteEndPoint}");

            // One thread per client — server stays responsive to new connections
            var thread = new Thread(() => HandleClient(client));
            thread.IsBackground = true;
            thread.Start();
        }
    }

    private static void HandleClient(TcpClient client)
    {
        try
        {
            using var _ = client;
            using var stream = client.GetStream();
            using var reader = new StreamReader(stream, Encoding.UTF8);
            using var writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true };

            writer.WriteLine("Calculator ready. Format: <a> <op> <b>  (op: + - * /)  |  quit");

            string? line;
            while ((line = reader.ReadLine()) != null)
            {
                if (line.Equals("quit", StringComparison.OrdinalIgnoreCase)) break;
                writer.WriteLine(Calculate(line));
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[Calculator] Client error: {ex.Message}");
        }
        finally
        {
            Console.WriteLine($"[Calculator] Client disconnected.");
        }
    }

    private static string Calculate(string expr)
    {
        string[] parts = expr.Trim().Split(' ', StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length != 3) return "ERROR: expected '<a> <op> <b>'";

        if (!double.TryParse(parts[0], out double a) ||
            !double.TryParse(parts[2], out double b))
            return "ERROR: operands must be numbers";

        return parts[1] switch
        {
            "+" => (a + b).ToString("G"),
            "-" => (a - b).ToString("G"),
            "*" => (a * b).ToString("G"),
            "/" => b == 0 ? "ERROR: division by zero" : (a / b).ToString("G"),
            _   => $"ERROR: unknown operator '{parts[1]}'"
        };
    }
}
