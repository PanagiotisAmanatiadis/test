/*
 * Lab 1 — Introduction to Threads (C# / .NET 8)
 *
 * Q1 Observation
 * ──────────────
 * Without storing Thread references in a data structure (array/list) we cannot
 * call Join() on them — the Thread object would be unreachable and we lose the
 * ability to wait for thread completion. Threads still execute (they are
 * foreground threads by default), but the main thread may exit before they
 * finish, causing the process to terminate abruptly.
 *
 * Q2  Two threads from two different worker classes.
 * Q3  Ten instances of each class running concurrently (20 threads total).
 * Q4  Ten threads, each printing the first 20 multiples of a unique multiplier.
 *     Isolated observation: each thread's output is in ascending order.
 *     Concurrent observation: output lines from all 10 threads interleave
 *     non-deterministically because the OS scheduler decides execution order.
 */

using Lab1;

Section("Exercise 2 — Two threads from different classes");
RunExercise2();

Section("Exercise 3 — Ten threads from each class (20 total)");
RunExercise3();

Section("Exercise 4 — Ten threads printing 20 multiples each");
RunExercise4();

// ── helpers ───────────────────────────────────────────────────────────────────

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}

static void RunExercise2()
{
    // IWorker enables polymorphism: both worker types share the same start/join pattern.
    var t1 = new Thread(new GreeterWorker("Alpha").Execute);
    var t2 = new Thread(new CounterWorker("Beta", limit: 5).Execute);

    t1.Start(); t2.Start();
    t1.Join();  t2.Join();
}

static void RunExercise3()
{
    const int N = 10;
    var greeters = new Thread[N];
    var counters  = new Thread[N];

    for (int i = 0; i < N; i++)
    {
        greeters[i] = new Thread(new GreeterWorker($"G{i}").Execute);
        counters[i]  = new Thread(new CounterWorker($"C{i}", limit: 3).Execute);
    }

    foreach (var t in greeters) t.Start();
    foreach (var t in counters)  t.Start();
    foreach (var t in greeters) t.Join();
    foreach (var t in counters)  t.Join();
}

static void RunExercise4()
{
    const int N = 10;
    var threads = new Thread[N];

    for (int i = 0; i < N; i++)
    {
        var worker = new MultiplesWorker(multiplier: i + 1, count: 20);
        threads[i] = new Thread(worker.Execute);
    }

    foreach (var t in threads) t.Start();
    foreach (var t in threads) t.Join();

    Console.WriteLine(
        "\n[Observation] Output lines above are interleaved non-deterministically " +
        "because the OS scheduler decides which thread runs at each moment.");
}
