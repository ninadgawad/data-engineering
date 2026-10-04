# How Databases Really Enforce UNIQUE Constraints: A Deep Dive into B+Trees, MVCC & Concurrency

A `UNIQUE` constraint looks deceptively simple:

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE
);
```

At the application level, it seems to mean:

> "Don't allow two users to have the same email."

But for a database engineer, the interesting question is:

> **How does the database guarantee that uniqueness when hundreds or thousands of transactions are trying to insert data concurrently?**

The answer takes us inside the database engine.

We need to understand four concepts:

1. **B+Tree indexes**
2. **Database pages and latches**
3. **Locks and MVCC**
4. **Commit and rollback**

---

## 1. UNIQUE Is More Than a Validation Rule

A common implementation mistake is to think uniqueness can be enforced like this:

```sql
SELECT *
FROM users
WHERE email = 'john@example.com';

-- If nothing found:
INSERT INTO users (...);
```

This is **not safe under concurrency**.

Consider two requests arriving simultaneously:

```text
Transaction A                  Transaction B
-------------                  -------------

SELECT email                  SELECT email
     ↓                             ↓
No row found                  No row found
     ↓                             ↓
INSERT                        INSERT
     ↓                             ↓
SUCCESS                       SUCCESS
```

We have just created duplicate data.

The database therefore needs to enforce uniqueness **atomically**, as part of its storage and transaction machinery.

This is where the unique index becomes important.

---

# 2. The Unique Index

Most relational databases implement a `UNIQUE` constraint using a unique index, although the exact implementation varies by database.

Conceptually:

```text
users table

101 | alice@example.com
102 | john@example.com
103 | mary@example.com
```

The unique index maintains keys in sorted order:

```text
              Root
               |
        ┌──────┴──────┐
        ↓             ↓
     Page 1         Page 2
   ┌─────────┐     ┌─────────┐
   │ alice   │     │ mary    │
   │ john    │     │ steve   │
   │ kate    │     │ tom     │
   └─────────┘     └─────────┘
```

This is typically organized as a **B+Tree**.

The important property is that the database doesn't need to scan every row to determine whether:

```text
john@example.com
```

already exists.

It traverses the tree to the appropriate leaf page.

---

# 3. What Happens During INSERT?

Consider:

```sql
INSERT INTO users(id, email)
VALUES (101, 'john@example.com');
```

The database engine roughly performs:

```text
SQL
 ↓
Parser
 ↓
Query Planner
 ↓
Execution Engine
 ↓
Unique Index
 ↓
B+Tree traversal
 ↓
Leaf Page
 ↓
Check for conflicting key
```

The B+Tree traversal looks conceptually like:

```text
                 Root
                  |
                  ↓
             Internal Page
                  |
                  ↓
              Leaf Page
                  |
        ┌─────────┴─────────┐
        ↓                   ↓
   key doesn't exist    key exists
        ↓                   ↓
     INSERT             Reject
```

But this still doesn't explain concurrency.

And concurrency is where things become interesting.

---

# 4. The Real Problem: Two Transactions

Imagine:

```text
Transaction A                  Transaction B

INSERT john@example.com        INSERT john@example.com
       ↓                              ↓
Find index location            Find index location
       ↓                              ↓
Check key                      Check key
       ↓                              ↓
      ???                            ???
```

Both transactions want the same unique key.

The database must guarantee:

```text
At most ONE transaction
can successfully create
the committed unique key.
```

This requires coordination.

---

# 5. Database Pages

Before talking about locks, we need to understand **pages**.

Databases don't normally read and write individual rows directly from disk.

Data is organized into fixed-size or managed-size **pages**.

Conceptually:

```text
Database
   |
   +-- Page 1
   +-- Page 2
   +-- Page 3
   +-- Page 4
   +-- ...
```

A B+Tree is therefore a collection of pages:

```text
                 Root Page
                    |
          ┌─────────┴─────────┐
          ↓                   ↓
      Internal Page       Internal Page
          |                   |
          ↓                   ↓
      Leaf Page            Leaf Page
```

When an index entry is inserted, the engine may need to modify one or more pages.

---

# 6. Latches: Protecting the B+Tree Structure

Now we introduce an important distinction:

## Latch ≠ Lock

A **latch** protects internal database structures.

For example, suppose two database threads attempt to modify the same index page:

```text
Thread A ────────┐
                 ↓
              Index Page
                 ↑
Thread B ────────┘
```

Without synchronization, they could corrupt the page.

A latch provides short-lived protection:

```text
Acquire latch
      ↓
Modify page
      ↓
Release latch
```

Think of it as:

> **A latch protects the physical data structure.**

It is generally held for a very short period.

---

# 7. Locks: Protecting Transactional Semantics

A **transaction lock** has a different purpose.

It protects logical data and transactional consistency.

Think:

> **Latch = protect the database structure.**

> **Lock = protect transactional correctness.**

This distinction is extremely useful in database interviews.

For example:

```text
                 Database
                    |
          ┌─────────┴─────────┐
          ↓                   ↓
       Latches              Locks
          ↓                   ↓
 Protect pages/tree       Protect transactional
 structure                consistency
