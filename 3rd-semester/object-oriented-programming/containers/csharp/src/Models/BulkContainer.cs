namespace ShipCargoSystem.Models;

/// <summary>
/// A shipping container carrying bulk (dry) cargo.
/// <para>Cost formula: <c>weightKg × 10</c></para>
/// </summary>
public sealed class BulkContainer : Container
{
    private const double RatePerKg = 10.0;

    /// <summary>Gets the cargo weight in kilograms.</summary>
    public double WeightKg { get; }

    /// <summary>Initialises a BulkContainer.</summary>
    /// <param name="code">Unique container identifier.</param>
    /// <param name="destination">Destination port or city.</param>
    /// <param name="weightKg">Cargo weight in kilograms.</param>
    public BulkContainer(string code, string destination, double weightKg)
        : base(code, destination) => WeightKg = weightKg;

    /// <inheritdoc/>
    public override double GetCost() => RatePerKg * WeightKg;

    /// <inheritdoc/>
    public override string ToString() =>
        $"BulkContainer[code={Code}, destination={Destination}, weight={WeightKg:F1} kg, cost={GetCost():F2}]";
}
