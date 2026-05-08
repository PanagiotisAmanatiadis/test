/*
 * Lab 4 — Producer-Consumer & CarPark Simulation (C# / .NET 8)
 *
 * Exercise 1 — Producer-Consumer with BlockingCollection<T>
 *   One producer thread enqueues N messages into a bounded queue (capacity 10).
 *   One consumer thread dequeues and processes each message.
 *   BlockingCollection.Add() blocks when the queue is full; Take() (via
 *   GetConsumingEnumerable) blocks when empty.  CompleteAdding() signals EOF.
 *
 * Exercise 2 — CarPark Simulation with SemaphoreSlim
 *   20 cars attempt to enter a park with 4 spaces.
 *   SemaphoreSlim(4,4) enforces the capacity: cars exceeding the limit block
 *   in Arrive() and are automatically unblocked when a parked car calls Depart().
 */

using System.Collections.Concurrent;
using Lab4.CarPark;
using Lab4.ProducerConsumer;

// ── Exercise 1: Producer-Consumer ────────────────────────────────────────────

Section("Exercise 1 — Producer-Consumer (BlockingCollection, capacity 10)");

var queue    = new BlockingCollection<Message>(boundedCapacity: 10);
var producer = new Producer(queue);
var consumer = new Consumer(queue);

var tProducer = new Thread(producer.Run);
var tConsumer = new Thread(consumer.Run);

tProducer.Start();
tConsumer.Start();

tProducer.Join();
tConsumer.Join();

Console.WriteLine($"\nAll {Producer.Count} messages produced and consumed.");

// ── Exercise 2: CarPark Simulation ───────────────────────────────────────────

Section("Exercise 2 — CarPark simulation (capacity 4, 20 cars)");

const int Capacity = 4;
const int NumCars  = 20;

var park    = new Park(Capacity);
var threads = new Thread[NumCars];

for (int i = 0; i < NumCars; i++)
{
    var car = new Car(i + 1, park);
    threads[i] = new Thread(car.Run);
}

foreach (var t in threads) t.Start();
foreach (var t in threads) t.Join();

Console.WriteLine($"\nAll {NumCars} cars have parked and departed.");

// ── helpers ───────────────────────────────────────────────────────────────────

static void Section(string title)
{
    Console.WriteLine();
    Console.WriteLine(new string('─', 60));
    Console.WriteLine(title);
    Console.WriteLine(new string('─', 60));
}
