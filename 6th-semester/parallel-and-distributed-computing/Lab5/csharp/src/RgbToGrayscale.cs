using System.Diagnostics;

namespace Lab5;

/// <summary>
/// Exercise 3 — RGB to Grayscale conversion.
///
/// Each pixel <c>(r,g,b)</c> is converted to grayscale using the luminance formula:
///   <c>gray = 0.299*r + 0.587*g + 0.114*b</c>
///
/// The image is represented as a flat array of <c>(byte r, byte g, byte b)</c> structs.
/// Parallelised by rows: each thread processes a contiguous band of pixel rows.
/// </summary>
internal static class RgbToGrayscale
{
    private const int Width      = 1920;
    private const int Height     = 1080;
    private const int NumThreads = 4;

    private readonly record struct Pixel(byte R, byte G, byte B);

    public static void Run()
    {
        // Simulate an image with known pixel values
        var pixels = new Pixel[Height, Width];
        var gray   = new byte[Height, Width];

        for (int y = 0; y < Height; y++)
            for (int x = 0; x < Width; x++)
                pixels[y, x] = new Pixel(R: 200, G: 150, B: 100);

        byte Convert(Pixel p) =>
            (byte)(0.299 * p.R + 0.587 * p.G + 0.114 * p.B);

        // ── Sequential ────────────────────────────────────────────────────────
        var sw = Stopwatch.StartNew();
        for (int y = 0; y < Height; y++)
            for (int x = 0; x < Width; x++)
                gray[y, x] = Convert(pixels[y, x]);
        sw.Stop();
        Console.WriteLine($"  Sequential : {sw.ElapsedMilliseconds,6} ms  " +
                          $"gray[0,0]={gray[0, 0]}");

        // ── Parallel (row partitioning) ───────────────────────────────────────
        var grayPar = new byte[Height, Width];
        sw.Restart();
        ParallelRunner.For(Height, NumThreads, (startRow, endRow) =>
        {
            for (int y = startRow; y < endRow; y++)
                for (int x = 0; x < Width; x++)
                    grayPar[y, x] = Convert(pixels[y, x]);
        });
        sw.Stop();
        Console.WriteLine($"  Parallel   : {sw.ElapsedMilliseconds,6} ms  " +
                          $"gray[0,0]={grayPar[0, 0]}  ({NumThreads} threads)");
    }
}
