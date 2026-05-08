using Microsoft.Extensions.Logging;
using KnuthSolver.Models;
using KnuthSolver.Services;

// ── Logging setup ─────────────────────────────────────────────────────────────
using ILoggerFactory loggerFactory = LoggerFactory.Create(builder =>
    builder.AddSimpleConsole(o => { o.SingleLine = true; o.TimestampFormat = "HH:mm:ss "; })
           .SetMinimumLevel(LogLevel.Information));

var logger = loggerFactory.CreateLogger<Program>();

// ── Read input ────────────────────────────────────────────────────────────────
Console.Write("Search method (BFS or ID): ");
string method = (Console.ReadLine() ?? string.Empty).Trim().ToUpperInvariant();

if (method is not ("BFS" or "ID"))
{
    logger.LogError("Unknown method '{Method}'. Valid options: BFS, ID.", method);
    Environment.Exit(1);
}

Console.Write("Goal number (positive integer): ");
if (!double.TryParse(Console.ReadLine()?.Trim(), out double goal) || goal <= 0)
{
    logger.LogError("Invalid goal number. Please enter a positive integer.");
    Environment.Exit(1);
}

Console.Write("Output file (default: result.txt): ");
string outputPath = Console.ReadLine()?.Trim() is { Length: > 0 } p ? p : "result.txt";

// ── Solve ─────────────────────────────────────────────────────────────────────
var root       = new SearchNode(4.0, parent: null);
var algorithms = new Algorithms(loggerFactory.CreateLogger<Algorithms>());

var result = method == "BFS"
    ? algorithms.BreadthFirstSearch(root, goal)
    : algorithms.IterativeDeepening(root, goal);

// ── Write output ──────────────────────────────────────────────────────────────
if (!result.Solved)
{
    logger.LogWarning("No solution found within the time limit.");
}
else
{
    // Moves list starts with "" for the root node; exclude it from the count.
    var actualMoves = result.Moves.Where(m => !string.IsNullOrEmpty(m)).ToList();

    await using var writer = new StreamWriter(outputPath);
    await writer.WriteLineAsync(
        $"Total moves to reach {goal}: {actualMoves.Count}, " +
        $"time: {(long)result.Elapsed.TotalMilliseconds} milliseconds");

    foreach (var move in actualMoves)
        await writer.WriteLineAsync(move);

    logger.LogInformation(
        "Solution written to '{Output}' ({Moves} moves, {Ms} ms).",
        outputPath, actualMoves.Count, (long)result.Elapsed.TotalMilliseconds);
}
