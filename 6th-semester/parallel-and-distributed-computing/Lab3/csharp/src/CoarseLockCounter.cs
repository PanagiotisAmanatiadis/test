namespace Lab3;

/// <summary>
/// Exercise 1 — Coarse-grained locking.
///
/// A single mutex guards the entire shared array.
/// All threads serialise on one lock, which is safe but limits parallelism
/// because only one thread can modify any element at a time.
/// </summary>
internal sealed class CoarseLockCounter
{
    private readonly int[]   _array;
    private readonly object  _mutex = new();
    private readonly int     _numThreads;

    public CoarseLockCounter(int size, int numThreads)
    {
        _array      = new int[size];
        _numThreads = numThreads;
    }

    /// <summary>
    /// Thread body: increments array[i] exactly i times for every index.
    /// The entire increment is protected by a single coarse-grained lock.
    /// </summary>
    public void Run()
    {
        for (int i = 0; i < _array.Length; i++)
            for (int j = 0; j < i; j++)
                lock (_mutex)
                    _array[i]++;
    }

    /// <summary>Returns the number of elements whose value differs from the expected N×i.</summary>
    public int Verify()
    {
        int errors = 0;
        for (int i = 0; i < _array.Length; i++)
        {
            int expected = _numThreads * i;
            if (_array[i] != expected)
            {
                errors++;
                if (errors <= 5)
                    Console.WriteLine($"  index {i,4}: got {_array[i],5}, expected {expected,5}");
            }
        }
        return errors;
    }
}
