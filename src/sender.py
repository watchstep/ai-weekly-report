"""Send Report to Teams/Slack"""

import requests

from config.settings import TEAMS_WEBHOOK_URL, SLACK_WEBHOOK_URL


def send_to_teams(report: str) -> bool:
    """Microsoft Teams로 발송 (Power Automate 호환)"""
    if not TEAMS_WEBHOOK_URL:
        print("⚠️ TEAMS_WEBHOOK_URL 미설정")
        return False
    
    # 리포트를 여러 섹션으로 분할 (4000자 제한)
    max_length = 3500
    report_text = report[:max_length]
    if len(report) > max_length:
        report_text += "\n\n... (전체 리포트는 GitHub Artifacts 참조)"
    
    # Adaptive Card 형식 (Power Automate 호환)
    card = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "📰 AI Weekly Report"
                        },
                        {
                            "type": "TextBlock",
                            "text": report_text,
                            "wrap": True,
                            "spacing": "Medium"
                        }
                    ]
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            json=card,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Power Automate는 200 또는 202 반환
        if response.status_code in [200, 202]:
            print("✅ Teams 발송 완료")
            return True
        else:
            print(f"❌ Teams 발송 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Teams 발송 실패: {e}")
        return False


def send_to_slack(report: str) -> bool:
    """Slack으로 발송 (Block Kit 형식)"""
    if not SLACK_WEBHOOK_URL:
        print("⚠️ SLACK_WEBHOOK_URL 미설정")
        return False
    
    # Slack Block Kit 형식 (Markdown 지원)
    # 블록당 3000자 제한
    max_block_length = 3000
    report_text = report[:max_block_length]
    
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📰 AI Weekly Report",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": report_text
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        # Slack은 성공 시 "ok" 반환
        if response.status_code == 200 and response.text == "ok":
            print("✅ Slack 발송 완료")
            return True
        else:
            print(f"❌ Slack 발송 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Slack 발송 실패: {e}")
        return False


def send_report(report: str):
    """설정된 채널로 리포트 발송"""
    teams_sent = False
    slack_sent = False
    
    if TEAMS_WEBHOOK_URL:
        teams_sent = send_to_teams(report)
    
    if SLACK_WEBHOOK_URL:
        slack_sent = send_to_slack(report)
    
    if not TEAMS_WEBHOOK_URL and not SLACK_WEBHOOK_URL:
        print("⚠️ 발송 채널이 설정되지 않았습니다.")
    
    return teams_sent or slack_sent