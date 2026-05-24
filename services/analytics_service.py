"""
Analytics Service — ЭТАП 6.

Функции:
- Trend analysis (углы наклона метрик)
- Burnout detection (правила + ML-ready)
- Productivity patterns (лучшие дни недели)
- Weekly/Monthly summaries
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.entry_repository import EntriesRepository
from repositories.insight_repository import InsightRepository

logger = logging.getLogger(__name__)


class BurnoutLevel:
    """Уровни риска выгорания."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalyticsService:
    """
    Сервис аналитики продуктивности.
    
    Демонстрирует:
    - Rule-based detection
    - Time-series анализ
    - Pattern recognition
    """

    @staticmethod
    async def get_burnout_risk(user_id: int, session: AsyncSession) -> dict:
        """
        Определить риск выгорания на основе последних 7 дней.
        
        Правила:
        - CRITICAL: 3+ дней motivation < 3 И sleep < 5
        - HIGH: avg_motivation < 4 ИЛИ avg_sleep < 5 за 5+ дней
        - MEDIUM: avg_motivation < 5 ИЛИ avg_energy < 5 за 7 дней
        - LOW: avg_motivation < 6 за 7 дней
        - NONE: всё в норме
        """
        entries = await EntriesRepository.get_by_period(user_id, session, days=7)

        if not entries:
            return {
                "level": BurnoutLevel.NONE,
                "message": "Недостаточно данных для анализа",
                "entries_analyzed": 0,
                "recommendations": ["Начните вести дневник каждый день"],
            }

        n = len(entries)
        avg_sleep = sum(e.sleep for e in entries) / n
        avg_energy = sum(e.energy for e in entries) / n
        avg_motivation = sum(e.motivation for e in entries) / n
        avg_clarity = sum(e.clarity for e in entries) / n

        # Подсчёт критических дней
        critical_days = sum(
            1 for e in entries
            if e.motivation < 3 and e.sleep < 5
        )

        # Определение уровня
        if critical_days >= 3:
            level = BurnoutLevel.CRITICAL
            message = "⚠️ Критический риск выгорания! Срочно нужен отдых."
            recommendations = [
                "Возьмите выходной или сократите нагрузку",
                "Обеспечьте 8+ часов сна",
                "Поговорите с кем-то близким",
                "Исключите все несрочные задачи",
            ]
        elif avg_motivation < 4 or avg_sleep < 5:
            level = BurnoutLevel.HIGH
            message = "🔴 Высокий риск выгорания. Нужны изменения."
            recommendations = [
                "Приоритизируйте сон (7-8 часов)",
                "Сократите количество задач",
                "Добавьте физическую активность",
            ]
        elif avg_motivation < 5 or avg_energy < 5:
            level = BurnoutLevel.MEDIUM
            message = "🟡 Средний риск. Обратите внимание на восстановление."
            recommendations = [
                "Улучшите режим сна",
                "Добавьте перерывы в течение дня",
                "Найдите источники мотивации",
            ]
        elif avg_motivation < 6:
            level = BurnoutLevel.LOW
            message = "🟢 Низкий риск. Всё под контролем."
            recommendations = [
                "Продолжайте текущий режим",
                "Следите за балансом работы и отдыха",
            ]
        else:
            level = BurnoutLevel.NONE
            message = "✅ Отличное состояние! Продолжайте в том же духе."
            recommendations = []

        return {
            "level": level,
            "message": message,
            "entries_analyzed": n,
            "metrics": {
                "avg_sleep": round(avg_sleep, 2),
                "avg_energy": round(avg_energy, 2),
                "avg_motivation": round(avg_motivation, 2),
                "avg_clarity": round(avg_clarity, 2),
                "critical_days": critical_days,
            },
            "recommendations": recommendations,
        }

    @staticmethod
    async def get_trends(user_id: int, session: AsyncSession, days: int = 14) -> dict:
        """
        Анализ трендов метрик за период.
        
        Возвращает направление тренда (rising/stable/falling)
        и процент изменения для каждой метрики.
        """
        entries = await EntriesRepository.get_by_period(user_id, session, days=days)

        if len(entries) < 3:
            return {"error": "Недостаточно данных для анализа трендов"}

        # Сортируем по дате
        sorted_entries = sorted(entries, key=lambda e: e.date)

        # Делим на первую и вторую половину
        mid = len(sorted_entries) // 2
        first_half = sorted_entries[:mid]
        second_half = sorted_entries[mid:]

        def avg(lst, field):
            return sum(getattr(e, field) for e in lst) / len(lst)

        def trend(first, second):
            diff = second - first
            if abs(diff) < 0.5:
                return "stable"
            return "rising" if diff > 0 else "falling"

        metrics = ["sleep", "energy", "clarity", "motivation"]
        trends = {}

        for metric in metrics:
            first_avg = avg(first_half, metric)
            second_avg = avg(second_half, metric)
            change_pct = ((second_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0

            trends[metric] = {
                "trend": trend(first_avg, second_avg),
                "first_half_avg": round(first_avg, 2),
                "second_half_avg": round(second_avg, 2),
                "change_percent": round(change_pct, 1),
            }

        return {
            "period_days": days,
            "entries_count": len(entries),
            "trends": trends,
        }

    @staticmethod
    async def get_productivity_patterns(user_id: int, session: AsyncSession) -> dict:
        """
        Анализ паттернов продуктивности по дням недели.
        
        Определяет:
        - Лучшие дни недели
        - Худшие дни недели
        - Средние показатели по дням
        """
        entries = await EntriesRepository.get_by_period(user_id, session, days=30)

        if not entries:
            return {"error": "Нет данных за последние 30 дней"}

        # Группируем по дням недели
        weekday_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        weekday_data: dict[int, list] = {i: [] for i in range(7)}

        for entry in entries:
            weekday = entry.date.weekday()
            score = (entry.energy + entry.clarity + entry.motivation) / 3
            weekday_data[weekday].append(score)

        # Считаем средние
        weekday_scores = {}
        for day_num, scores in weekday_data.items():
            if scores:
                weekday_scores[weekday_names[day_num]] = round(sum(scores) / len(scores), 2)

        if not weekday_scores:
            return {"error": "Недостаточно данных"}

        best_day = max(weekday_scores, key=lambda k: weekday_scores[k])
        worst_day = min(weekday_scores, key=lambda k: weekday_scores[k])

        return {
            "best_day": best_day,
            "worst_day": worst_day,
            "scores_by_weekday": weekday_scores,
            "entries_analyzed": len(entries),
        }

    @staticmethod
    async def get_streak(user_id: int, session: AsyncSession) -> dict:
        """
        Подсчёт streak — количество дней подряд с записями.
        """
        entries = await EntriesRepository.get_by_period(user_id, session, days=365)

        if not entries:
            return {"current_streak": 0, "best_streak": 0}

        # Уникальные даты, отсортированные
        dates = sorted(set(e.date for e in entries), reverse=True)

        current_streak = 0
        today = datetime.now(timezone.utc).date()
        check_date = today

        for d in dates:
            if d == check_date or d == check_date - timedelta(days=1):
                current_streak += 1
                check_date = d
            else:
                break

        # Best streak
        best_streak = 1
        temp_streak = 1
        for i in range(1, len(dates)):
            if (dates[i - 1] - dates[i]).days == 1:
                temp_streak += 1
                best_streak = max(best_streak, temp_streak)
            else:
                temp_streak = 1

        return {
            "current_streak": current_streak,
            "best_streak": best_streak,
            "total_entries": len(entries),
            "last_entry_date": str(dates[0]) if dates else None,
        }
