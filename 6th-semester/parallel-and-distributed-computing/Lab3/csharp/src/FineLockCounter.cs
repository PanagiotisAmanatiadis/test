namespace Lab3;

/// <summary>
/// Exercise 2 — Fine-grained locking.
///
/// Each array element has its own dedicated lock object.
/// Threads that operate on different indices can proceed concurrently;
/// only threads that collide on the same index serialise.
/// This maximises parallelism while still being race-free.
/// </summary>
internal sealed class FineLockCounter
{
    private readonly int[]     _array;
    private readonly object[]  _locks;
    private readonly int       _numThreads;

    public FineLockCounter(int size, int numThreads)
    {
        _array      = new int[size];
        _locks      = new object[size];
        _numThreads = numThreads;

        for (int i = 0; i < size; i++)
            _locks[i] = new object();
    }

    /// <summary>
    /// Thread body: increments array[i] exactly i times.
    /// Each increment acquires only the per-element lock for index i,
    /// allowing other threads to concurrently update different elements.
    /// </summary>
    public void Run()
    {
        for (int i = 0; i < _array.Length; i++)
            for (int j = 0; j < i; j++)
                lock (_locks[i])
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
