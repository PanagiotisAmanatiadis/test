namespace Lab4.CarPark;

/// <summary>
/// Simulates a car that arrives at the park, waits for a space if needed,
/// parks for a random duration, then departs.
/// </summary>
internal sealed class Car
{
    private readonly string _name;
    private readonly Park   _park;

    public Car(int id, Park park)
    {
        _name = $"Car-{id,2}";
        _park = park;
    }

    public void Run()
    {
        _park.Arrive(_name);
        _park.Park();
        _park.Depart(_name);
    }
}
