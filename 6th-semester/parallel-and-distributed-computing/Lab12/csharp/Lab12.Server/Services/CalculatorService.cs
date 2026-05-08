using Grpc.Core;

namespace Lab12.Server.Services;

/// <summary>
/// gRPC implementation of the Calculator service.
///
/// All four operations delegate to simple arithmetic; Divide returns an
/// error field in the reply (rather than throwing) when the divisor is zero,
/// keeping the RPC successful at the transport level.
/// </summary>
public sealed class CalculatorService : Calculator.CalculatorBase
{
    public override Task<NumberReply> Add(BinaryRequest request, ServerCallContext context) =>
        Task.FromResult(new NumberReply { Result = request.A + request.B });

    public override Task<NumberReply> Subtract(BinaryRequest request, ServerCallContext context) =>
        Task.FromResult(new NumberReply { Result = request.A - request.B });

    public override Task<NumberReply> Multiply(BinaryRequest request, ServerCallContext context) =>
        Task.FromResult(new NumberReply { Result = request.A * request.B });

    public override Task<NumberReply> Divide(BinaryRequest request, ServerCallContext context)
    {
        if (request.B == 0)
            return Task.FromResult(new NumberReply { Error = "Division by zero" });

        return Task.FromResult(new NumberReply { Result = request.A / request.B });
    }
}
