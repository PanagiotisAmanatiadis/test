# Lab 12 — gRPC Distributed Services

Implements two gRPC services hosted in an ASP.NET Core server, with a separate
console client that exercises both services concurrently.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Project Structure

```
csharp/
├── Lab12.sln
├── Lab12.Server/
│   ├── Protos/
│   │   ├── calculator.proto   # four-function calculator service definition
│   │   └── emailstore.proto   # thread-safe email store service definition
│   ├── Services/
│   │   ├── CalculatorService.cs
│   │   └── EmailStoreService.cs
│   ├── Program.cs             # registers services on http://localhost:5050
│   └── appsettings.json
└── Lab12.Client/
    ├── Protos/                # same .proto files (generates client stubs)
    └── Program.cs             # runs calculator and email store demos
```

## Services

### Calculator

```protobuf
service Calculator {
  rpc Add      (BinaryRequest) returns (NumberReply);
  rpc Subtract (BinaryRequest) returns (NumberReply);
  rpc Multiply (BinaryRequest) returns (NumberReply);
  rpc Divide   (BinaryRequest) returns (NumberReply);
}
```

Division by zero returns a populated `error` field instead of throwing,
keeping the RPC transport-level result successful.

### EmailStore

```protobuf
service EmailStore {
  rpc Send     (SendRequest)  returns (SendReply);
  rpc GetAll   (GetRequest)   returns (GetReply);
  rpc GetInbox (InboxRequest) returns (GetReply);
}
```

- **Thread safety**: `ConcurrentDictionary<int, EmailMessage>` + `Interlocked.Increment` for the ID counter — no `lock` needed.
- The client demo sends 4 emails concurrently via `Task.WhenAll` to exercise concurrent server access.

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps

**Terminal 1 — start the server:**
```bash
cd Lab12/csharp/Lab12.Server
dotnet run
```

**Terminal 2 — run the client:**
```bash
cd Lab12/csharp/Lab12.Client
dotnet run
```

## Key Concepts

| Concept | Detail |
|---------|--------|
| Protocol Buffers | `.proto` files define service contracts; `Grpc.Tools` generates C# stubs at build time |
| `GrpcChannel` | Single long-lived channel; multiplexes all RPCs over one HTTP/2 connection |
| `ConcurrentDictionary` | Lock-free concurrent email store |
| `Interlocked.Increment` | Atomic, lock-free ID generation |
| `Task.WhenAll` | Sends multiple RPCs concurrently from the client |
