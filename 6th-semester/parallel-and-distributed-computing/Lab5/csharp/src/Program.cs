/*
 * Lab 5 — Data Parallelism (C# / .NET 8)
 *
 * Each exercise runs a sequential version followed by a parallel version
 * (4 threads) and prints the elapsed time for comparison.
 * Threads divide the work by partitioning the index space into equal chunks;
 * no synchronisation is needed because each thread writes to a disjoint range.
 *
 * Exercise 1 — Vector Addition   : a[i] = b[i] + c[i]   (1 M elements)
 * Exercise 2 — Matrix Addition   : a[i,j] = b[i,j]+c[i,j]  (1000×1000)
 * Exercise 3 — RGB to Grayscale  : gray = 0.299R + 0.587G + 0.114B  (1920×1080)
 * Exercise 4 — SAT Solver        : parallel Boolean circuit check (2^20 inputs)
 */

using Lab5;

Section("Exercise 1 — Vector Addition  (1 M elements)");
VectorAdd.Run();

Section("Exercise 2 — Matrix Addition  (1000 × 1000)");
MatrixAdd.Run();

Section("Exercise 3 — RGB to Grayscale  (1920 × 1080)");
RgbToGrayscale.Run();

Section("Exercise 4 — SAT Solver  (2^20 = 1 048 576 combinations)");
SatSolver.Run();

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}
