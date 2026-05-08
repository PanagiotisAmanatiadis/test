using Grpc.Core;
using System.Collections.Concurrent;

namespace Lab12.Server.Services;

/// <summary>
/// gRPC implementation of the EmailStore service.
///
/// Emails are stored in a <see cref="ConcurrentDictionary{TKey,TValue}"/> so
/// that concurrent RPC calls from multiple clients do not corrupt the store.
/// The auto-incrementing message id uses <see cref="Interlocked.Increment"/>
/// for a lock-free, thread-safe counter.
///
/// Demonstrates that a gRPC service is invoked on multiple threads
/// simultaneously and must protect any shared mutable state.
/// </summary>
public sealed class EmailStoreService : EmailStore.EmailStoreBase
{
    private readonly ConcurrentDictionary<int, EmailMessage> _store = new();
    private int _nextId = 0;

    public override Task<SendReply> Send(SendRequest request, ServerCallContext context)
    {
        int id = Interlocked.Increment(ref _nextId);
        var msg = new EmailMessage
        {
            Id      = id,
            From    = request.From,
            To      = request.To,
            Subject = request.Subject,
            Body    = request.Body
        };
        _store[id] = msg;
        Console.WriteLine($"[EmailStore] Stored email #{id}: '{request.Subject}' from {request.From} to {request.To}");
        return Task.FromResult(new SendReply { Id = id });
    }

    public override Task<GetReply> GetAll(GetRequest request, ServerCallContext context)
    {
        var reply = new GetReply();
        reply.Messages.AddRange(_store.Values.OrderBy(m => m.Id));
        return Task.FromResult(reply);
    }

    public override Task<GetReply> GetInbox(InboxRequest request, ServerCallContext context)
    {
        var reply = new GetReply();
        reply.Messages.AddRange(
            _store.Values
                  .Where(m => m.To.Equals(request.Recipient, StringComparison.OrdinalIgnoreCase))
                  .OrderBy(m => m.Id));
        return Task.FromResult(reply);
    }
}
