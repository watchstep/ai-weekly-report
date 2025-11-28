"""Send Report to Teams/Slack"""

import requests

from config.settings import TEAMS_WEBHOOK_URL, SLACK_WEBHOOK_URL


def send_to_teams(report: str) -> bool:
    """Microsoft Teams로 발송"""
    if not TEAMS_WEBHOOK_URL:
        print("⚠️ TEAMS_WEBHOOK_URL 미설정")
        return False
    
    payload = {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": [{
                    "type": "TextBlock",
                    "text": report[:4000],
                    "wrap": True
                }]
            }
        }]
    }
    
    try:
        response = requests.post(TEAMS_WEBHOOK_URL, json=payload, timeout=30)
        response.raise_for_status()
        print("✅ Teams 발송 완료")
        return True
    except Exception as e:
        print(f"❌ Teams 발송 실패: {e}")
        return False


def send_to_slack(report: str) -> bool:
    """Slack으로 발송"""
    if not SLACK_WEBHOOK_URL:
        print("⚠️ SLACK_WEBHOOK_URL 미설정")
        return False
    
    payload = {
        "text": report[:3000]
    }
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=30)
        response.raise_for_status()
        print("✅ Slack 발송 완료")
        return True
    except Exception as e:
        print(f"❌ Slack 발송 실패: {e}")
        return False


def send_report(report: str):
    """설정된 채널로 리포트 발송"""
    if TEAMS_WEBHOOK_URL:
        send_to_teams(report)
    if SLACK_WEBHOOK_URL:
        send_to_slack(report)