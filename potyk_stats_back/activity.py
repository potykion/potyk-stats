import datetime
import sqlite3
from dataclasses import dataclass

from potyk_stats_back.dt_utils import parse_dt


@dataclass(frozen=True)
class ActivityEntry:
    activity: str
    created: datetime.datetime
    comment: str | None


class ActivityRepo:
    def __init__(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor

    def insert_activity(self, activity: ActivityEntry) -> None:
        self.cursor.execute(
            """
            INSERT INTO activities (activity, created, comment)
            VALUES (?, ?, ?)""",
            (
                activity.activity,
                activity.created.strftime("%Y-%m-%dT%H:%M"),
                activity.comment,
            ),
        )
        self.cursor.connection.commit()

    def list_activities(self) -> list[ActivityEntry]:
        rows = self.cursor.execute("""select * from activities""").fetchall()
        return [
            ActivityEntry(
                activity=row["activity"],
                created=parse_dt(row["created"]),
                comment=row["comment"],
            )
            for row in rows
        ]

    def list_activity_values(self) -> list[str]:
        rows = self.cursor.execute("""select distinct activity from activities""").fetchall()
        activity_values = []
        for row in rows:
            activity_values.append(row[0])
        return activity_values