```

The exact implementation varies between database engines.

---

# 8. Transaction A Inserts the Key

Suppose Transaction A executes:

```sql
BEGIN;

INSERT INTO users
VALUES (101, 'john@example.com');
```

The database traverses the B+Tree and reaches the appropriate leaf page.

It determines that:

```text
john@example.com
```

doesn't have a conflicting committed entry.

The database now has to coordinate the insertion with other transactions.

Conceptually:

```text
Unique Index

john@example.com
       |
       ↓
Transaction A
       |
       ↓
Pending insertion
```

The important principle is:

> **The uniqueness decision is part of the transaction, not a separate application-level check.**

---

# 9. Transaction B Arrives

Now B executes:

```sql
BEGIN;

INSERT INTO users
VALUES (102, 'john@example.com');
```

B reaches the same logical key.

But A's transaction has not committed yet.

B cannot simply conclude:

> "The key exists."

Why?

Because A could still execute:

```sql
ROLLBACK;
```

Therefore B may need to wait for A's transaction outcome.

Conceptually:

```text
              john@example.com
                     |
             Transaction A
                     |
                uncommitted
                     |
             Transaction B
                     |
                  WAIT
```

This is a critical concept:

> **An uncommitted conflicting operation is not necessarily the final state of the database.**

---

# 10. Scenario 1: Transaction A Commits

A executes:

```sql
COMMIT;
```

Now:

```text
john@example.com
        |
        ↓
Transaction A
        |
        ↓
COMMITTED
```

Transaction B can now continue its uniqueness check.

It discovers:

```text
john@example.com already exists
```

Therefore:

```text
Transaction A → SUCCESS

Transaction B → UNIQUE VIOLATION
```

Final state:

```text
101 | john@example.com
```

Only one row exists.

---

# 11. Scenario 2: Transaction A Rolls Back

Suppose instead A executes:

```sql
ROLLBACK;
```

Now:

```text
Transaction A
      |
      ↓
  ROLLBACK
      |
      ↓
Insertion disappears
```

Transaction B can now proceed.

```text
Transaction A → ROLLBACK

Transaction B
      |
      ↓
Retry/continue uniqueness check
      |
      ↓
Key available
      |
      ↓
INSERT
      |
      ↓
COMMIT
```

Final state:

```text
102 | john@example.com
```

This illustrates why transaction state matters when enforcing uniqueness.

---

# 12. Where Does MVCC Fit?

Now we get to another major database concept:

**MVCC — Multi-Version Concurrency Control.**

MVCC allows transactions to work with different logical versions of data without requiring every reader to block every writer.

Conceptually:

```text
Row / Index Entry

Version A
created by Transaction 100
        |
        ↓
uncommitted

Version B
created later
        |
        ↓
committed
```

A transaction's visibility depends on things such as:

* transaction ID
* commit status
* isolation level
* visibility rules

The key mental model is:

> **MVCC answers: "What version of the data should this transaction see?"**

Concurrency control answers:

> **"What operations can happen concurrently?"**

These mechanisms work together, but they solve different problems.

---

# 13. MVCC Does Not Mean "No Locks"

This is another common misconception.

You may hear:

> "PostgreSQL/MySQL uses MVCC, so it doesn't need locks."

That's too simplistic.

MVCC reduces the need for blocking between readers and writers, but databases still need synchronization and locking mechanisms for many operations.

For example:

```text
Readers
   ↓
MVCC visibility
   ↓
Often don't block writers

Writers
   ↓
Concurrency control
   ↓
May conflict with other writers
```

Unique constraints are a particularly interesting case because two transactions trying to create the **same logical key** have an inherent conflict.

---

# 14. What Happens If the B+Tree Page Is Full?

Suppose our leaf page looks like:

```text
┌───────────────────────────┐
│ alice                     │
│ kate                      │
│ mary                      │
│ steve                     │
│ tom                       │
└───────────────────────────┘
```

Now we insert:

```text
john
```

The page may not have enough room.

The B+Tree can perform a **page split**:

```text
Before:

┌───────────────────────────┐
│ A B C D E F G H I J       │
└───────────────────────────┘


After:

┌───────────────┐    ┌───────────────┐
│ A B C D E     │    │ F G H I J     │
└───────────────┘    └───────────────┘
```

The parent node must then be updated to reference the new page.

This is another reason latches are important.

Multiple threads cannot safely restructure the same B+Tree simultaneously without synchronization.

---

# 15. Physical Correctness vs Transactional Correctness

This gives us a very useful architectural distinction.

### Physical correctness

The B+Tree must never become corrupted.

Mechanisms:

```text
Pages
+
Latches
+
Buffer management
+
Logging/recovery
```

### Transactional correctness

The database must preserve the rules of the transaction.

Mechanisms:

```text
Locks
+
MVCC
+
Transaction IDs
+
Isolation
+
Commit/Rollback
```

So:

```text
              Database Engine
                     |
          ┌──────────┴──────────┐
          ↓                     ↓
   Physical correctness    Transactional correctness
          ↓                     ↓
       B+Tree                 MVCC
       Pages                  Locks
       Latches                Isolation
                              Commit
                              Rollback
