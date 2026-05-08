/*
 * Lab 9 — TCP Client-Server (C# / .NET 8)
 *
 * Usage:
 *   dotnet run -- server text  [port]   Run the text-transform server (single-threaded)
 *   dotnet run -- server calc  [port]   Run the calculator server (multi-threaded)
 *   dotnet run -- client       [host] [port]  Connect as interactive client
 *
 * Defaults: host=127.0.0.1, port=8080
 *
 * Exercise 1 — Text-transform server (single-threaded)
 *   Accepts one client at a time.  Commands: upper / lower / reverse / length.
 *   Demonstrates the basic TCP accept-read-write-close cycle.
 *
 * Exercise 2 — Calculator server (multithreaded, one thread per client)
 *   Each accepted connection spawns a background thread so multiple clients
 *   can use the server simultaneously.
 *   Protocol: "<a> <op> <b>"  where op ∈ {+ - * /}
 *
 * Exercise 3 — Interactive client
 *   Connects to either server, reads the greeting, then sends user-typed
 *   commands and prints each server response.
 */

using Lab9.Client;
using Lab9.Server;

if (args.Length == 0)
{
    PrintUsage();
    return;
}

switch (args[0].ToLowerInvariant())
{
    case "server":
    {
        string mode = args.Length > 1 ? args[1].ToLowerInvariant() : "text";
        int    port = args.Length > 2 ? int.Parse(args[2]) : 8080;

        if (mode == "calc")
            new CalculatorServer(port).Start();
        else
            new TextTransformServer(port).Start();
        break;
    }

    case "client":
    {
        string host = args.Length > 1 ? args[1] : "127.0.0.1";
        int    port = args.Length > 2 ? int.Parse(args[2]) : 8080;
        new TcpCommandClient(host, port).Connect();
        break;
    }

    default:
        PrintUsage();
        break;
}

static void PrintUsage()
{
    Console.WriteLine("Usage:");
    Console.WriteLine("  dotnet run -- server text [port]        Text-transform server (default port 8080)");
    Console.WriteLine("  dotnet run -- server calc [port]        Calculator server (multithreaded)");
    Console.WriteLine("  dotnet run -- client [host] [port]      Interactive TCP client");
}
