using System.Collections.Concurrent;

namespace Lab4.ProducerConsumer;

/// <summary>
/// Consumes messages from the bounded <see cref="BlockingCollection{T}"/>.
/// Blocks when the queue is empty and exits automatically once the producer
/// calls <c>CompleteAdding()</c> and the queue has been drained.
/// </summary>
internal sealed class Consumer
{
    private readonly BlockingCollection<Message> _queue;

    public Consumer(BlockingCollection<Message> queue) => _queue = queue;

    public void Run()
    {
        // GetConsumingEnumerable() blocks on empty and stops when CompleteAdding() is called.
        foreach (var msg in _queue.GetConsumingEnumerable())
        {
            Thread.Sleep(10); // simulate processing time
            Console.WriteLine($"  Consumed  {msg.Text,3}");
        }
    }
}
