namespace Lab5;

/// <summary>
/// Utility that splits an index range [0, total) into <paramref name="numThreads"/>
/// equal chunks and runs <paramref name="body"/> on each chunk concurrently.
///
/// This is the manual thread-based equivalent of <c>Parallel.For</c> and is used
/// throughout Lab 5 to show how data-parallel loops are implemented by hand.
/// </summary>
internal static class ParallelRunner
{
    /// <summary>
    /// Partitions [0, <paramref name="total"/>) into <paramref name="numThreads"/> slices
    /// and invokes <c>body(start, end)</c> on each slice in a separate thread.
    /// </summary>
    public static void For(int total, int numThreads, Action<int, int> body)
    {
        int chunkSize = (total + numThreads - 1) / numThreads;
        var threads   = new Thread[numThreads];

        for (int t = 0; t < numThreads; t++)
        {
            int start = t * chunkSize;
            int end   = Math.Min(start + chunkSize, total);
            threads[t] = new Thread(() => body(start, end));
        }

        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();
    }
}
