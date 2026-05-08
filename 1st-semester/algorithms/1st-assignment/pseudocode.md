# Pseudocode – Best Time To Party

## Problem

Given a list of celebrities each attending the bazaar during a half-open interval
`[arrival, departure)`, find the 1-hour window `[t, t+1)` that maximises the number
of celebrities present simultaneously.

---

## Algorithm

```
ALGORITHM BestTime2Party(celebrities[1..n])

INPUT  : Array of n celebrities, each with (name, arrival, departure).
         Intervals are half-open: [arrival, departure).
         Visitor window is exactly 1 hour: [t, t+1).

OUTPUT : best_time   – optimal arrival hour
         best_count  – number of celebrities in that window
         best_list   – names of those celebrities

─────────────────────────────────────────────────────────────────────

BEGIN

    // Step 1 – Collect candidate window-start times.
    // The optimal window must begin at one of the arrival times,
    // because any earlier start only risks losing celebrities.

    candidates ← empty set
    FOR i ← 1 TO n DO
        candidates ← candidates ∪ { celebrities[i].arrival }
    END FOR

    // Step 2 – Evaluate each candidate window.

    best_time  ← -1
    best_count ←  0
    best_list  ← empty list

    FOR EACH t IN candidates DO

        count   ← 0
        present ← empty list

        FOR i ← 1 TO n DO
            // Overlap condition: arrival < t+1  AND  departure > t
            IF celebrities[i].arrival < t + 1 AND celebrities[i].departure > t THEN
                count   ← count + 1
                present ← present + [ celebrities[i].name ]
            END IF
        END FOR

        IF count > best_count THEN
            best_count ← count
            best_time  ← t
            best_list  ← present
        END IF

    END FOR

    // Step 3 – Report.

    PRINT "Best arrival time :", best_time, ":00"
    PRINT "Celebrities found :", best_count
    FOR EACH name IN best_list DO
        PRINT "  -", name
    END FOR

    RETURN best_time, best_count, best_list

END
```

---

## Complexity

| Dimension | Value  | Reason                                              |
|-----------|--------|-----------------------------------------------------|
| Time      | O(n²)  | For each of ≤ n candidate times, scan all n records |
| Space     | O(n)   | Candidate set + best list, both bounded by n        |

---

## Trace – Given Data (task.pdf, Table 1)

| Window `[t, t+1)` | Celebrities present                                                        | Count |
|--------------------|----------------------------------------------------------------------------|-------|
| `[18, 19)`         | Slayer, Ozzy                                                               | 2     |
| `[19, 20)`         | Metallica, Black Sabbath, Iron Maiden, Ozzy, Sepultura                     | 5     |
| **`[20, 21)`**     | **Metallica, Mötley Crüe, Accept, Black Sabbath, Manowar, Ozzy, Megadeth, Sepultura** | **8** |
| `[21, 22)`         | Mötley Crüe, Accept, Judas Priest, Black Sabbath, Manowar, Sepultura       | 6     |
| `[22, 23)`         | Scorpions, Nazareth, Judas Priest, Manowar, Anthrax, Sepultura             | 6     |
| `[23, 24)`         | Scorpions, Queensrÿche, Anthrax                                            | 3     |

**Answer:** Arrive at **20:00** to meet **8 celebrities**.
