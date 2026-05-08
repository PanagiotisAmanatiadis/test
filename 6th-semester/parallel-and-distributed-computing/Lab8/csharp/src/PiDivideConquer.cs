using System.Diagnostics;

namespace Lab8;

/// <summary>
/// Exercise 1 — Pi via divide-and-conquer numerical integration.
///
/// The integration range [0, 1] is recursively split in half.
/// Each half is computed in a new thread until the sub-range contains fewer
/// than <see cref="SequentialThreshold"/> steps, at which point the remainder
/// is computed sequentially.
///
/// This creates a binary task tree with depth log₂(numSteps / threshold).
/// </summary>
internal static class PiDivideConquer
{
    private const long NumSteps           = 10_000_000L;
    private const long SequentialThreshold = 500_000L; // switch to sequential below this

    public static void Run()
    {
        double step = 1.0 / NumSteps;

        // ── Sequential reference ──────────────────────────────────────────────
        var sw = Stopwatch.StartNew();
        double piSeq = Integrate(0, NumSteps, step) * step;
        sw.Stop();
        Console.WriteLine($"  Sequential       : {sw.ElapsedMilliseconds,6} ms  " +
                          $"pi = {piSeq:F15}");

        // ── Divide-and-conquer parallel ───────────────────────────────────────
        sw.Restart();
        double piPar = IntegrateParallel(0, NumSteps, step) * step;
        sw.Stop();
        Console.WriteLine($"  Divide-and-conquer: {sw.ElapsedMilliseconds,6} ms  " +
                          $"pi = {piPar:F15}");
    }

    // ── Sequential integration of steps in [lo, hi) ──────────────────────────

    private static double Integrate(long lo, long hi, double step)
    {
        double sum = 0.0;
        for (long i = lo; i < hi; i++)
        {
            double x = (i + 0.5) * step;
            sum += 4.0 / (1.0 + x * x);
        }
        return sum;
    }

    // ── Parallel divide-and-conquer ───────────────────────────────────────────

    private static double IntegrateParallel(long lo, long hi, double step)
    {
        if (hi - lo <= SequentialThreshold)
            return Integrate(lo, hi, step);

        long mid = (lo + hi) / 2;
        double rightResult = 0.0;

        // Compute right half in a new thread
        var t = new Thread(() => rightResult = IntegrateParallel(mid, hi, step));
        t.Start();

        // Compute left half on this thread
        double leftResult = IntegrateParallel(lo, mid, step);

        t.Join();
        return leftResult + rightResult;
    }
}
