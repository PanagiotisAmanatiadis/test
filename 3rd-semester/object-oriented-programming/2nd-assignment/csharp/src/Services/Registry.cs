using Microsoft.Extensions.Logging;
using SurveillanceGui.Models;

namespace SurveillanceGui.Services;

public class Registry
{
    private static readonly IReadOnlySet<string> SuspiciousKeywords =
        new HashSet<string> { "Bomb", "Attack", "Gun", "Explosives" };

    private readonly ILogger<Registry>   _logger;
    private readonly List<Suspect>       _suspects       = [];
    private readonly List<Communication> _communications = [];

    public Registry(ILogger<Registry> logger) => _logger = logger;

    public IReadOnlyList<Suspect> Suspects => _suspects.AsReadOnly();

    public void AddSuspect(Suspect suspect)
    { _suspects.Add(suspect); _logger.LogInformation("Registered: {Name}", suspect.Name); }

    public void AddCommunication(Communication communication)
    {
        _communications.Add(communication);
        var s1 = FindByNumber(communication.SenderNumber);
        var s2 = FindByNumber(communication.ReceiverNumber);
        if (s1 is not null && s2 is not null && s1 != s2)
        { s1.AddCollaborator(s2); s2.AddCollaborator(s1); }
    }

    public Suspect? GetSuspectByName(string name) =>
        _suspects.FirstOrDefault(s => s.Name.Equals(name, StringComparison.OrdinalIgnoreCase));

    public Suspect? GetSuspectWithMostPartners() => _suspects.MaxBy(s => s.CollaboratorCount);

    public IReadOnlyList<Sms> GetSuspiciousMessagesBetween(string number1, string number2) =>
        _communications
            .Where(c => Involves(c, number1, number2) && !string.IsNullOrEmpty(c.GetSmsContent()))
            .Where(c => SuspiciousKeywords.Any(kw => c.GetSmsContent().Contains(kw)))
            .Cast<Sms>().ToList();

    public IReadOnlyList<Suspect> GetSuspectsFromCountry(string country) =>
        _suspects.Where(s => s.Country == country).ToList();

    private Suspect? FindByNumber(string number) =>
        _suspects.FirstOrDefault(s => s.PhoneNumbers.Contains(number));

    private static bool Involves(Communication c, string n1, string n2) =>
        (c.SenderNumber == n1 && c.ReceiverNumber == n2) ||
        (c.SenderNumber == n2 && c.ReceiverNumber == n1);
}
