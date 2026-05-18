import os
from datetime import datetime
import aiosqlite

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------
_host = os.environ.get("HOST", "0.0.0.0")
_port = int(os.environ.get("PORT", "8000"))

DB_PATH = "expenses.db"

mcp = FastMCP(
    "expense-tracker",
    host=_host,
    port=_port,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)

# ---------------------------------------------------------------------------
# DB INIT
# ---------------------------------------------------------------------------
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                note TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


# ---------------------------------------------------------------------------
# TOOL 1 — log_expense
# ---------------------------------------------------------------------------
@mcp.tool()
async def log_expense(amount: float, category: str, note: str = "") -> str:
    """
    Log a new expense into SQLite.
    """

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO expenses (amount, category, note)
            VALUES (?, ?, ?)
            """,
            (amount, category.lower(), note),
        )
        await db.commit()

    return f"✅ Logged ₹{amount} under '{category}'"


# ---------------------------------------------------------------------------
# TOOL 2 — summarise_spending
# ---------------------------------------------------------------------------
@mcp.tool()
async def summarise_spending(period: str = "this month") -> str:
    """
    Summarise spending grouped by category.
    (For now: ignores period, aggregates all data)
    """

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)
        rows = await cursor.fetchall()

    if not rows:
        return "No expenses found."

    total = sum(row[1] for row in rows)

    lines = [f"💰 Total spending: ₹{total:.2f}\n"]

    for category, amount in rows:
        lines.append(f"- {category}: ₹{amount:.2f}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# TOOL 3 — budget_alert
# ---------------------------------------------------------------------------
@mcp.tool()
async def budget_alert(category: str, limit: float) -> str:
    """
    Check if spending exceeds a category budget.
    """

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT SUM(amount)
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
            """,
            (category,),
        )
        row = await cursor.fetchone()

    spent = row[0] or 0

    if spent > limit:
        return (
            f"⚠️ Over budget for '{category}'!\n"
            f"Spent: ₹{spent:.2f}\n"
            f"Limit: ₹{limit:.2f}"
        )

    return (
        f"✅ Within budget for '{category}'\n"
        f"Spent: ₹{spent:.2f}\n"
        f"Remaining: ₹{limit - spent:.2f}"
    )


# ---------------------------------------------------------------------------
# STARTUP
# ---------------------------------------------------------------------------
def main():
    import asyncio

    async def run():
        await init_db()
        mcp.run(transport="streamable-http")

    asyncio.run(run())


if __name__ == "__main__":
    main()