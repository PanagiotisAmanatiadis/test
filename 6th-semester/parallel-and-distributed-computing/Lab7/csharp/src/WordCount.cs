using System.Diagnostics;

namespace Lab7;

/// <summary>
/// Exercise 2 — Parallel word count.
///
/// Counts the total number of words in a text (words separated by whitespace).
/// A word boundary is detected at any character that transitions from a
/// non-space to a space (or end of the chunk).
///
/// Each thread counts words in its slice.  Slice boundaries that split a
/// word between two threads are handled by checking whether the first
/// character of the slice continues a word started in the previous slice.
/// </summary>
internal static class WordCount
{
    private const int NumThreads = 4;

    public static void Run(string text)
    {
        // ── Sequential ────────────────────────────────────────────────────────
        var sw = Stopwatch.StartNew();
        int seqCount = CountWords(text, 0, text.Length);
        sw.Stop();
        Console.WriteLine($"  Sequential : {sw.ElapsedMilliseconds,6} ms  words={seqCount}");

        // ── Parallel ──────────────────────────────────────────────────────────
        int   chunk   = (text.Length + NumThreads - 1) / NumThreads;
        int[] partial = new int[NumThreads];
        var   threads = new Thread[NumThreads];

        for (int t = 0; t < NumThreads; t++)
        {
            int tid   = t;
            int start = tid * chunk;
            int end   = Math.Min(start + chunk, text.Length);
            threads[t] = new Thread(() =>
            {
                partial[tid] = CountWords(text, start, end);
                // If the slice starts mid-word, subtract 1 to avoid double-counting.
                // (the previous thread will have counted the beginning of that word)
                if (start > 0 && !char.IsWhiteSpace(text[start - 1]) &&
                    !char.IsWhiteSpace(text[start]))
                    partial[tid]--;
            });
        }

        sw.Restart();
        foreach (var th in threads) th.Start();
        foreach (var th in threads) th.Join();

        int parCount = partial.Sum();
        sw.Stop();
        Console.WriteLine($"  Parallel   : {sw.ElapsedMilliseconds,6} ms  words={parCount}  " +
                          $"({NumThreads} threads)");
    }

    private static int CountWords(string text, int start, int end)
    {
        int count    = 0;
        bool inWord  = false;
        for (int i = start; i < end; i++)
        {
            if (!char.IsWhiteSpace(text[i]))
            {
                if (!inWord) { count++; inWord = true; }
            }
            else inWord = false;
        }
        return count;
    }
}
