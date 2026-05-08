using System.Diagnostics;

namespace Lab5;

/// <summary>
/// Exercise 2 — Matrix Addition: <c>a[i,j] = b[i,j] + c[i,j]</c>.
///
/// Parallelised by rows: each thread is assigned a contiguous range of rows.
/// Threads never write to the same row, so no synchronisation is needed.
/// </summary>
internal static class MatrixAdd
{
    private const int Size       = 1_000;
    private const int NumThreads = 4;

    public static void Run()
    {
        double[,] b = new double[Size, Size];
        double[,] c = new double[Size, Size];
        for (int i = 0; i < Size; i++)
            for (int j = 0; j < Size; j++) { b[i, j] = 0.3; c[i, j] = 0.5; }

        // ── Sequential ────────────────────────────────────────────────────────
        double[,] aSeq = new double[Size, Size];
        var sw = Stopwatch.StartNew();
        for (int i = 0; i < Size; i++)
            for (int j = 0; j < Size; j++)
                aSeq[i, j] = b[i, j] + c[i, j];
        sw.Stop();
        Console.WriteLine($"  Sequential : {sw.ElapsedMilliseconds,6} ms  " +
                          $"a[0,0]={aSeq[0, 0]:F1}");

        // ── Parallel (row partitioning) ───────────────────────────────────────
        double[,] aPar = new double[Size, Size];
        sw.Restart();
        ParallelRunner.For(Size, NumThreads, (startRow, endRow) =>
        {
            for (int i = startRow; i < endRow; i++)
                for (int j = 0; j < Size; j++)
                    aPar[i, j] = b[i, j] + c[i, j];
        });
        sw.Stop();
        Console.WriteLine($"  Parallel   : {sw.ElapsedMilliseconds,6} ms  " +
                          $"a[0,0]={aPar[0, 0]:F1}  ({NumThreads} threads)");
    }
}
