using System.Diagnostics;

namespace Lab5;

/// <summary>
/// Exercise 1 — Vector Addition: <c>a[i] = b[i] + c[i]</c>.
///
/// Sequential: single loop over all elements.
/// Parallel: the index range is partitioned among <see cref="NumThreads"/> threads;
///   each thread adds its assigned slice independently (no shared writes).
/// </summary>
internal static class VectorAdd
{
    private const int Size       = 1_000_000;
    private const int NumThreads = 4;

    public static void Run()
    {
        double[] b = new double[Size];
        double[] c = new double[Size];
        for (int i = 0; i < Size; i++) { b[i] = 1.0; c[i] = 0.5; }

        // ── Sequential ────────────────────────────────────────────────────────
        double[] aSeq = new double[Size];
        var sw = Stopwatch.StartNew();
        for (int i = 0; i < Size; i++) aSeq[i] = b[i] + c[i];
        sw.Stop();
        Console.WriteLine($"  Sequential : {sw.ElapsedMilliseconds,6} ms  " +
                          $"a[0]={aSeq[0]:F1}  a[{Size-1}]={aSeq[Size-1]:F1}");

        // ── Parallel ──────────────────────────────────────────────────────────
        double[] aPar = new double[Size];
        sw.Restart();
        ParallelRunner.For(Size, NumThreads, (start, end) =>
        {
            for (int i = start; i < end; i++) aPar[i] = b[i] + c[i];
        });
        sw.Stop();
        Console.WriteLine($"  Parallel   : {sw.ElapsedMilliseconds,6} ms  " +
                          $"a[0]={aPar[0]:F1}  a[{Size-1}]={aPar[Size-1]:F1}  " +
                          $"({NumThreads} threads)");
    }
}
