namespace Lab2;

/// <summary>
/// Exercise 1 — for-loop pattern: each thread loops over every index 0..End-1
/// and increments <c>array[i]</c> exactly <c>i</c> times.
///
/// After all <c>N</c> threads finish, the expected value at each index is <c>N × i</c>.
///
/// <list type="bullet">
///   <item><see cref="Unsafe"/> — no synchronisation; demonstrates a race condition.</item>
///   <item><see cref="Safe"/>   — uses <c>lock</c>; guarantees the correct result.</item>
/// </list>
/// </summary>
internal static class ForLoopWorker
{
    // ── Unsafe variant ───────────────────────────────────────────────────────

    internal sealed class Unsafe
    {
        private readonly SharedArrayState _state;

        public Unsafe(SharedArrayState state) => _state = state;

        public void Run()
        {
            for (int i = 0; i < _state.End; i++)
                for (int j = 0; j < i; j++)
                    _state.Array[i]++; // ← unsynchronised — race condition possible
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
            for (int i = 0; i < _state.End; i++)
                for (int j = 0; j < i; j++)
                    lock (_mutex)
                        _state.Array[i]++; // ← protected — no race condition
        }
    }
}
