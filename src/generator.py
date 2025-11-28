"""Generate Report with Gemini API"""

from datetime import datetime, timedelta

from google import genai
from google.genai import types
from jinja2 import Environment, FileSystemLoader

from config.paths import PROMPTS_DIR, REPORT_FILE


def get_week_info() -> dict:
    """지난 주 월요일-일요일 기준 주차 정보 계산
    
    예시 (오늘 = 11/28 금요일):
    - today.weekday() = 4 (금요일)
    - last_monday = 11/28 - 11 = 11/17
    - last_sunday = 11/17 + 6 = 11/23
    - week_of_month = (17-1)//7+1 = 3 (11월 3주차)
    """
    today = datetime.now()
    
    # 지난 주 월요일 ~ 일요일 (수집 대상 기간)
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    
    # 주차 계산: 지난 월요일이 해당 월의 몇 주차인지
    # 1일~7일: 1주차, 8일~14일: 2주차, 15일~21일: 3주차, 22일~28일: 4주차
    week_of_month = (last_monday.day - 1) // 7 + 1
    
    return {
        "today": today.strftime("%Y-%m-%d"),
        "month": last_monday.month,
        "week": week_of_month,
        "start_date": last_monday.strftime("%m/%d"),  # 11/17 형식
        "end_date": last_sunday.strftime("%m/%d"),    # 11/23 형식
        "start_date_full": last_monday.strftime("%Y-%m-%d"),
        "end_date_full": last_sunday.strftime("%Y-%m-%d"),
    }


def load_prompt(template_name: str, **kwargs) -> str:
    """Jinja2 템플릿 렌더링"""
    env = Environment(loader=FileSystemLoader(PROMPTS_DIR))
    template = env.get_template(template_name)
    return template.render(**kwargs)


def generate_report(articles: list[dict]) -> str:
    """Gemini API로 리포트 생성"""
    
    # 클라이언트 생성 (GOOGLE_API_KEY 환경변수 자동 인식)
    client = genai.Client()
    
    # 프롬프트 준비
    system_prompt = load_prompt("system.j2")
    week_info = get_week_info()
    
    # 최대 50개 기사만 전달 (토큰 제한)
    articles_to_use = articles[:50]
    
    user_prompt = load_prompt(
        "user.j2",
        articles=articles_to_use,
        total_articles=len(articles),  # 전체 수집 기사 수
        **week_info
    )
    
    print(f"🤖 Gemini로 리포트 생성 중...")
    print(f"   📅 기간: {week_info['month']}월 {week_info['week']}주차 ({week_info['start_date']} - {week_info['end_date']})")
    print(f"   📰 기사: {len(articles)}개 수집 → {len(articles_to_use)}개 분석")
    
    # API 호출
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
        ),
    )
    
    return response.text


def save_report(report: str):
    """리포트를 마크다운 파일로 저장"""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"📄 리포트 저장: {REPORT_FILE}")


if __name__ == "__main__":
    import json
    from config.paths import ARTICLES_FILE
    
    with open(ARTICLES_FILE, encoding="utf-8") as f:
        articles = json.load(f)
    
    report = generate_report(articles)
    save_report(report)
    print(report)