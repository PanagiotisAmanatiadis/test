# Relational Algebra Queries

Ten relational algebra queries over a sports-equipment salesperson database.

## Course
Databases — Semester 3

## Schema

```
Salesperson(ssn, firstname, lastname, type, boss)
Category(id, name, season)
Specialization(ssn, categoryID, last_spec_date)
```

- `Salesperson.boss` references `Salesperson.ssn` (self-referencing)
- `Specialization.ssn` references `Salesperson.ssn`
- `Specialization.categoryID` references `Category.id`

---

## Queries

### Query 1 — Salespersons specialized in both Tennis and Golf

> Return the SSNs of salespersons who are specialized in **both** tennis and golf.

```
π Specialization.ssn (σ Category.name='tennis' (
    σ Specialization.categoryID=Category.id (Specialization ⨝ Category)
))
∩
π Specialization.ssn (σ Category.name='golf' (
    σ Specialization.categoryID=Category.id (Specialization ⨝ Category)
))
```

---

### Query 2 — Salespersons specialized in Tennis or Ski

> Return the SSNs of salespersons who are specialized in **tennis** or **ski**.

```
π Specialization.ssn (
    σ Category.name='tennis' (σ Specialization.categoryID=Category.id (Specialization ⨝ Category))
    ∪
    σ Category.name='ski'    (σ Specialization.categoryID=Category.id (Specialization ⨝ Category))
)
```

---

### Query 3 — Salesperson types specialized in Snowboard

> Return the employment types of salespersons who are specialized in snowboard.

```
π type (
    σ Category.id=Specialization.categoryID ∧ name='snowboard'
    (Category ⨝ Salesperson ⨝ Specialization)
)
```

---

### Query 4 — Categories with specializations exclusively from 2014 onward

> Return the name and season of categories that have **only** specializations with `last_spec_date ≥ 2014-01-01`
> (i.e., exclude any category that also has a specialization before that date).

```
π Category.name, Category.season (
    σ Specialization.last_spec_date >= date('2014-01-01') (
        σ Specialization.categoryID=Category.id (Specialization ⨝ Category)
    )
)
−
π Category.name, Category.season (
    σ Specialization.last_spec_date < date('2014-01-01') (
        σ Specialization.categoryID=Category.id (Specialization ⨝ Category)
    )
)
```

---

### Query 5 — Direct subordinates of Bradley Salinas

> Return the first and last names of salespersons whose direct boss is **Bradley Salinas**.

```
π Salesperson2.firstname, Salesperson2.lastname (
    σ Salesperson1.ssn = Salesperson2.boss (
        σ Salesperson1.firstname='Bradley' ∧ Salesperson1.lastname='Salinas' (
            (ρ Salesperson1 Salesperson) ⨯ (ρ Salesperson2 Salesperson)
        )
    )
)
```

---

### Query 6 — Non-trainee salespersons with first name starting with G or last name starting with M

> Return the type, first name, and last name of salespersons who are **not** trainees and whose
> first name starts with 'G' **or** last name starts with 'M'.

```
π type, firstname, lastname (
    σ firstname LIKE 'G%' ∨ lastname LIKE 'M%' (
        π type, firstname, lastname (
            σ type ≠ 'trainee' Salesperson
        )
    )
)
```

---

### Query 7 — Colleagues sharing a category with salesperson '9771-50397'

> Return the SSN, first name, and last name of salespersons who share **at least one** category
> with the salesperson whose SSN is '9771-50397', excluding that salesperson themselves.

```
π Table2.ssn, Table2.firstname, Table2.lastname (
    σ Table1.categoryID = Table2.categoryID (
        σ Table1.ssn = '9771-50397' (
            (ρ Table1 (Specialization ⨝ Salesperson)) ⨯ (ρ Table2 (Specialization ⨝ Salesperson))
        )
    )
)
−
π ssn, firstname, lastname (σ ssn='9771-50397' Salesperson)
```

---

### Query 8 — Salespersons specialized in at least 3 different categories

> Return the first and last names of salespersons who have specializations in **at least 3** distinct categories.

```
π Table1.firstname, Table1.lastname (
    σ Table1.ssn = Table2.ssn
    ∧ Table2.ssn = Table3.ssn
    ∧ Table1.categoryID ≠ Table2.categoryID
    ∧ Table2.categoryID ≠ Table3.categoryID
    ∧ Table3.categoryID ≠ Table1.categoryID (
        (ρ Table1 (Salesperson ⨝ Specialization))
        ⨯ (ρ Table2 (Salesperson ⨝ Specialization))
        ⨯ (ρ Table3 (Salesperson ⨝ Specialization))
    )
)
```

---

### Query 9 — Most recent specialization record per salesperson-category pair

> Return the SSN, categoryID, and last_spec_date of specialization records that are **not**
> dominated by any other record with a later date (i.e., the maximum per pair).

```
π Specialization.ssn, Specialization.categoryID, Specialization.last_spec_date
    Specialization
−
π Specialization1.ssn, Specialization1.categoryID, Specialization1.last_spec_date (
    σ Specialization1.last_spec_date > Specialization2.last_spec_date (
        (ρ Specialization1 Specialization) ⨯ (ρ Specialization2 Specialization)
    )
)
```

---

### Query 10 — Categories covered by all salesperson types (Relational Division)

> Return the categories that are specialized in by **every** salesperson type present in the database.

```
(π Specialization.categoryID, Salesperson.type (
    σ Specialization.categoryID = Category.id (Specialization ⨝ Salesperson ⨝ Category)
))
÷
(π Salesperson.type (
    σ Specialization.categoryID = Category.id (Specialization ⨝ Salesperson ⨝ Category)
))
```

---

## What It Demonstrates
- Core relational algebra operators: projection (π), selection (σ), natural join (⨝), Cartesian product (⨯)
- Set operators: union (∪), intersection (∩), difference (−)
- Rename (ρ) for self-joins
- Relational division (÷) for universal quantification
- Query formulation without SQL
