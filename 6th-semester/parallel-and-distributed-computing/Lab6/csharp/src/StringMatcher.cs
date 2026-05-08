using System.Collections.Concurrent;
using System.Diagnostics;

namespace Lab6;

/// <summary>
/// Brute-force substring search, sequential then parallel.
///
/// Given text T (length n) and pattern P (length m), checks every starting
/// position j in [0, n-m) to see whether T[j..j+m-1] == P.
///
/// Parallel variant: partitions the position range across threads.
/// Matches are collected in a <see cref="ConcurrentBag{T}"/> which is
/// thread-safe for concurrent adds.
/// </summary>
internal static class StringMatcher
{
    private const int NumThreads = 4;

    // Synthetic text of 1 M characters with known occurrences of the pattern.
    private static readonly string Text    = BuildText(1_000_000);
    private static readonly string Pattern = "hello";

    public static void Run()
    {
        // ── Sequential ────────────────────────────────────────────────────────
        var sw     = Stopwatch.StartNew();
        var seqHits = SearchSequential(Text, Pattern);
        sw.Stop();
        Console.WriteLine($"  Sequential : {sw.ElapsedMilliseconds,6} ms  " +
                          $"matches: {seqHits.Count}");

        // ── Parallel ──────────────────────────────────────────────────────────
        sw.Restart();
        var parHits = SearchParallel(Text, Pattern, NumThreads);
        sw.Stop();
        Console.WriteLine($"  Parallel   : {sw.ElapsedMilliseconds,6} ms  " +
                          $"matches: {parHits.Count}  ({NumThreads} threads)");
    }

    // ── implementations ───────────────────────────────────────────────────────

    private static List<int> SearchSequential(string text, string pattern)
    {
        var hits = new List<int>();
        int n = text.Length, m = pattern.Length;

        for (int j = 0; j <= n - m; j++)
        {
            int i;
            for (i = 0; i < m && pattern[i] == text[j + i]; i++) { }
            if (i >= m) hits.Add(j);
        }
        return hits;
    }

    private static ConcurrentBag<int> SearchParallel(string text, string pattern, int numThreads)
    {
        var hits      = new ConcurrentBag<int>();
        int n         = text.Length, m = pattern.Length;
        int positions = n - m + 1;
        int chunk     = (positions + numThreads - 1) / numThreads;
        var threads   = new Thread[numThreads];

        for (int t = 0; t < numThreads; t++)
        {
            int start = t * chunk;
            int end   = Math.Min(start + chunk, positions);
            threads[t] = new Thread(() =>
            {
                for (int j = start; j < end; j++)
                {
                    int i;
                    for (i = 0; i < m && pattern[i] == text[j + i]; i++) { }
                    if (i >= m) hits.Add(j);
                }
            });
        }

        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();
        return hits;
    }

    // ── helper ────────────────────────────────────────────────────────────────

    private static string BuildText(int length)
    {
        // Fill with 'a' and sprinkle "hello" every 10 000 characters
        var buf = new char[length];
        System.Array.Fill(buf, 'a');
        for (int pos = 0; pos + 5 <= length; pos += 10_000)
        {
            buf[pos]     = 'h';
            buf[pos + 1] = 'e';
            buf[pos + 2] = 'l';
            buf[pos + 3] = 'l';
            buf[pos + 4] = 'o';
        }
        return new string(buf);
    }
}
