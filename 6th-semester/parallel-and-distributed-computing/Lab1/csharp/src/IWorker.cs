namespace Lab1;

/// <summary>
/// Common contract for all thread worker types.
/// Enables polymorphism: both <see cref="GreeterWorker"/> and <see cref="CounterWorker"/>
/// can be stored in the same array and started uniformly.
/// </summary>
internal interface IWorker
{
    void Execute();
}
