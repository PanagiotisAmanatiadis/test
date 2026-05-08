namespace Lab2;

/// <summary>
/// Holds the shared array and optional index counter used across all exercises.
/// Passing this object to threads demonstrates sharing state via a constructor argument
/// rather than relying on static/global fields.
/// </summary>
internal sealed class SharedArrayState
{
    public int[] Array   { get; }
    public int   Counter { get; set; }
    public int   End     { get; }

    public SharedArrayState(int end)
    {
        End     = end;
        Array   = new int[end];
        Counter = 0;
    }

    /// <summary>
    /// Verifies that every cell equals <paramref name="expectedMultiplier"/> × its index.
    /// </summary>
    public int CheckForLoop(int expectedMultiplier)
    {
        int errors = 0;
        for (int i = 0; i < End; i++)
        {
            int expected = expectedMultiplier * i;
            if (Array[i] != expected)
            {
                errors++;
                if (errors <= 5) // print at most 5 sample errors
                    Console.WriteLine($"  index {i,5}: got {Array[i],6}, expected {expected,6}");
            }
        }
        return errors;
    }

    /// <summary>
    /// Verifies that every cell equals exactly 1 (written exactly once).
    /// </summary>
    public int CheckWhileLoop()
    {
        int errors = 0;
        for (int i = 0; i < End; i++)
        {
            if (Array[i] != 1)
            {
                errors++;
                if (errors <= 5)
                    Console.WriteLine($"  index {i,5}: got {Array[i],6}, expected 1");
            }
        }
        return errors;
    }

    /// <summary>Resets the array and counter for a fresh run.</summary>
    public void Reset()
    {
        System.Array.Clear(Array, 0, End);
        Counter = 0;
    }
}
