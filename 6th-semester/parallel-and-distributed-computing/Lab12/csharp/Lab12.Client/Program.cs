/*
 * Lab 12 — gRPC Client (C# / .NET 8)
 *
 * Connects to the Lab12.Server (http://localhost:5050) and exercises
 * both the Calculator service and the EmailStore service.
 *
 * Start the server first:
 *   cd Lab12.Server && dotnet run
 * Then run this client:
 *   cd Lab12.Client && dotnet run
 */

using Grpc.Net.Client;
using Lab12.Client;

const string ServerAddress = "http://localhost:5050";

Console.WriteLine($"Connecting to gRPC server at {ServerAddress} ...\n");
using var channel = GrpcChannel.ForAddress(ServerAddress);

await RunCalculatorDemo(channel);
await RunEmailStoreDemo(channel);

// ── Calculator demo ───────────────────────────────────────────────────────────

static async Task RunCalculatorDemo(GrpcChannel channel)
{
    var client = new Calculator.CalculatorClient(channel);

    Console.WriteLine("=== Calculator Service ===");

    var ops = new (string label, double a, string op, double b)[]
    {
        ("10 + 3.5", 10, "+", 3.5),
        ("10 - 3",   10, "-", 3  ),
        ("4  * 2.5", 4,  "*", 2.5),
        ("9  / 3",   9,  "/", 3  ),
        ("5  / 0",   5,  "/", 0  ),  // expected: error
    };

    foreach (var (label, a, op, b) in ops)
    {
        var req = new BinaryRequest { A = a, B = b };
        NumberReply reply = op switch
        {
            "+" => await client.AddAsync(req),
            "-" => await client.SubtractAsync(req),
            "*" => await client.MultiplyAsync(req),
            _   => await client.DivideAsync(req),
        };

        string result = string.IsNullOrEmpty(reply.Error)
            ? reply.Result.ToString("G")
            : $"ERROR: {reply.Error}";

        Console.WriteLine($"  {label,-12} = {result}");
    }
    Console.WriteLine();
}

// ── EmailStore demo ───────────────────────────────────────────────────────────

static async Task RunEmailStoreDemo(GrpcChannel channel)
{
    var client = new EmailStore.EmailStoreClient(channel);

    Console.WriteLine("=== EmailStore Service ===");

    // Send several emails concurrently to exercise thread safety
    var sends = new[]
    {
        client.SendAsync(new SendRequest { From="alice@lab", To="bob@lab",   Subject="Hello Bob",  Body="Hi Bob!"  }),
        client.SendAsync(new SendRequest { From="bob@lab",   To="alice@lab", Subject="Re: Hello",  Body="Hey!"     }),
        client.SendAsync(new SendRequest { From="alice@lab", To="carol@lab", Subject="Meeting",    Body="3pm?"     }),
        client.SendAsync(new SendRequest { From="carol@lab", To="bob@lab",   Subject="Invitation", Body="Join us!" }),
    };

    var replies = await Task.WhenAll(sends.Select(c => c.ResponseAsync));
    Console.WriteLine($"Sent {replies.Length} emails concurrently. IDs: {string.Join(", ", replies.Select(r => r.Id))}");

    // Retrieve all emails
    var all = await client.GetAllAsync(new GetRequest());
    Console.WriteLine($"\nAll emails ({all.Messages.Count} total):");
    foreach (var m in all.Messages)
        Console.WriteLine($"  #{m.Id}  {m.From} → {m.To}  \"{m.Subject}\"");

    // Retrieve Bob's inbox
    var bobInbox = await client.GetInboxAsync(new InboxRequest { Recipient = "bob@lab" });
    Console.WriteLine($"\nBob's inbox ({bobInbox.Messages.Count} messages):");
    foreach (var m in bobInbox.Messages)
        Console.WriteLine($"  #{m.Id}  from {m.From}  \"{m.Subject}\"");
}