```

---

# 16. The Complete INSERT Journey

Let's put everything together.

A request arrives:

```sql
INSERT INTO users(id, email)
VALUES (101, 'john@example.com');
```

The database roughly goes through:

```text
                SQL INSERT
                    |
                    ↓
              Query Processing
                    |
                    ↓
             Unique Index Lookup
                    |
                    ↓
               B+Tree Traversal
                    |
                    ↓
                Leaf Page
                    |
                    ↓
            Is key conflicting?
                    |
          ┌─────────┴──────────┐
          ↓                    ↓
         NO                   YES
          |                    |
          ↓                    ↓
  Insert index entry      Determine transaction
          |                    |
          ↓                    ↓
   Transaction state       Wait / conflict
          |                    |
          └─────────┬──────────┘
                    ↓
              COMMIT / ROLLBACK
```

This is the conceptual journey.

The exact implementation differs significantly across PostgreSQL, MySQL/InnoDB, Oracle, SQL Server, etc., but the architectural principles are similar.

---

# 17. Why "SELECT Then INSERT" Is Fundamentally Different

Consider:

```sql
SELECT *
FROM users
WHERE email = 'john@example.com';

INSERT INTO users (...);
```

The first operation answers:

> "What do I see right now?"

The second operation says:

> "Make this change."

Between those two operations, another transaction can modify the database.

That's a classic **race condition**.

A database-level unique constraint moves the invariant into the database's concurrency-controlled storage layer.

Instead of:

```text
Application
   ↓
SELECT
   ↓
Application decision
   ↓
INSERT
```

we have:

```text
Application
   ↓
INSERT
   ↓
Unique Index
   ↓
Concurrency Control
   ↓
Atomic decision
```

That is much stronger.

---

# 18. A Senior Engineer's Mental Model

When looking at database concurrency, think in four layers:

### Layer 1 — B+Tree

**Where is the key?**

```text
Root
 ↓
Internal nodes
 ↓
Leaf page
```

### Layer 2 — Pages and Latches

**Can multiple threads safely manipulate the physical structure?**

```text
Page
 ↓
Latch
 ↓
Modify safely
```

### Layer 3 — Locks + MVCC

**How do concurrent transactions interact?**

```text
Transaction A
      ↕
Concurrency Control
      ↕
Transaction B
```

### Layer 4 — Transaction Lifecycle

**What is the final outcome?**

```text
INSERT
  ↓
Pending
  ↓
COMMIT → durable
  or
ROLLBACK → undone
```

---

# 19. The Interview Question I'd Ask a Senior Engineer

Imagine you're interviewing someone and ask:

> **Two transactions simultaneously insert the same email into a table with a UNIQUE constraint. Walk me through what happens inside the database.**

A strong answer should mention:

```text
1. Unique index
2. B+Tree traversal
3. Leaf/index page
4. Concurrency control
5. Locks and/or MVCC
6. Transaction visibility
7. Waiting for conflicting transaction
8. COMMIT vs ROLLBACK
9. Unique violation
10. Physical page protection via latches
```

A weak answer is:

> "The database checks if the value exists and throws an error."

That's functionally correct, but it doesn't demonstrate understanding of the database engine.

A strong answer explains **how the database makes that check safe under concurrency**.

---

# 20. The Big Takeaway

A `UNIQUE` constraint looks like a simple business rule:

```sql
UNIQUE(email)
```

But internally it represents a sophisticated interaction between:

```text
                  UNIQUE CONSTRAINT
                         |
             ┌───────────┴───────────┐
             ↓                       ↓
         UNIQUE INDEX           TRANSACTION
             |                       |
           B+Tree                MVCC / Locks
             |                       |
          Pages                 Isolation
             |                       |
          Latches              Commit/Rollback
             |                       |
             └───────────┬───────────┘
                         ↓
                 CONCURRENT CORRECTNESS
```

The real engineering insight is this:

> **A database constraint is not merely validation logic. It is an invariant enforced inside the database's concurrency-controlled storage engine.**

That's why database-level constraints remain essential even when the application has its own validation.

---

## Final Mental Model

When you see:

```sql
email VARCHAR(255) UNIQUE
```

don't just think:

> "No duplicate emails."

Think:

> **"The database has an indexed, transaction-aware mechanism that must locate the key efficiently, coordinate concurrent writers, respect transaction visibility, and produce exactly one valid committed outcome."**

That's the difference between understanding **SQL** and understanding the **database engine**.




> Generated using Codex
