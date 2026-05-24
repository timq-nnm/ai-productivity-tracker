from repositories.entry_repository import EntriesRepository

class StatsService:
    @staticmethod
    async def get_week_stats(user_id: int, session):

        entries = await EntriesRepository.get_by_period(user_id, session)

        if not entries:
            return {
                "avg_sleep": 0,
                "avg_energy": 0,
                "avg_clarity": 0,
                "avg_motivation": 0,
                "entries_count": 0
            }

        return {
            "avg_sleep": sum(e.sleep for e in entries) / len(entries),
            "avg_energy": sum(e.energy for e in entries) / len(entries),
            "avg_clarity": sum(e.clarity for e in entries) / len(entries),
            "avg_motivation": sum(e.motivation for e in entries) / len(entries),
            "entries_count": len(entries)
        }