"""
HITL Notification Service

Sends approval requests to human via multiple channels.

Design principles:
- Multi-channel notifications
- Non-blocking
- Retry logic
- Audit trail
"""

from typing import Optional
from uuid import UUID

from app.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    """
    Service for sending HITL approval notifications.
    
    Sends notifications via:
    - Web UI (WebSocket or polling)
    - Telegram Bot
    """
    
    async def send_approval_request(
        self,
        proposal_id: UUID,
        proposal_data: dict,
        urgency: str = "normal",
    ) -> bool:
        """
        Send an approval request notification.
        
        Args:
            proposal_id: Which proposal needs approval
            proposal_data: Proposal details
            urgency: Urgency level (low, normal, high)
            
        Returns:
            True if notification sent successfully
        """
        logger.info(
            f"Sending approval request for proposal {proposal_id}",
            extra={"urgency": urgency},
        )
        
        # TODO: Send to Web UI (via WebSocket or database flag)
        # TODO: Send to Telegram Bot
        
        return True
    
    async def send_execution_complete(
        self,
        action_id: UUID,
        outcome: dict,
    ) -> bool:
        """
        Notify human that an action has been executed.
        
        Args:
            action_id: Which action was executed
            outcome: Execution outcome
            
        Returns:
            True if notification sent successfully
        """
        logger.info(f"Sending execution complete notification for action {action_id}")
        
        # TODO: Send to Web UI
        # TODO: Send to Telegram Bot
        
        return True


# Global notification service instance
_notification_service: Optional[NotificationService] = None


def get_notification_service() -> NotificationService:
    """
    Get or create the global notification service.
    """
    global _notification_service
    
    if _notification_service is None:
        _notification_service = NotificationService()
    
    return _notification_service
