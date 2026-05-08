namespace Lab3;

/// <summary>
/// Exercise 3 — Dining Philosophers (deadlock-free).
///
/// Five philosophers sit around a table.  Between each adjacent pair lies one
/// fork (five forks total).  To eat, a philosopher must hold both the fork to
/// their left and the fork to their right simultaneously.
///
/// Naive approach (always pick up left fork first) leads to circular waiting
/// and deadlock.  The resource-ordering solution breaks the cycle by making the
/// philosopher with the highest id pick up the RIGHT fork first.
///
/// Each philosopher eats and thinks <see cref="Rounds"/> times, then stops.
/// </summary>
internal sealed class DiningPhilosophers
{
    public const int Rounds = 3;

    private readonly int      _n;
    private readonly object[] _forks;

    public DiningPhilosophers(int n = 5)
    {
        _n     = n;
        _forks = new object[n];
        for (int i = 0; i < n; i++)
            _forks[i] = new object();
    }

    public void Run()
    {
        var threads = new Thread[_n];
        for (int i = 0; i < _n; i++)
        {
            int id = i; // capture loop variable
            threads[i] = new Thread(() => Philosopher(id));
        }

        foreach (var t in threads) t.Start();
        foreach (var t in threads) t.Join();

        Console.WriteLine("All philosophers finished — no deadlock.");
    }

    // ── private ──────────────────────────────────────────────────────────────

    private void Philosopher(int id)
    {
        int left  = id;
        int right = (id + 1) % _n;

        for (int round = 1; round <= Rounds; round++)
        {
            Think(id, round);
            Eat(id, round, left, right);
        }
    }

    private void Think(int id, int round)
    {
        Console.WriteLine($"  Philosopher {id} is thinking  (round {round})");
        Thread.Sleep(Random.Shared.Next(10, 50));
    }

    private void Eat(int id, int round, int left, int right)
    {
        // Resource-ordering: the last philosopher picks up RIGHT before LEFT.
        // This breaks the circular dependency and prevents deadlock.
        int first  = id == _n - 1 ? right : left;
        int second = id == _n - 1 ? left  : right;

        lock (_forks[first])
            lock (_forks[second])
            {
                Console.WriteLine($"  Philosopher {id} is eating    (round {round})");
                Thread.Sleep(Random.Shared.Next(10, 50));
            }
    }
}
