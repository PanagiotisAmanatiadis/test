namespace Lab4.CarPark;

/// <summary>
/// Bounded car park with <see cref="Capacity"/> spaces.
///
/// A <see cref="SemaphoreSlim"/> limits the number of cars parked simultaneously.
/// Cars that arrive when the park is full block on <see cref="Arrive"/> until a
/// space becomes available; <see cref="Depart"/> releases the semaphore.
///
/// A separate <c>lock</c> ensures that reading and printing the free-space count
/// is atomic and consistent.
/// </summary>
internal sealed class Park
{
    public int Capacity { get; }

    private readonly SemaphoreSlim _gate;
    private          int           _free;
    private readonly object        _printLock = new();

    private const int WaitScaleMs = 10; // max arrival delay
    private const int ParkScaleMs = 5;  // max park duration

    public Park(int capacity)
    {
        Capacity = capacity;
        _free    = capacity;
        _gate    = new SemaphoreSlim(capacity, capacity);
    }

    /// <summary>
    /// Car arrives: random arrival delay, then waits for a free space.
    /// Blocks if the park is full.
    /// </summary>
    public void Arrive(string carName)
    {
        Thread.Sleep(Random.Shared.Next(WaitScaleMs)); // random arrival delay
        Console.WriteLine($"  {carName} arrival");

        _gate.Wait(); // block if no free spaces

        lock (_printLock)
        {
            _free--;
            Console.WriteLine($"  {carName}     parking  (free: {_free})");
        }
    }

    /// <summary>Car stays parked for a random duration.</summary>
    public void Park()
    {
        Thread.Sleep(Random.Shared.Next(ParkScaleMs));
    }

    /// <summary>Car departs: frees the semaphore slot.</summary>
    public void Depart(string carName)
    {
        lock (_printLock)
        {
            _free++;
            Console.WriteLine($"  {carName}         departure  (free: {_free})");
        }

        _gate.Release(); // allow a waiting car to enter
    }
}
