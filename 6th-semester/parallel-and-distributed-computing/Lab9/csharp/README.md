# Lab 9 — TCP Client-Server

Implements distributed computing over TCP sockets: a text-transform server
(single-threaded), a calculator server (one thread per client), and an
interactive command-line client.

## Course
Parallel and Distributed Computing — Semester 6

## Language
C# 12 / .NET 8

## Exercises

### Exercise 1 — Text-Transform Server (single-threaded)

Accepts one client at a time.

| Command | Example | Response |
|---------|---------|----------|
| `upper <text>` | `upper hello world` | `HELLO WORLD` |
| `lower <text>` | `lower HELLO` | `hello` |
| `reverse <text>` | `reverse abc` | `cba` |
| `length <text>` | `length hello` | `5` |
| `quit` | — | closes connection |

### Exercise 2 — Calculator Server (multithreaded)

One background thread per accepted client — multiple clients can connect simultaneously.

```
Protocol: <a> <op> <b>   where op ∈ { + - * / }
Example:  3.5 * 2        →  7
          10 / 0         →  ERROR: division by zero
```

### Exercise 3 — Interactive Client

Connects to either server and enters a read-eval-print loop.

## How to Run

### Prerequisites
- .NET 8 SDK

### Steps — run server and client in two terminals

**Terminal 1 (text server):**
```bash
cd Lab9/csharp
dotnet run -- server text 8080
```

**Terminal 2 (calculator server, different port):**
```bash
dotnet run -- server calc 8081
```

**Terminal 3 (client):**
```bash
dotnet run -- client 127.0.0.1 8080
> upper hello world
< HELLO WORLD
> quit
```

## Key C# Networking Primitives

| Class | Role |
|-------|------|
| `TcpListener` | Binds a port, accepts incoming connections |
| `TcpClient` | Establishes outbound TCP connections |
| `NetworkStream` | Byte stream over the TCP connection |
| `StreamReader/Writer` | Newline-delimited text protocol on top of the stream |
| `Thread` (background) | Per-client handler in the calculator server |
