"""
Sentinel Telegram Bot

Telegram bot for quick HITL approvals.

Design principles:
- Simple command interface
- Quick approve/reject
- View pending proposals
- Secure authentication
"""

from typing import Optional

from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)


class TelegramBot:
    """
    Telegram bot for HITL approvals.
    
    Commands:
    /pending - List pending proposals
    /approve <proposal_id> - Approve a proposal
    /reject <proposal_id> - Reject a proposal
    /details <proposal_id> - Get proposal details
    """
    
    def __init__(self, token: str):
        """
        Initialize Telegram bot.
        
        Args:
            token: Telegram Bot API token
        """
        self.token = token
        logger.info("Telegram bot initialized (stub)")
    
    async def start(self) -> None:
        """
        Start the Telegram bot.
        """
        logger.info("Starting Telegram bot...")
        
        # TODO: Initialize python-telegram-bot
        # TODO: Register command handlers
        # TODO: Start polling
    
    async def stop(self) -> None:
        """
        Stop the Telegram bot.
        """
        logger.info("Stopping Telegram bot...")
        
        # TODO: Stop polling
        # TODO: Cleanup
    
    async def send_approval_request(
        self,
        chat_id: str,
        proposal_id: str,
        proposal_summary: str,
    ) -> bool:
        """
        Send an approval request via Telegram.
        
        Args:
            chat_id: Telegram chat ID
            proposal_id: Proposal needing approval
            proposal_summary: Brief proposal description
            
        Returns:
            True if sent successfully
        """
        logger.info(f"Sending Telegram approval request for {proposal_id}")
        
        # TODO: Send Telegram message with inline buttons
        
        return True


# Global bot instance
_telegram_bot: Optional[TelegramBot] = None


def get_telegram_bot() -> Optional[TelegramBot]:
    """
    Get or create the global Telegram bot.
    
    Returns None if Telegram is not configured.
    """
    global _telegram_bot
    
    if _telegram_bot is not None:
        return _telegram_bot
    
    settings = get_settings()
    
    # TODO: Add telegram_bot_token to config
    # if settings.telegram_bot_token:
    #     _telegram_bot = TelegramBot(settings.telegram_bot_token)
    #     return _telegram_bot
    
    logger.warning("Telegram bot not configured")
    return None
