/*
 * Lab 8 — Divide-and-Conquer Parallelism (C# / .NET 8)
 *
 * Exercise 1 — Pi via recursive divide-and-conquer
 *   Integration range [0,1] is recursively split in half.
 *   Each half is computed on a new thread until the sub-range falls below
 *   SequentialThreshold steps, at which point the computation goes sequential.
 *   No shared state between threads — results combined at each join point.
 *
 * Exercise 2 — Parallel Merge Sort
 *   Two halves of the array are sorted concurrently up to MaxParallelDepth
 *   recursive levels (creating ≤ 2^MaxParallelDepth threads).
 *   Below that depth the algorithm reverts to sequential sort to avoid the
 *   overhead of spawning too many tiny threads.
 *   The merge step is always sequential.
 */

using Lab8;

Section("Exercise 1 — Pi via divide-and-conquer integration  (10 M steps)");
PiDivideConquer.Run();

Section("Exercise 2 — Parallel Merge Sort  (4 M integers)");
ParallelMergeSort.Run();

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}
