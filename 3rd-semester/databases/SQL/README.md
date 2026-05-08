# SQL Queries

Fifteen SQL queries over the **Chinook** sample database — a digital music store schema.

## Course
Databases — Semester 3

## Database
[Chinook Database](https://github.com/lerocha/chinook-database) — SQLite

### Key Tables

```
artist(ArtistId, Name)
album(AlbumId, Title, ArtistId)
track(TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
genre(GenreId, Name)
mediatype(MediaTypeId, Name)
employee(EmployeeId, FirstName, LastName, ReportsTo, BirthDate, ...)
customer(CustomerId, FirstName, LastName, ..., Country, SupportRepId)
invoice(InvoiceId, CustomerId, InvoiceDate, BillingCity, ..., Total)
invoiceline(InvoiceLineId, InvoiceId, TrackId, UnitPrice, Quantity)
playlist(PlaylistId, Name)
playlisttrack(PlaylistId, TrackId)
```

---

## Queries

### Query 01 — Albums with "Best" in the title

> Return all columns of albums whose title contains the word **Best**.

```sql
SELECT *
FROM album
WHERE Title LIKE '%Best%';
```

---

### Query 02 — Led Zeppelin albums

> Return the album ID and title of all Led Zeppelin albums.

```sql
SELECT album.AlbumId, album.Title
FROM album
JOIN artist ON album.ArtistId = artist.ArtistId
WHERE artist.Name = 'Led Zeppelin';
```

---

### Query 03 — Track count per genre (descending)

> Return genre name and track count, ordered by count descending.

```sql
SELECT genre.Name, COUNT(track.GenreId)
FROM track
JOIN genre ON track.GenreId = genre.GenreId
GROUP BY genre.GenreId
ORDER BY COUNT(track.GenreId) DESC;
```

---

### Query 04 — Customer count per employee (including zero)

> Return employee first name, last name, and the number of customers they support.
> Employees with no customers must appear with count **0**.

```sql
SELECT employee.FirstName, employee.LastName, COUNT(customer.CustomerId)
FROM employee
JOIN customer ON employee.EmployeeId = customer.SupportRepId
GROUP BY employee.EmployeeId

UNION ALL

SELECT employee.FirstName, employee.LastName, 0
FROM employee
WHERE employee.FirstName NOT IN (
    SELECT employee.FirstName
    FROM employee
    JOIN customer ON employee.EmployeeId = customer.SupportRepId
    GROUP BY employee.EmployeeId
)
AND employee.LastName NOT IN (
    SELECT employee.LastName
    FROM employee
    JOIN customer ON employee.EmployeeId = customer.SupportRepId
    GROUP BY employee.EmployeeId
);
```

---

### Query 05 — Media type / genre combinations with more than 50 tracks (descending)

> Return media type name, genre name, and track count for combinations that have more than 50 tracks,
> ordered by count descending.

```sql
SELECT mediatype.Name, genre.Name, COUNT(*)
FROM track
JOIN mediatype ON track.MediaTypeId = mediatype.MediaTypeId
JOIN genre     ON genre.GenreId     = track.GenreId
GROUP BY genre.Name
HAVING COUNT(*) > 50;
```

---

### Query 06 — Invoices billed to New York containing tracks from more than one genre

> Return invoice ID, product count, total calculated as `UnitPrice × Quantity`, and the stored total —
> for invoices billed to **New York** that include tracks spanning **more than one genre**.

```sql
SELECT
    invoice.InvoiceId,
    COUNT(invoiceline.InvoiceId)                        AS product_count,
    SUM(invoiceline.UnitPrice * invoiceline.Quantity)   AS total1,
    invoice.Total                                       AS total2
FROM invoice
JOIN invoiceline ON invoice.InvoiceId  = invoiceline.InvoiceId
JOIN track       ON invoiceline.TrackId = track.TrackId
JOIN genre       ON track.GenreId       = genre.GenreId
WHERE invoice.BillingCity = 'New York'
GROUP BY invoice.InvoiceId
HAVING COUNT(DISTINCT genre.Name) > 1
ORDER BY invoice.InvoiceId;
```

---

### Query 07 — Customers who purchased tracks from every genre starting with "S"

> Return all customer columns for customers who have bought tracks from **all** genres
> whose name begins with the letter S.

```sql
SELECT
    customer.CustomerId, customer.FirstName, customer.LastName,
    customer.Company,    customer.Address,   customer.City,
    customer.State,      customer.Country,   customer.PostalCode,
    customer.Phone,      customer.Fax,       customer.Email,
    customer.SupportRepId
FROM customer
JOIN invoice     ON customer.CustomerId  = invoice.CustomerId
JOIN invoiceline ON invoice.InvoiceId    = invoiceline.InvoiceId
JOIN track       ON invoiceline.TrackId  = track.TrackId
JOIN genre       ON track.GenreId        = genre.GenreId
WHERE genre.Name LIKE 'S%'
GROUP BY customer.CustomerId
HAVING COUNT(DISTINCT genre.Name) = (
    SELECT COUNT(DISTINCT genre.Name)
    FROM genre
    WHERE genre.Name LIKE 'S%'
);
```

---

### Query 08 — Employees older than their manager

> Return last name and birth date of the employee, and last name and birth date of their manager,
> for every employee who is **older** than their direct manager.

```sql
SELECT e1.LastName, e1.BirthDate, e2.LastName, e2.BirthDate
FROM employee e1
JOIN employee e2 ON e1.ReportsTo = e2.EmployeeId
WHERE e1.BirthDate < e2.BirthDate;
```

---

### Query 09 — Canadian customer with the most recent order

> Return last name and invoice date for the Canadian customer who placed the **most recent** order.

```sql
SELECT customer.LastName, invoice.InvoiceDate
FROM customer
JOIN invoice ON customer.CustomerId = invoice.CustomerId
WHERE invoice.InvoiceDate = (
    SELECT MAX(invoice.InvoiceDate)
    FROM customer
    JOIN invoice ON customer.CustomerId = invoice.CustomerId
    WHERE customer.Country = 'Canada'
);
```

---

### Query 10 — Playlist with the most tracks

> Return playlist ID, name, and track count for the playlist(s) with the **highest** track count.

```sql
SELECT playlist.PlaylistId, playlist.Name, COUNT(*) AS track_count
FROM playlist
JOIN playlisttrack ON playlist.PlaylistId  = playlisttrack.PlaylistId
JOIN track         ON playlisttrack.TrackId = track.TrackId
GROUP BY playlist.PlaylistId
HAVING COUNT(*) = (
    SELECT MAX(maxcount)
    FROM (
        SELECT COUNT(*) AS maxcount
        FROM playlist
        JOIN playlisttrack ON playlist.PlaylistId  = playlisttrack.PlaylistId
        JOIN track         ON playlisttrack.TrackId = track.TrackId
        GROUP BY playlist.PlaylistId
    ) a
);
```

---

### Query 11 — Playlists containing both Rock and Metal tracks

> Return all playlists that include tracks of **both** the Rock and Metal genres.

```sql
SELECT playlist.Name, playlist.PlaylistId
FROM playlist
JOIN playlisttrack ON playlist.PlaylistId  = playlisttrack.PlaylistId
JOIN track         ON playlisttrack.TrackId = track.TrackId
JOIN genre         ON track.GenreId         = genre.GenreId
WHERE genre.Name = 'Rock' OR genre.Name = 'Metal'
GROUP BY playlist.Name;
```

---

### Query 12 — Jazz tracks that have never been sold

> Return name, composer, duration, size, and unit price of Jazz tracks that appear in **no** invoice line.

```sql
SELECT track.Name, track.Composer, track.Milliseconds, track.Bytes, track.UnitPrice
FROM track
JOIN genre ON track.GenreId = genre.GenreId
WHERE genre.Name = 'Jazz'
  AND track.TrackId NOT IN (SELECT invoiceline.TrackId FROM invoiceline)
GROUP BY track.TrackId;
```

---

### Query 14 — Tracks starting with "C" and their playlists starting with "C"

> For tracks whose name starts with **C**, return the track name and the name of any playlist
> (also starting with C) it belongs to. Tracks that belong to **no such playlist** must still appear
> with an empty playlist name.

```sql
SELECT track.Name, playlist.Name
FROM track
JOIN playlisttrack ON track.TrackId        = playlisttrack.TrackId
JOIN playlist      ON playlisttrack.PlaylistId = playlist.PlaylistId
WHERE track.Name   LIKE 'C%'
  AND playlist.Name LIKE 'C%'

UNION

SELECT track.Name, ''
FROM track
WHERE track.Name LIKE 'C%'
  AND track.TrackId NOT IN (
      SELECT track.TrackId
      FROM track
      JOIN playlisttrack ON track.TrackId           = playlisttrack.TrackId
      JOIN playlist      ON playlisttrack.PlaylistId = playlist.PlaylistId
      WHERE track.Name   LIKE 'C%'
        AND playlist.Name LIKE 'C%'
  );
```

---

### Query 15 — Invoices containing only tracks from "Greatest" albums

> Return all invoice columns for invoices where **every** track belongs to an album whose title
> contains the word **Greatest**.

```sql
SELECT
    invoice.InvoiceId,    invoice.CustomerId,      invoice.InvoiceDate,
    invoice.BillingAddress, invoice.BillingCity,   invoice.BillingState,
    invoice.BillingCountry, invoice.BillingPostalCode, invoice.Total
FROM invoice
JOIN invoiceline ON invoice.InvoiceId  = invoiceline.InvoiceId
JOIN track       ON invoiceline.TrackId = track.TrackId
JOIN album       ON track.AlbumId       = album.AlbumId
WHERE invoice.InvoiceId NOT IN (
    SELECT invoice.InvoiceId
    FROM invoice
    JOIN invoiceline ON invoice.InvoiceId  = invoiceline.InvoiceId
    JOIN track       ON invoiceline.TrackId = track.TrackId
    JOIN album       ON track.AlbumId       = album.AlbumId
    WHERE album.Title NOT LIKE '%Greatest%'
    GROUP BY invoice.InvoiceId
)
GROUP BY invoice.InvoiceId;
```

---

## What It Demonstrates
- `JOIN`, `LEFT JOIN`, and self-joins
- Aggregate functions: `COUNT`, `MAX`, `SUM`
- `GROUP BY` / `HAVING` filtering
- Correlated and non-correlated subqueries
- `UNION` / `UNION ALL` for result merging
- Universal quantification via `NOT IN` + subquery count
- Pattern matching with `LIKE`
