using Microsoft.Extensions.Logging;
using SurveillanceGui.Models;
using SurveillanceGui.Services;

namespace SurveillanceGui.UI;

/// <summary>Interactive console UI mirroring the Swing GUI screen flow.</summary>
public class ConsoleUI
{
    private readonly Registry           _registry;
    private readonly ILogger<ConsoleUI> _logger;

    public ConsoleUI(Registry registry, ILogger<ConsoleUI> logger)
    { _registry = registry; _logger = logger; }

    public void Run()
    {
        _logger.LogInformation("Surveillance Registry — Console Interface");
        while (true)
        {
            Console.Write("\nSearch suspect by name (or 'quit'): ");
            string? input = Console.ReadLine()?.Trim();
            if (string.IsNullOrEmpty(input) || input.Equals("quit", StringComparison.OrdinalIgnoreCase)) break;

            var suspect = _registry.GetSuspectByName(input);
            if (suspect is null) { _logger.LogWarning("Suspect \"{Name}\" not found.", input); continue; }
            ShowDetail(suspect);
        }
        _logger.LogInformation("Session ended.");
    }

    private void ShowDetail(Suspect suspect)
    {
        while (true)
        {
            Console.WriteLine($"\n╔══ {suspect.Name} ({suspect.CodeName}) — {suspect.Country}, {suspect.City}");
            Console.WriteLine("║ [1] Collaborators  [2] Suggested partners");
            Console.WriteLine("║ [3] Suspicious SMS [4] Co-nationals  [0] Back");
            Console.Write("╚═ Choice: ");
            switch (Console.ReadLine()?.Trim())
            {
                case "1":
                    foreach (var s in suspect.Collaborators)
                        Console.WriteLine($"  {s.Name} ({s.CodeName})");
                    break;
                case "2":
                    foreach (var s in suspect.GetSuggestedPartners())
                        Console.WriteLine($"  {s.Name}");
                    break;
                case "3":
                    Console.Write("Target number: ");
                    string? target = Console.ReadLine()?.Trim();
                    if (string.IsNullOrEmpty(target)) break;
                    bool found = false;
                    foreach (var own in suspect.PhoneNumbers)
                        foreach (var sms in _registry.GetSuspiciousMessagesBetween(own, target))
                        { Console.WriteLine($"  {sms.Content}"); found = true; }
                    if (!found) Console.WriteLine("  No suspicious messages.");
                    break;
                case "4":
                    foreach (var s in _registry.GetSuspectsFromCountry(suspect.Country))
                        Console.WriteLine($"  {s.Name} ({s.CodeName})");
                    break;
                case "0": return;
                default: Console.WriteLine("Invalid option."); break;
            }
        }
    }
}
