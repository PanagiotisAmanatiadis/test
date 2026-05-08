using Lab12.Server.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddGrpc();

var app = builder.Build();
app.MapGrpcService<CalculatorService>();
app.MapGrpcService<EmailStoreService>();

app.MapGet("/", () =>
    "Lab 12 gRPC server. Use a gRPC client to connect (see Lab12.Client).");

Console.WriteLine("Lab 12 gRPC server starting...");
app.Run();
