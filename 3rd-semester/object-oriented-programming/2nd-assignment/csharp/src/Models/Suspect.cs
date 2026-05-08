namespace SurveillanceGui.Models;

public class Suspect
{
    private readonly List<string>  _phoneNumbers  = [];
    private readonly List<Suspect> _collaborators = [];

    public string Name     { get; set; } = string.Empty;
    public string CodeName { get; set; } = string.Empty;
    public string Country  { get; set; } = string.Empty;
    public string City     { get; set; } = string.Empty;

    public IReadOnlyList<string>  PhoneNumbers  => _phoneNumbers.AsReadOnly();
    public IReadOnlyList<Suspect> Collaborators => _collaborators.AsReadOnly();
    public int CollaboratorCount => _collaborators.Count;

    public Suspect() { }
    public Suspect(string name, string codeName, string country, string city)
    { Name = name; CodeName = codeName; Country = country; City = city; }

    public void AddPhoneNumber(string number)
    { if (!_phoneNumbers.Contains(number)) _phoneNumbers.Add(number); }

    public void AddCollaborator(Suspect suspect)
    { if (!_collaborators.Contains(suspect)) _collaborators.Add(suspect); }

    public bool IsConnectedTo(Suspect suspect) => _collaborators.Contains(suspect);

    public IReadOnlyList<Suspect> GetCommonPartners(Suspect other) =>
        _collaborators.Where(s => other.Collaborators.Contains(s)).ToList();

    /// <summary>Returns friends-of-friends not yet directly linked.</summary>
    public IReadOnlyList<Suspect> GetSuggestedPartners()
    {
        var suggestions = new List<Suspect>();
        foreach (var c in _collaborators)
            foreach (var fof in c.Collaborators)
                if (!_collaborators.Contains(fof) && fof != this && !suggestions.Contains(fof))
                    suggestions.Add(fof);
        return suggestions.AsReadOnly();
    }

    public override string ToString() =>
        $"Suspect[name={Name}, codeName={CodeName}, country={Country}, city={City}]";
}
