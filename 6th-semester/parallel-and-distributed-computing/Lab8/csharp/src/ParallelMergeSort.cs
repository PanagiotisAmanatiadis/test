using System.Diagnostics;

namespace Lab8;

/// <summary>
/// Exercise 2 — Parallel Merge Sort.
///
/// Divide-and-conquer merge sort where the two halves are sorted
/// concurrently up to a configurable recursion depth.  Beyond
/// <see cref="MaxParallelDepth"/> the algorithm falls back to sequential
/// sorting to prevent thread-creation overhead from dominating.
///
/// The merge step remains sequential (in-place merging two sorted halves).
/// </summary>
internal static class ParallelMergeSort
{
    private const int MaxParallelDepth = 3; // creates up to 2^MaxParallelDepth = 8 threads

    public static void Run()
    {
        const int N = 4_000_000;
        int[] original = GenerateArray(N, seed: 42);

        // ── Sequential ────────────────────────────────────────────────────────
        int[] arr1 = (int[])original.Clone();
        var sw = Stopwatch.StartNew();
        SequentialSort(arr1, 0, arr1.Length - 1);
        sw.Stop();
        Console.WriteLine($"  Sequential   : {sw.ElapsedMilliseconds,6} ms  " +
                          $"sorted={IsSorted(arr1)}  arr[0]={arr1[0]}  arr[^1]={arr1[^1]}");

        // ── Parallel ──────────────────────────────────────────────────────────
        int[] arr2 = (int[])original.Clone();
        sw.Restart();
        ParallelSort(arr2, 0, arr2.Length - 1, depth: 0);
        sw.Stop();
        Console.WriteLine($"  Parallel     : {sw.ElapsedMilliseconds,6} ms  " +
                          $"sorted={IsSorted(arr2)}  arr[0]={arr2[0]}  arr[^1]={arr2[^1]}  " +
                          $"(max depth={MaxParallelDepth})");
    }

    // ── Sequential merge sort ─────────────────────────────────────────────────

    private static void SequentialSort(int[] arr, int l, int r)
    {
        if (l >= r) return;
        int m = l + (r - l) / 2;
        SequentialSort(arr, l, m);
        SequentialSort(arr, m + 1, r);
        Merge(arr, l, m, r);
    }

    // ── Parallel merge sort ───────────────────────────────────────────────────

    private static void ParallelSort(int[] arr, int l, int r, int depth)
    {
        if (l >= r) return;

        int m = l + (r - l) / 2;

        if (depth < MaxParallelDepth)
        {
            // Sort right half on a new thread
            var t = new Thread(() => ParallelSort(arr, m + 1, r, depth + 1));
            t.Start();

            // Sort left half on this thread
            ParallelSort(arr, l, m, depth + 1);

            t.Join();
        }
        else
        {
            // Past the parallel depth — go sequential
            SequentialSort(arr, l, m);
            SequentialSort(arr, m + 1, r);
        }

        Merge(arr, l, m, r);
    }

    // ── Merge two sorted halves arr[l..m] and arr[m+1..r] ────────────────────

    private static void Merge(int[] arr, int l, int m, int r)
    {
        int n1 = m - l + 1, n2 = r - m;
        int[] left  = arr[l..(m + 1)];
        int[] right = arr[(m + 1)..(r + 1)];

        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2)
            arr[k++] = left[i] <= right[j] ? left[i++] : right[j++];
        while (i < n1) arr[k++] = left[i++];
        while (j < n2) arr[k++] = right[j++];
    }

    // ── helpers ───────────────────────────────────────────────────────────────

    private static int[] GenerateArray(int n, int seed)
    {
        var rng = new Random(seed);
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = rng.Next();
        return arr;
    }

    private static bool IsSorted(int[] arr)
    {
        for (int i = 1; i < arr.Length; i++)
            if (arr[i] < arr[i - 1]) return false;
        return true;
    }
}
