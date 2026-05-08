namespace KnuthSolver.Services;

/// <summary>Result returned by a search algorithm.</summary>
/// <param name="Moves">Sequence of move names recorded during exploration (first entry is "" for the root node).</param>
/// <param name="Elapsed">Wall-clock time taken by the search.</param>
/// <param name="Solved">Whether the goal was reached within the time limit.</param>
internal sealed record SearchResult(
    IReadOnlyList<string> Moves,
    TimeSpan Elapsed,
    bool Solved
);
