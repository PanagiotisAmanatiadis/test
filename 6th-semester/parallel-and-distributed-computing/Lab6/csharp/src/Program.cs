/*
 * Lab 6 — Pi Computation & Parallel String Matching (C# / .NET 8)
 *
 * Pi via numerical integration of 4/(1+x²) over [0,1] — three variants:
 *   Variant 1: Sequential — single loop, baseline.
 *   Variant 2: Parallel + shared lock — correct but heavy contention.
 *   Variant 3: Parallel + local reduction — each thread accumulates into its
 *              own array slot; results are summed once after all threads join.
 *              No contention during computation → best performance.
 *
 * Brute-force substring search:
 *   Sequential: O(n·m) scan of a 1 M character text.
 *   Parallel:   position range split across 4 threads; hits go to ConcurrentBag<int>.
 */

using Lab6;

Section("Exercise 1 — Pi computation  (10 M steps)");
PiComputation.Sequential();
PiComputation.SharedLock();
PiComputation.LocalReduction();

Section("Exercise 2 — Brute-force string matching  (1 M chars, pattern \"hello\")");
StringMatcher.Run();

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}
