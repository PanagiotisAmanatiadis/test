namespace Lab4.ProducerConsumer;

/// <summary>Immutable message passed through the bounded blocking queue.</summary>
internal sealed record Message(string Text);
