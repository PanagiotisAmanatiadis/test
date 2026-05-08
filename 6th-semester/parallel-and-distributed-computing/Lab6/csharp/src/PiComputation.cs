using System.Diagnostics;

namespace Lab6;

/// <summary>
/// Pi computation via numerical integration of 4/(1+x²) over [0,1].
///
/// Three variants:
/// <list type="number">
///   <item><see cref="Sequential"/>   — single thread, baseline.</item>
///   <item><see cref="SharedLock"/>   — multiple threads accumulate into one shared
///         double, protected by a <c>lock</c>. Correct but every step acquires
///         the lock — high contention, poor scalability.</item>
///   <item><see cref="LocalReduction"/> — each thread keeps its own private partial
///         sum; partial sums are combined once after all threads finish.
///         No contention during computation — optimal scalability.</item>
/// </list>
/// </summary>
internal static class PiComputation
{
    private const long NumSteps  = 10_000_000L;
    private const int  NumThreads = 4;

    // ── Variant 1: Sequential ─────────────────────────────────────────────────

    public static void Sequential()
    {
        double step = 1.0 / NumSteps;
        double sum  = 0.0;

        var sw = Stopwatch.StartNew();
        for (long i = 0; i < NumSteps; i++)
        {
            double x = (i + 0.5) * step;
            sum += 4.0 / (1.0 + x * x);
        }
        double pi = sum * step;
        sw.Stop();

        PrintResult("Sequential            ", pi, sw.Elapsed);
    }

    // ── Variant 2: Parallel with shared sum + lock ────────────────────────────

    public static void SharedLock()
    {
        double step   = 1.0 / NumSteps;
        double sum    = 0.0;
        object mutex  = new();

        var sw = Stopwatch.StartNew();
        RunThreads((start, end) =>
        {
            for (long i = start; i < end; i++)
            {
                double x = (i + 0.5) * step;
                lock (mutex) sum += 4.0 / (1.0 + x * x);
            }
        });
        double pi = sum * step;
        sw.Stop();

        PrintResult("Parallel (shared lock)", pi, sw.Elapsed);
    }

    // ── Variant 3: Parallel with per-thread local reduction ───────────────────

    public static void LocalReduction()
    {
        double step       = 1.0 / NumSteps;
        double[] partials = new double[NumThreads]; // one slot per thread, no sharing

        var sw = Stopwatch.StartNew();

        int  chunkSize = (int)((NumSteps + NumThreads - 1) / NumThreads);
        var  threads   = new Thread[NumThreads];

        for (int t = 0; t < NumThreads; t++)
        {
            int tid   = t;
            long s    = (long)tid * chunkSize;
            long e    = Math.Min(s + chunkSize, NumSteps);
            threads[t] = new Thread(() =>
            {
                double localSum = 0.0;
                for (long i = s; i < e; i++)
                {
                    double x = (i + 0.5) * step;
                    localSum += 4.0 / (1.0 + x * x);
                }
                partials[tid] = localSum; // write to own slot — no race
            });
        }

        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();

        double pi = partials.Sum() * step; // single-threaded reduction
        sw.Stop();

        PrintResult("Parallel (local sums) ", pi, sw.Elapsed);
    }

    // ── helpers ───────────────────────────────────────────────────────────────

    private static void PrintResult(string label, double pi, TimeSpan elapsed)
    {
        Console.WriteLine($"  [{label}]  pi = {pi:F18}  " +
                          $"diff = {Math.Abs(pi - Math.PI):E4}  " +
                          $"time = {elapsed.TotalSeconds:F3}s");
    }

    private static void RunThreads(Action<long, long> body)
    {
        long chunkSize = (NumSteps + NumThreads - 1) / NumThreads;
        var threads    = new Thread[NumThreads];
        for (int t = 0; t < NumThreads; t++)
        {
            long s = (long)t * chunkSize;
            long e = Math.Min(s + chunkSize, NumSteps);
            threads[t] = new Thread(() => body(s, e));
        }
        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();
    }
}
