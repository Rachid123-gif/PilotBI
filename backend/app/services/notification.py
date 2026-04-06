"""
Notification service for email (Resend) and WhatsApp (Twilio).
"""

from __future__ import annotations

import logging
from typing import Any, Dict

import resend
from twilio.rest import Client as TwilioClient

from app.config import get_settings
from app.models.enums import AlertCondition

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Email via Resend
# ---------------------------------------------------------------------------

async def send_email(to: str, subject: str, html_body: str) -> str | None:
    """
    Send an email using the Resend API.

    Returns the email ID on success, or None on failure.
    """
    settings = get_settings()
    resend.api_key = settings.RESEND_API_KEY

    try:
        result = resend.Emails.send({
            "from": settings.RESEND_FROM_EMAIL,
            "to": [to],
            "subject": subject,
            "html": html_body,
        })
        email_id = result.get("id")
        logger.info("Email sent to %s (id=%s)", to, email_id)
        return email_id
    except Exception:
        logger.exception("Failed to send email to %s", to)
        return None


# ---------------------------------------------------------------------------
# WhatsApp via Twilio
# ---------------------------------------------------------------------------

async def send_whatsapp(to: str, message: str) -> str | None:
    """
    Send a WhatsApp message using the Twilio API.

    Parameters
    ----------
    to : str
        Recipient phone number in E.164 format (e.g. "+212600000000").
    message : str
        Message body text.

    Returns the message SID on success, or None on failure.
    """
    settings = get_settings()

    try:
        client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            from_=f"whatsapp:{settings.TWILIO_WHATSAPP_FROM}",
            to=f"whatsapp:{to}",
            body=message,
        )
        logger.info("WhatsApp sent to %s (sid=%s)", to, msg.sid)
        return msg.sid
    except Exception:
        logger.exception("Failed to send WhatsApp to %s", to)
        return None


# ---------------------------------------------------------------------------
# Alert notification dispatcher
# ---------------------------------------------------------------------------

CONDITION_LABELS = {
    AlertCondition.ABOVE.value: "au-dessus de",
    AlertCondition.BELOW.value: "en-dessous de",
    AlertCondition.CHANGE_PCT.value: "variation de plus de",
}


def _build_alert_email(alert: Dict[str, Any], actual_value: float) -> tuple[str, str]:
    """Build email subject and HTML body for an alert notification."""
    condition_label = CONDITION_LABELS.get(alert["condition"], alert["condition"])
    threshold = alert["threshold"]
    kpi_type = alert.get("kpi_type", "")

    subject = f"[PilotBI] Alerte : {alert['name']}"

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: #2563EB; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
            <h1 style="margin: 0; font-size: 20px;">PilotBI - Alerte Declenchee</h1>
        </div>
        <div style="padding: 24px; background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 0 0 8px 8px;">
            <h2 style="color: #1F2937; margin-top: 0;">{alert['name']}</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; color: #6B7280;">KPI</td>
                    <td style="padding: 8px 0; font-weight: bold;">{kpi_type}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6B7280;">Condition</td>
                    <td style="padding: 8px 0;">{condition_label} {threshold:,.2f}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #6B7280;">Valeur actuelle</td>
                    <td style="padding: 8px 0; font-weight: bold; color: #DC2626;">{actual_value:,.2f}</td>
                </tr>
            </table>
            <p style="margin-top: 20px; color: #6B7280; font-size: 14px;">
                Connectez-vous a votre tableau de bord PilotBI pour plus de details.
            </p>
        </div>
    </div>
    """
    return subject, html


def _build_alert_whatsapp(alert: Dict[str, Any], actual_value: float) -> str:
    """Build WhatsApp message text for an alert notification."""
    condition_label = CONDITION_LABELS.get(alert["condition"], alert["condition"])
    return (
        f"*PilotBI - Alerte*\n\n"
        f"_{alert['name']}_\n"
        f"KPI: {alert.get('kpi_type', '')}\n"
        f"Condition: {condition_label} {alert['threshold']:,.2f}\n"
        f"Valeur actuelle: *{actual_value:,.2f}*\n\n"
        f"Connectez-vous a PilotBI pour plus de details."
    )


async def notify_alert(db: Any, alert: Dict[str, Any], actual_value: float) -> None:
    """
    Send alert notifications via configured channels.

    Looks up the organization members' contact info to send
    email and/or WhatsApp notifications.
    """
    org_id = alert.get("organization_id")
    created_by = alert.get("created_by")

    # Fetch the alert creator's contact info
    if created_by:
        profile_result = (
            db.table("profiles")
            .select("email, phone")
            .eq("id", created_by)
            .maybe_single()
            .execute()
        )
    else:
        profile_result = (
            db.table("profiles")
            .select("email, phone")
            .eq("organization_id", org_id)
            .limit(1)
            .execute()
        )

    profile = profile_result.data if profile_result.data else None

    if not profile:
        logger.warning("No profile found for alert notification (org=%s)", org_id)
        return

    # Handle single result vs list
    if isinstance(profile, list):
        profile = profile[0]

    # Send email
    if alert.get("notify_email") and profile.get("email"):
        subject, html = _build_alert_email(alert, actual_value)
        await send_email(profile["email"], subject, html)

    # Send WhatsApp
    if alert.get("notify_whatsapp") and profile.get("phone"):
        message = _build_alert_whatsapp(alert, actual_value)
        await send_whatsapp(profile["phone"], message)
