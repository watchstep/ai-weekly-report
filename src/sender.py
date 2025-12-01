"""Send Report to Teams/Slack"""

import time
import requests

from config.settings import TEAMS_WEBHOOK_URL, SLACK_WEBHOOK_URL


"""Send Report to Teams/Slack"""

import time
import requests

from config.settings import TEAMS_WEBHOOK_URL, SLACK_WEBHOOK_URL


def _format_report_for_teams(report: str) -> str:
    """Teams Adaptive Card에서 잘 보이도록 간단 전처리"""
    text = report

    # [[원문](url)] 같은 패턴을 [원문](url) 로 정리
    text = text.replace("[[원문]", "[원문]")
    text = text.replace("[[원문 ", "[원문 ")

    # 필요하면 여기서 추가 치환 가능
    return text


def _chunk_text(text: str, chunk_size: int = 4000) -> list[str]:
    """길이를 제한하지 않고. 카드 안에서만 잘게 나눠 여러 TextBlock으로 넣기"""
    if not text:
        return [""]
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def send_to_teams(report: str) -> bool:
    """Microsoft Teams로 발송 (Power Automate 호환)"""
    if not TEAMS_WEBHOOK_URL:
        print("⚠️ TEAMS_WEBHOOK_URL 미설정")
        return False

    # 전체 리포트를 전처리하고. 카드 안에서만 여러 블록으로 나눔. 잘라서 버리지는 않음
    processed = _format_report_for_teams(report)
    chunks = _chunk_text(processed, chunk_size=4000)

    # 카드 본문 구성.
    body_blocks = []

    for i, chunk in enumerate(chunks):
        body_blocks.append(
            {
                "type": "TextBlock",
                "wrap": True,
                "spacing": "Medium" if i == 0 else "Small",
                "text": chunk,
            }
        )

    card = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "body": body_blocks,
                },
            }
        ],
    }

    try:
        print("📡 HTTP 요청 전송 중...")
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            json=card,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        print(f"📡 HTTP 상태 코드: {response.status_code}")
        print(f"📡 응답 본문: {response.text}")

        if response.status_code in [200, 202]:
            print("✅ Teams 발송 완료")
            return True
        else:
            print(f"❌ Teams 발송 실패: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Teams 발송 실패: {e}")
        import traceback

        traceback.print_exc()
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