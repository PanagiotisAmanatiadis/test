/*
 * Lab 2 — Shared Variables & Race Conditions (C# / .NET 8)
 *
 * Demonstrates three sharing strategies (global static / constructor args / shared object)
 * combined with two synchronisation modes (unsafe vs. lock) across two exercise patterns:
 *
 *   Exercise 1 — For-loop array counter
 *     N threads each iterate 0..End-1 and increment array[i] exactly i times.
 *     Expected after all threads finish: array[i] == N × i.
 *     Unsafe → race condition → errors.
 *     Safe   → lock on every increment → 0 errors.
 *
 *   Exercise 2 — While-loop index counter
 *     Threads share a global index; each claims one cell and writes to it once.
 *     Expected: every cell == 1.
 *     Unsafe → race condition → errors (cells missed or double-written).
 *     Safe   → lock wraps the read-check-write-increment → 0 errors.
 *
 * Sharing strategies illustrated:
 *   • Global static fields      — accessed directly by thread methods (ForLoop variants)
 *   • Constructor arguments     — state passed at thread creation time (WhileLoop variants)
 *   • Shared object reference   — single SharedArrayState instance shared by all workers
 *     (both exercises use the same SharedArrayState object, showing all three approaches)
 */

using Lab2;

const int End        = 1000;
const int NumThreads = 4;

Section("Exercise 1 — For-loop  |  UNSAFE (race condition expected)");
RunForLoop(safe: false);

Section("Exercise 1 — For-loop  |  SAFE   (lock on every increment)");
RunForLoop(safe: true);

Section("Exercise 2 — While-loop  |  UNSAFE (race condition expected)");
RunWhileLoop(safe: false);

Section("Exercise 2 — While-loop  |  SAFE   (lock on index claim)");
RunWhileLoop(safe: true);

// ── helpers ───────────────────────────────────────────────────────────────────

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}

static void RunForLoop(bool safe)
{
    var state   = new SharedArrayState(End);
    var mutex   = new object();
    var threads = new Thread[NumThreads];

    for (int i = 0; i < NumThreads; i++)
    {
        if (safe)
        {
            var worker = new ForLoopWorker.Safe(state, mutex);
            threads[i] = new Thread(worker.Run);
        }
        else
        {
            var worker = new ForLoopWorker.Unsafe(state);
            threads[i] = new Thread(worker.Run);
        }
    }

    foreach (var t in threads) t.Start();
    foreach (var t in threads) t.Join();

    int errors = state.CheckForLoop(expectedMultiplier: NumThreads);
    Console.WriteLine($"Checking...  {errors} error(s).  " +
                      (errors == 0 ? "PASS" : "FAIL — race condition detected"));
}

static void RunWhileLoop(bool safe)
{
    var state   = new SharedArrayState(End);
    var mutex   = new object();
    var threads = new Thread[NumThreads];

    for (int i = 0; i < NumThreads; i++)
    {
        if (safe)
        {
            var worker = new WhileLoopWorker.Safe(state, mutex);
            threads[i] = new Thread(worker.Run);
        }
        else
        {
            var worker = new WhileLoopWorker.Unsafe(state);
            threads[i] = new Thread(worker.Run);
        }
    }

    foreach (var t in threads) t.Start();
    foreach (var t in threads) t.Join();

    int errors = state.CheckWhileLoop();
    Console.WriteLine($"Checking...  {errors} error(s).  " +
                      (errors == 0 ? "PASS" : "FAIL — race condition detected"));
}
