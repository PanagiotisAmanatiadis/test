/*
 * Lab 3 — Mutual Exclusion (C# / .NET 8)
 *
 * Exercise 1 — Coarse-grained locking
 *   A single mutex guards the whole shared array.
 *   Simple and correct, but all threads serialise on one lock.
 *
 * Exercise 2 — Fine-grained locking
 *   One lock per array element.  Threads operating on different elements
 *   run truly in parallel; only collisions on the same element serialise.
 *   Better throughput than coarse-grained, equally correct.
 *
 * Exercise 3 — Dining Philosophers (deadlock-free)
 *   Classic five-philosopher problem solved with resource ordering:
 *   philosopher N-1 picks up the right fork before the left, breaking
 *   the circular wait that would otherwise cause deadlock.
 */

using Lab3;

const int Size       = 500;
const int NumThreads = 4;

// ── Exercise 1: Coarse-grained lock ──────────────────────────────────────────

Section("Exercise 1 — Coarse-grained locking (single mutex)");

var coarse  = new CoarseLockCounter(Size, NumThreads);
var tCoarse = StartAndJoin(NumThreads, coarse.Run);

int e1 = coarse.Verify();
Console.WriteLine($"Checking...  {e1} error(s).  {(e1 == 0 ? "PASS" : "FAIL")}");

// ── Exercise 2: Fine-grained locking ─────────────────────────────────────────

Section("Exercise 2 — Fine-grained locking (per-element mutex)");

var fine  = new FineLockCounter(Size, NumThreads);
var tFine = StartAndJoin(NumThreads, fine.Run);

int e2 = fine.Verify();
Console.WriteLine($"Checking...  {e2} error(s).  {(e2 == 0 ? "PASS" : "FAIL")}");

// ── Exercise 3: Dining Philosophers ──────────────────────────────────────────

Section("Exercise 3 — Dining Philosophers (resource-ordering, deadlock-free)");
new DiningPhilosophers(n: 5).Run();

// ── helpers ───────────────────────────────────────────────────────────────────

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}

static Thread[] StartAndJoin(int n, ThreadStart body)
{
    var threads = new Thread[n];
    for (int i = 0; i < n; i++) threads[i] = new Thread(body);
    foreach (var t in threads) t.Start();
    foreach (var t in threads) t.Join();
    return threads;
}
