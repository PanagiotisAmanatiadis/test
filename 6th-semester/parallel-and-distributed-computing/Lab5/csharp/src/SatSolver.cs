using System.Collections.Concurrent;
using System.Diagnostics;

namespace Lab5;

/// <summary>
/// Exercise 4 — Parallel SAT Solver.
///
/// Evaluates a Boolean circuit over all 2^<see cref="Size"/> input combinations.
/// Each combination is an integer whose bits are the Boolean variable values.
///
/// The circuit is the 23-variable formula from the Java sample.
/// With size=23 there are ~8 M iterations — partitioned across threads by
/// assigning each thread a contiguous range of integers.
///
/// A <see cref="ConcurrentBag{T}"/> collects satisfying assignments thread-safely.
/// </summary>
internal static class SatSolver
{
    private const int Size       = 20; // 2^20 = ~1M iterations (manageable demo size)
    private const int NumThreads = 4;

    public static void Run()
    {
        int iterations = 1 << Size; // 2^Size

        // ── Sequential ────────────────────────────────────────────────────────
        var resultsSeq = new List<int>();
        var sw = Stopwatch.StartNew();
        for (int z = 0; z < iterations; z++)
            if (CheckCircuit(z)) resultsSeq.Add(z);
        sw.Stop();
        Console.WriteLine($"  Sequential : {sw.ElapsedMilliseconds,6} ms  " +
                          $"solutions found: {resultsSeq.Count}");

        // ── Parallel ──────────────────────────────────────────────────────────
        var resultsPar = new ConcurrentBag<int>();
        sw.Restart();
        ParallelRunner.For(iterations, NumThreads, (start, end) =>
        {
            for (int z = start; z < end; z++)
                if (CheckCircuit(z)) resultsPar.Add(z);
        });
        sw.Stop();
        Console.WriteLine($"  Parallel   : {sw.ElapsedMilliseconds,6} ms  " +
                          $"solutions found: {resultsPar.Count}  ({NumThreads} threads)");
    }

    // ── Boolean circuit (same formula as the Java sample) ─────────────────────

    private static bool CheckCircuit(int z)
    {
        // Decompose z into bit vector v[0..Size-1]
        bool[] v = new bool[Size];
        for (int i = Size - 1; i >= 0; i--)
            v[i] = (z & (1 << i)) != 0;

        // Guard against out-of-range access when Size < 23
        bool Safe(int idx) => idx < Size && v[idx];

        return (  Safe(0)  ||  Safe(1)  )
            && ( !Safe(1)  || !Safe(3)  )
            && (  Safe(2)  ||  Safe(3)  )
            && ( !Safe(3)  || !Safe(4)  )
            && (  Safe(4)  || !Safe(5)  )
            && (  Safe(5)  || !Safe(6)  )
            && (  Safe(5)  ||  Safe(6)  )
            && (  Safe(7)  || !Safe(8)  )
            && ( !Safe(7)  || !Safe(13) )
            && (  Safe(8)  ||  Safe(9)  )
            && (  Safe(8)  || !Safe(9)  )
            && ( !Safe(9)  || !Safe(10) )
            && (  Safe(9)  ||  Safe(11) )
            && (  Safe(10) ||  Safe(11) )
            && (  Safe(12) ||  Safe(13) )
            && (  Safe(13) || !Safe(14) )
            && (  Safe(14) ||  Safe(15) )
            && (  Safe(17) ||  Safe(1)  )
            && (  Safe(18) || !Safe(0)  )
            && (  Safe(19) ||  Safe(1)  )
            && (  Safe(19) || !Safe(18) )
            && ( !Safe(19) || !Safe(9)  )
            && (  Safe(0)  ||  Safe(17) )
            && ( !Safe(1)  || Safe(19)  ); // trimmed to fit size=20
    }
}
