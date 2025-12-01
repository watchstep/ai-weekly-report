# 📰 AI Weekly Report Generator

Automatically collect AI news from RSS feeds, generate weekly trend reports using Gemini API, and send to Teams/Slack.


## ✨ Features

- **RSS Collection**: Auto-collect articles from 50+ AI-related feeds (previous Mon-Sun)
- **Report Generation**: Summarize trends into 6 categories using Gemini 2.5 Flash
- **Auto Delivery**: Send via Teams/Slack Webhook every Monday
- **Scheduling**: Run automatically with GitHub Actions

## 🛠 How It Works

```
OPML (RSS list) → feedparser (collect) → Gemini API (analyze) → Webhook (send)
```

| Step | Tool | Description |
|------|------|-------------|
| Collect | feedparser | Filter articles from previous Mon-Sun |
| Analyze | google-genai | Jinja2 prompt + Gemini 2.5 Flash |
| Send | requests | Teams Adaptive Card / Slack Block |


## 📁 Project Structure

```
ai-weekly-report/
├── config/
│   ├── paths.py          # Path configuration
│   └── settings.py       # Environment variables
├── data/
│   └── ai-feeds.opml     # RSS feed list
├── prompts/
│   ├── system.j2         # System prompt (selection criteria)
│   └── user.j2           # User prompt (output format)
├── src/
│   ├── collector.py      # RSS collection
│   ├── generator.py      # Gemini report generation
│   └── sender.py         # Webhook delivery
├── main.py               # Entry point
├── requirements.txt
├── .env                  # API keys (git ignored)
└── .github/
    └── workflows/
        └── weekly-report.yml
```

## 🚀 Usage

### 1. Fork/Clone Repository

```bash
git clone https://github.com/your-username/ai-weekly-report.git
cd ai-weekly-report
```

### 2. Register GitHub Secrets (Required)

Go to **Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|------|-------|
| `GOOGLE_API_KEY` | Your Gemini API Key |
| `TEAMS_WEBHOOK_URL` | Your Teams Webhook URL |
| `SLACK_WEBHOOK_URL` | Your Slack Webhook URL (optional) |

> ⚠️ **Do NOT push `.env` file.** Use GitHub Secrets for security.

### 3. Enable Workflow

Actions tab → "Weekly AI Report" → Enable workflow

### 4. Run

- **Auto**: Every Monday 10:00 AM KST
- **Manual**: Actions → Run workflow

## 📅 Output Example

```markdown
## 📰 지난 주 AI 트렌드 정리: 11월 3주차 (11/17 - 11/23)

---
📊 **지난 주 통계**
- 수집된 기사: 73개
- 선별된 기사: 24개  
- 카테고리별: Tool(4), Product(5), Model(5), Paper(4), Trend(3), Business(3)
---

### 🤖 Model
- **[Google]** Gemini 3 출시, LMArena 1501 Elo 달성 (11/18) [[원문](https://...)]
- **[OpenAI]** GPT-5.1 Codex Max 공개, compaction 기술 도입 (11/19) [[원문](https://...)]

...
```