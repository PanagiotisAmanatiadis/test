namespace ShipCargoSystem.Models;

/// <summary>
/// A refrigerated shipping container charged based on power consumption.
/// <para>Cost formula: <c>powerKw × 2000</c></para>
/// </summary>
public sealed class RefrigeratedContainer : Container
{
    private const double RatePerKw = 2000.0;

    /// <summary>Gets the power consumption in kilowatts.</summary>
    public double PowerKw { get; }

    /// <summary>Initialises a RefrigeratedContainer.</summary>
    /// <param name="code">Unique container identifier.</param>
    /// <param name="destination">Destination port or city.</param>
    /// <param name="powerKw">Power consumption in kilowatts.</param>
    public RefrigeratedContainer(string code, string destination, double powerKw)
        : base(code, destination) => PowerKw = powerKw;

    /// <inheritdoc/>
    public override double GetCost() => RatePerKw * PowerKw;

    /// <inheritdoc/>
    public override string ToString() =>
        $"RefrigeratedContainer[code={Code}, destination={Destination}, power={PowerKw:F1} kW, cost={GetCost():F2}]";
}
