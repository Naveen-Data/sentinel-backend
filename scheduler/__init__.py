"""
Sentinel Scheduler

Background task scheduling using APScheduler.

Design principles:
- Scheduled observations (email polling, health sync)
- Cron-based triggers
- Observable execution
- Graceful shutdown
"""

from typing import Optional
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)


class SentinelScheduler:
    """
    Background task scheduler for Sentinel.
    
    Schedules:
    - Email polling
    - Calendar sync
    - Health data sync
    - Scheduled proposals
    """
    
    def __init__(self):
        """
        Initialize the scheduler.
        """
        self.scheduler = AsyncIOScheduler()
        logger.info("Scheduler initialized")
    
    def start(self) -> None:
        """
        Start the scheduler.
        """
        settings = get_settings()
        
        if not settings.enable_scheduler:
            logger.info("Scheduler is disabled")
            return
        
        logger.info("Starting scheduler...")
        
        # Schedule email polling (every 5 minutes)
        self.scheduler.add_job(
            self._poll_emails,
            trigger=CronTrigger(minute="*/5"),
            id="poll_emails",
            name="Poll Gmail for new emails",
        )
        
        # Schedule calendar sync (every 15 minutes)
        self.scheduler.add_job(
            self._sync_calendar,
            trigger=CronTrigger(minute="*/15"),
            id="sync_calendar",
            name="Sync Google Calendar",
        )
        
        # Schedule health data sync (daily at 7am)
        self.scheduler.add_job(
            self._sync_health_data,
            trigger=CronTrigger(hour=7, minute=0),
            id="sync_health",
            name="Sync health data",
        )
        
        self.scheduler.start()
        logger.info("Scheduler started")
    
    def shutdown(self) -> None:
        """
        Shutdown the scheduler gracefully.
        """
        logger.info("Shutting down scheduler...")
        self.scheduler.shutdown(wait=True)
        logger.info("Scheduler shutdown complete")
    
    async def _poll_emails(self) -> None:
        """
        Scheduled task: Poll Gmail for new emails.
        """
        logger.info("Scheduled task: Polling emails")
        
        # TODO: Fetch unread emails
        # TODO: Create observations
        # TODO: Trigger graph runs
    
    async def _sync_calendar(self) -> None:
        """
        Scheduled task: Sync Google Calendar.
        """
        logger.info("Scheduled task: Syncing calendar")
        
        # TODO: Fetch calendar changes
        # TODO: Create observations
    
    async def _sync_health_data(self) -> None:
        """
        Scheduled task: Sync health data.
        """
        logger.info("Scheduled task: Syncing health data")
        
        # TODO: Fetch health metrics
        # TODO: Create observations


# Global scheduler instance
_scheduler: Optional[SentinelScheduler] = None


def get_scheduler() -> SentinelScheduler:
    """
    Get or create the global scheduler.
    """
    global _scheduler
    
    if _scheduler is None:
        _scheduler = SentinelScheduler()
    
    return _scheduler
