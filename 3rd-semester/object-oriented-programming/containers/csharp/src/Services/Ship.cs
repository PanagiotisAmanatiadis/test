using Microsoft.Extensions.Logging;
using ShipCargoSystem.Models;

namespace ShipCargoSystem.Services;

/// <summary>
/// Represents a cargo ship with a fixed maximum container capacity.
/// </summary>
public class Ship
{
    private readonly ILogger<Ship>   _logger;
    private readonly List<Container> _containers = [];
    private readonly int             _capacity;

    /// <summary>Gets all loaded containers (read-only).</summary>
    public IReadOnlyList<Container> Containers => _containers.AsReadOnly();

    /// <summary>Initialises the Ship.</summary>
    /// <param name="capacity">Maximum number of containers.</param>
    /// <param name="logger">Logger instance.</param>
    public Ship(int capacity, ILogger<Ship> logger)
    {
        _capacity = capacity;
        _logger   = logger;
    }

    /// <summary>
    /// Loads a container if capacity allows; warns and skips otherwise.
    /// </summary>
    /// <param name="container">The container to load.</param>
    public void AddContainer(Container container)
    {
        if (_containers.Count < _capacity)
            _containers.Add(container);
        else
            _logger.LogWarning("Ship at full capacity ({Cap}). Cannot add {Code}.", _capacity, container.Code);
    }

    /// <summary>Calculates the total shipping cost for all loaded containers.</summary>
    /// <returns>Total cost.</returns>
    public double GetTotalCost() => _containers.Sum(c => c.GetCost());

    /// <summary>Logs all loaded containers.</summary>
    public void PrintContainers()
    {
        foreach (var c in _containers)
            _logger.LogInformation("{Container}", c);
    }
}
