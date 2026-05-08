namespace Lab1;

/// <summary>
/// Prints a greeting message that includes the worker's name and the current managed thread id.
/// Demonstrates a thread class with a named-parameter constructor.
/// </summary>
internal sealed class GreeterWorker : IWorker
{
    private readonly string _name;

    public GreeterWorker(string name) => _name = name;

    public void Execute() =>
        Console.WriteLine(
            $"[Greeter '{_name}'] Hello! Running on thread id={Environment.CurrentManagedThreadId}");
}
