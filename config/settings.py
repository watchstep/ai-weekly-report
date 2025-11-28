import os
from dotenv import load_dotenv
from config.paths import ENV_FILE

# .env 파일 로드
load_dotenv(ENV_FILE)

# API 키 (google-genai SDK는 GOOGLE_API_KEY 우선 인식)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Webhook URLs (선택)
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")