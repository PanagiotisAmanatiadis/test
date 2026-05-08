/*
 * Lab 7 — Histogram, Word Count & Sieve of Eratosthenes (C# / .NET 8)
 *
 * Exercise 1 — Character Histogram
 *   Each thread builds a local frequency array for its slice of text.
 *   After all threads join, local arrays are merged in O(128 × numThreads) time.
 *   No synchronisation during counting.
 *
 * Exercise 2 — Word Count
 *   Threads count words in their slice; boundary words that span two slices
 *   are corrected by decrementing the count when the slice begins mid-word.
 *
 * Exercise 3 — Sieve of Eratosthenes (10 M)
 *   Phase 1 (sequential): mark composites for all primes p ≤ √Limit.
 *   Phase 2 (parallel): three scheduling strategies:
 *     • Static  — divide the remaining range equally once at startup.
 *     • Cyclic  — each thread handles every N-th number (round-robin).
 *     • Dynamic — threads atomically claim fixed-size chunks until done.
 */

using Lab7;

// Build a synthetic text (5 M characters) for exercises 1 and 2
string text = BuildText(5_000_000);

Section("Exercise 1 — Character Histogram  (5 M characters)");
CharHistogram.Run(text);

Section("Exercise 2 — Word Count  (5 M characters)");
WordCount.Run(text);

Section("Exercise 3 — Sieve of Eratosthenes  (limit = 10 M)");
SieveOfEratosthenes.Sequential();
SieveOfEratosthenes.StaticScheduling();
SieveOfEratosthenes.CyclicScheduling();
SieveOfEratosthenes.DynamicScheduling();

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}

static string BuildText(int length)
{
    // Generate readable text: repeating "the quick brown fox " pattern
    const string Word = "the quick brown fox jumps over the lazy dog ";
    var buf = new System.Text.StringBuilder(length);
    while (buf.Length < length)
        buf.Append(Word);
    return buf.ToString(0, length);
}
