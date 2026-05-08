using System.Diagnostics;

namespace Lab7;

/// <summary>
/// Exercise 3 — Parallel Sieve of Eratosthenes.
///
/// Finds all primes up to <see cref="Limit"/>.
///
/// Phase 1 (sequential): mark composites for primes p ≤ √Limit.
/// Phase 2 (parallel):   sieve the remaining candidates.
///   Three scheduling strategies are compared:
///   <list type="bullet">
///     <item><see cref="StaticScheduling"/>  — divide range [√Limit, Limit] equally.</item>
///     <item><see cref="CyclicScheduling"/>  — round-robin: thread t handles multiples of stride.</item>
///     <item><see cref="DynamicScheduling"/> — threads pull work units from a shared counter.</item>
///   </list>
/// </summary>
internal static class SieveOfEratosthenes
{
    private const int Limit      = 10_000_000;
    private const int NumThreads = 4;
    private const int ChunkSize  = 1_000; // work unit for dynamic scheduling

    // ── Sequential reference ──────────────────────────────────────────────────

    public static void Sequential()
    {
        bool[] composite = new bool[Limit + 1];
        var sw = Stopwatch.StartNew();
        Sieve(composite, 2, Limit);
        sw.Stop();
        int count = CountPrimes(composite);
        Console.WriteLine($"  Sequential    : {sw.ElapsedMilliseconds,6} ms  primes={count}");
    }

    // ── Static scheduling ─────────────────────────────────────────────────────

    public static void StaticScheduling()
    {
        bool[] composite = new bool[Limit + 1];
        int sqrtLimit    = (int)Math.Sqrt(Limit);

        // Phase 1: sequential sieve up to √Limit
        Sieve(composite, 2, sqrtLimit);

        // Phase 2: divide remainder evenly
        int rangeStart = sqrtLimit + 1;
        int rangeLen   = Limit - rangeStart + 1;
        int chunk      = (rangeLen + NumThreads - 1) / NumThreads;
        var threads    = new Thread[NumThreads];

        var sw = Stopwatch.StartNew();
        for (int t = 0; t < NumThreads; t++)
        {
            int s = rangeStart + t * chunk;
            int e = Math.Min(s + chunk - 1, Limit);
            threads[t] = new Thread(() => SieveRange(composite, s, e, sqrtLimit));
        }
        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();
        sw.Stop();

        int count = CountPrimes(composite);
        Console.WriteLine($"  Static        : {sw.ElapsedMilliseconds,6} ms  primes={count}  ({NumThreads} threads)");
    }

    // ── Cyclic scheduling ─────────────────────────────────────────────────────

    public static void CyclicScheduling()
    {
        bool[] composite = new bool[Limit + 1];
        int sqrtLimit    = (int)Math.Sqrt(Limit);

        Sieve(composite, 2, sqrtLimit);

        int rangeStart = sqrtLimit + 1;
        var threads    = new Thread[NumThreads];

        var sw = Stopwatch.StartNew();
        for (int t = 0; t < NumThreads; t++)
        {
            int tid = t;
            threads[t] = new Thread(() =>
            {
                // Thread tid handles numbers: rangeStart+tid, rangeStart+tid+NumThreads, ...
                for (int n = rangeStart + tid; n <= Limit; n += NumThreads)
                {
                    if (!composite[n])
                        MarkMultiples(composite, n, Limit);
                }
            });
        }
        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();
        sw.Stop();

        int count = CountPrimes(composite);
        Console.WriteLine($"  Cyclic        : {sw.ElapsedMilliseconds,6} ms  primes={count}  ({NumThreads} threads)");
    }

    // ── Dynamic scheduling ────────────────────────────────────────────────────

    public static void DynamicScheduling()
    {
        bool[] composite = new bool[Limit + 1];
        int sqrtLimit    = (int)Math.Sqrt(Limit);

        Sieve(composite, 2, sqrtLimit);

        // Shared work counter; threads atomically claim the next chunk start
        int sharedStart  = sqrtLimit + 1;
        var threads      = new Thread[NumThreads];

        var sw = Stopwatch.StartNew();
        for (int t = 0; t < NumThreads; t++)
        {
            threads[t] = new Thread(() =>
            {
                while (true)
                {
                    int s = Interlocked.Add(ref sharedStart, ChunkSize) - ChunkSize;
                    if (s > Limit) break;
                    int e = Math.Min(s + ChunkSize - 1, Limit);
                    SieveRange(composite, s, e, sqrtLimit);
                }
            });
        }
        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();
        sw.Stop();

        int count = CountPrimes(composite);
        Console.WriteLine($"  Dynamic       : {sw.ElapsedMilliseconds,6} ms  primes={count}  ({NumThreads} threads, chunk={ChunkSize})");
    }

    // ── private helpers ───────────────────────────────────────────────────────

    /// <summary>Sequential sieve from 2 to <paramref name="limit"/>.</summary>
    private static void Sieve(bool[] composite, int from, int limit)
    {
        for (int p = from; p <= limit; p++)
            if (!composite[p])
                MarkMultiples(composite, p, composite.Length - 1);
    }

    /// <summary>
    /// For each number n in [start, end] that is not yet marked composite,
    /// mark all its multiples.  Used by static and dynamic scheduling where
    /// a contiguous block is assigned to one thread.
    /// </summary>
    private static void SieveRange(bool[] composite, int start, int end, int sqrtLimit)
    {
        for (int p = 2; p <= sqrtLimit; p++)
        {
            if (composite[p]) continue;
            // First multiple of p that falls in [start, end]
            int first = ((start + p - 1) / p) * p;
            if (first == p) first += p; // skip p itself
            for (int k = first; k <= end; k += p)
                composite[k] = true;
        }
    }

    private static void MarkMultiples(bool[] composite, int p, int limit)
    {
        for (long k = (long)p * p; k <= limit; k += p)
            composite[(int)k] = true;
    }

    private static int CountPrimes(bool[] composite)
    {
        int count = 0;
        for (int i = 2; i < composite.Length; i++)
            if (!composite[i]) count++;
        return count;
    }
}
