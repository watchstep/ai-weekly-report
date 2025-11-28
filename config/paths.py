from pathlib import Path

# 프로젝트 루트
ROOT = Path(__file__).parent.parent

# 주요 디렉토리
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
PROMPTS_DIR = ROOT / "prompts"
SRC_DIR = ROOT / "src"

# 데이터 파일
OPML_FILE = DATA_DIR / "ai-feeds.opml"
ARTICLES_FILE = DATA_DIR / "raw_articles.json"
REPORT_FILE = DATA_DIR / "weekly_report.md"

# 프롬프트 템플릿
SYSTEM_PROMPT = PROMPTS_DIR / "system.j2"
USER_PROMPT = PROMPTS_DIR / "user.j2"

# 환경변수 파일
ENV_FILE = ROOT / ".env"