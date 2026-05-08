using System.Diagnostics;

namespace Lab7;

/// <summary>
/// Exercise 1 — Character frequency histogram.
///
/// Counts how many times each character appears in a large string.
///
/// Sequential: single pass over the text.
/// Parallel: each thread scans its own slice of the text into a local
///   frequency array, then all local arrays are merged into the final result.
///   No contention during counting — merge happens after all threads join.
/// </summary>
internal static class CharHistogram
{
    private const int NumThreads = 4;

    public static void Run(string text)
    {
        // ── Sequential ────────────────────────────────────────────────────────
        int[] seqFreq = new int[128];
        var sw = Stopwatch.StartNew();
        foreach (char c in text)
            if (c < 128) seqFreq[c]++;
        sw.Stop();
        Console.WriteLine($"  Sequential : {sw.ElapsedMilliseconds,6} ms  " +
                          $"'a'={seqFreq['a']}  'e'={seqFreq['e']}  ' '={seqFreq[' ']}");

        // ── Parallel ──────────────────────────────────────────────────────────
        int[][] locals  = new int[NumThreads][];
        for (int t = 0; t < NumThreads; t++) locals[t] = new int[128];

        int chunk   = (text.Length + NumThreads - 1) / NumThreads;
        var threads = new Thread[NumThreads];

        for (int t = 0; t < NumThreads; t++)
        {
            int tid   = t;
            int start = tid * chunk;
            int end   = Math.Min(start + chunk, text.Length);
            threads[t] = new Thread(() =>
            {
                for (int i = start; i < end; i++)
                {
                    char c = text[i];
                    if (c < 128) locals[tid][c]++;
                }
            });
        }

        sw.Restart();
        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();

        // Sequential merge — happens once, no sync needed
        int[] parFreq = new int[128];
        foreach (var local in locals)
            for (int i = 0; i < 128; i++) parFreq[i] += local[i];
        sw.Stop();

        Console.WriteLine($"  Parallel   : {sw.ElapsedMilliseconds,6} ms  " +
                          $"'a'={parFreq['a']}  'e'={parFreq['e']}  ' '={parFreq[' ']}  " +
                          $"({NumThreads} threads)");
    }
}
