namespace Lab1;

/// <summary>
/// Counts from 1 to a configurable limit, printing each value.
/// Demonstrates a thread class with a different constructor signature and a distinct
/// <see cref="Execute"/> body compared to <see cref="GreeterWorker"/>.
/// </summary>
internal sealed class CounterWorker : IWorker
{
    private readonly string _id;
    private readonly int _limit;

    public CounterWorker(string id, int limit)
    {
        _id    = id;
        _limit = limit;
    }

    public void Execute()
    {
        for (int i = 1; i <= _limit; i++)
            Console.WriteLine(
                $"[Counter '{_id}'] i={i}  (thread {Environment.CurrentManagedThreadId})");
    }
}
