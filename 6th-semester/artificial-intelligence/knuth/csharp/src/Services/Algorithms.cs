using Microsoft.Extensions.Logging;
using KnuthSolver.Models;

namespace KnuthSolver.Services;

/// <summary>
/// Search algorithms for Knuth's conjecture.
///
/// Both algorithms start from state 4 and apply factorial, square root, and
/// floor operations to reach a user-specified target integer.
/// </summary>
internal sealed class Algorithms
{
    private static readonly TimeSpan BfsTimeLimit = TimeSpan.FromSeconds(60);
    private static readonly TimeSpan IdTimeLimit  = TimeSpan.FromSeconds(30);

    private readonly ILogger<Algorithms> _logger;

    public Algorithms(ILogger<Algorithms> logger) => _logger = logger;

    /// <summary>
    /// Breadth-First Search (time limit: 60 s).
    ///
    /// Records the move of every node dequeued, so <see cref="SearchResult.Moves"/>
    /// reflects the exploration order, not a path from root to goal.
    /// </summary>
    public SearchResult BreadthFirstSearch(SearchNode root, double goal)
    {
        _logger.LogInformation("BFS started — goal: {Goal}", goal);
        var start  = DateTime.UtcNow;
        var queue  = new Queue<SearchNode>();
        var moves  = new List<string>();

        queue.Enqueue(root);

        while (queue.Count > 0 && DateTime.UtcNow - start < BfsTimeLimit)
        {
            var node = queue.Dequeue();
            moves.Add(node.Move);

            if (node.IsGoal(goal))
            {
                var elapsed = DateTime.UtcNow - start;
                _logger.LogInformation("BFS solved in {Ms} ms after exploring {Nodes} nodes.",
                    (long)elapsed.TotalMilliseconds, moves.Count);
                return new SearchResult(moves, elapsed, Solved: true);
            }

            node.ExpandNode();
            foreach (var child in node.Children)
                queue.Enqueue(child);
        }

        var timeout = DateTime.UtcNow - start;
        _logger.LogWarning("BFS failed to find {Goal} within {Limit}.", goal, BfsTimeLimit);
        return new SearchResult(moves, timeout, Solved: false);
    }

    /// <summary>
    /// Iterative Deepening DFS (time limit: 30 s).
    ///
    /// Repeatedly performs depth-limited DFS with increasing depth limits until
    /// the goal is found or the time limit is exceeded.
    /// </summary>
    public SearchResult IterativeDeepening(SearchNode root, double goal)
    {
        _logger.LogInformation("Iterative Deepening started — goal: {Goal}", goal);
        var start      = DateTime.UtcNow;
        int depthLimit = 1;

        while (DateTime.UtcNow - start < IdTimeLimit)
        {
            var result = DepthLimitedSearch(root, goal, depthLimit, start);
            if (result.Solved)
            {
                _logger.LogInformation("ID solved at depth {Depth} in {Ms} ms ({Nodes} nodes explored).",
                    depthLimit, (long)result.Elapsed.TotalMilliseconds, result.Moves.Count);
                return result;
            }
            depthLimit++;
        }

        var timeout = DateTime.UtcNow - start;
        _logger.LogWarning("Iterative Deepening failed to find {Goal} within {Limit}.", goal, IdTimeLimit);
        return new SearchResult([], timeout, Solved: false);
    }

    // ── private ───────────────────────────────────────────────────────────────

    private SearchResult DepthLimitedSearch(
        SearchNode root, double goal, int depthLimit, DateTime start)
    {
        var stack = new Stack<SearchNode>();
        var moves = new List<string>();
        stack.Push(root);

        while (stack.Count > 0 && DateTime.UtcNow - start < IdTimeLimit)
        {
            var node = stack.Pop();
            moves.Add(node.Move);

            if (node.IsGoal(goal))
                return new SearchResult(moves, DateTime.UtcNow - start, Solved: true);

            if (node.Depth < depthLimit)
            {
                node.ExpandNode();
                foreach (var child in node.Children)
                    stack.Push(child);
            }
        }

        return new SearchResult(moves, DateTime.UtcNow - start, Solved: false);
    }
}
