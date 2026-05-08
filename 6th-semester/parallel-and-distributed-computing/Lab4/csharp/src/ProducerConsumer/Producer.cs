using System.Collections.Concurrent;

namespace Lab4.ProducerConsumer;

/// <summary>
/// Produces <see cref="Count"/> messages, placing each into the bounded
/// <see cref="BlockingCollection{T}"/>.  After all messages are enqueued the
/// collection is marked complete so the consumer knows when to stop.
///
/// <c>Thread.Sleep(i)</c> mirrors the original Java sample: message 0 is
/// produced immediately, message 99 waits 99 ms — simulating variable
/// production rates.
/// </summary>
internal sealed class Producer
{
    public const int Count = 20; // kept small to avoid very long waits

    private readonly BlockingCollection<Message> _queue;

    public Producer(BlockingCollection<Message> queue) => _queue = queue;

    public void Run()
    {
        for (int i = 0; i < Count; i++)
        {
            Thread.Sleep(i);                          // simulate variable production speed
            var msg = new Message(i.ToString());
            _queue.Add(msg);
            Console.WriteLine($"  Produced  {msg.Text,3}");
        }

        _queue.CompleteAdding(); // signal: no more messages will be added
    }
}
