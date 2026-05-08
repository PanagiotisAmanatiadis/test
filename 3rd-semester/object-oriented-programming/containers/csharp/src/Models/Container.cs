namespace ShipCargoSystem.Models;

/// <summary>
/// Abstract base class representing a shipping container.
/// Concrete subclasses define the cost calculation for their cargo type.
/// </summary>
public abstract class Container
{
    /// <summary>Gets the unique container identifier.</summary>
    public string Code { get; }

    /// <summary>Gets the destination port or city.</summary>
    public string Destination { get; }

    /// <summary>Initialises a Container.</summary>
    /// <param name="code">Unique container identifier.</param>
    /// <param name="destination">Destination port or city.</param>
    protected Container(string code, string destination)
    {
        Code        = code;
        Destination = destination;
    }

    /// <summary>Calculates the shipping cost for this container.</summary>
    /// <returns>Shipping cost in currency units.</returns>
    public abstract double GetCost();

    /// <inheritdoc/>
    public override string ToString() =>
        $"{GetType().Name}[code={Code}, destination={Destination}, cost={GetCost():F2}]";
}
