namespace Lab2;

/// <summary>
/// Exercise 2 — while-loop pattern: threads share a global index counter.
/// Each iteration a thread reads the current index, writes to that cell, then
/// increments the counter.  Each cell should be written exactly once.
///
/// <list type="bullet">
///   <item><see cref="Unsafe"/> — no synchronisation; demonstrates a race condition
///         (two threads can read the same index and both write to the same cell).</item>
///   <item><see cref="Safe"/>   — locks the read-check-write-increment sequence;
///         guarantees each cell is written exactly once.</item>
/// </list>
/// </summary>
internal static class WhileLoopWorker
{
    // ── Unsafe variant ───────────────────────────────────────────────────────

    internal sealed class Unsafe
    {
        private readonly SharedArrayState _state;

        public Unsafe(SharedArrayState state) => _state = state;

        public void Run()
        {
            while (true)
            {
                if (_state.Counter >= _state.End) break;
                // ← race: another thread may read the same Counter value
                _state.Array[_state.Counter]++;
                _state.Counter++;
            }
        }
    }

    // ── Safe variant (lock) ──────────────────────────────────────────────────

    internal sealed class Safe
    {
        private readonly SharedArrayState _state;
        private readonly object           _mutex;

        public Safe(SharedArrayState state, object mutex)
        {
            _state = state;
            _mutex = mutex;
        }

        public void Run()
        {
            while (true)
            {
                lock (_mutex)
                {
                    if (_state.Counter >= _state.End) break;
                    // The entire check-write-increment is atomic under the lock.
                    _state.Array[_state.Counter]++;
                    _state.Counter++;
                }
            }
        }
    }
}
