using Microsoft.Extensions.Logging;
using ShipCargoSystem.Models;
using ShipCargoSystem.Services;

// ── Logging setup ─────────────────────────────────────────────────────────────
using ILoggerFactory loggerFactory = LoggerFactory.Create(builder =>
    builder.AddSimpleConsole(o =>
    {
        o.SingleLine      = true;
        o.TimestampFormat = "yyyy-MM-dd HH:mm:ss ";
    }).SetMinimumLevel(LogLevel.Information));

ILogger<Ship>    shipLogger = loggerFactory.CreateLogger<Ship>();
ILogger<Program> log        = loggerFactory.CreateLogger<Program>();

// ── Ship setup ────────────────────────────────────────────────────────────────
var ship = new Ship(450, shipLogger);

ship.AddContainer(new BulkContainer("CYZ1011",        "Madrid",    500.0));
ship.AddContainer(new BulkContainer("CYZ1012",        "Barcelona", 2000.0));
ship.AddContainer(new RefrigeratedContainer("CYZ1013", "Rome",     100.0));
ship.AddContainer(new RefrigeratedContainer("CYZ1014", "Milano",   200.0));

// ── Console menu ──────────────────────────────────────────────────────────────
log.LogInformation("Ship Cargo System — Console Interface");

while (true)
{
    Console.WriteLine("\n[1] Calculate total charge");
    Console.WriteLine("[2] List all containers");
    Console.WriteLine("[0] Exit");
    Console.Write("Choice: ");

    switch (Console.ReadLine()?.Trim())
    {
        case "1":
            log.LogInformation("Total shipping cost: {Cost:F2}", ship.GetTotalCost());
            break;
        case "2":
            ship.PrintContainers();
            break;
        case "0":
            goto done;
        default:
            Console.WriteLine("Invalid option.");
            break;
    }
}

done:
log.LogInformation("Goodbye.");
