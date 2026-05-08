namespace Lab1;

/// <summary>
/// Prints the first <see cref="_count"/> multiples of <see cref="_multiplier"/>.
///
/// Used by Exercise 4: 10 threads each compute multiples of a different integer (1–10).
/// When all 10 run concurrently the output lines interleave non-deterministically,
/// demonstrating that thread scheduling is controlled by the OS, not the programmer.
/// </summary>
internal sealed class MultiplesWorker
{
    private readonly int _multiplier;
    private readonly int _count;

    public MultiplesWorker(int multiplier, int count = 20)
    {
        _multiplier = multiplier;
        _count      = count;
    }

    public void Execute()
    {
        for (int i = 1; i <= _count; i++)
            Console.WriteLine($"{i,2} × {_multiplier,2} = {i * _multiplier,4}");
    }
}
