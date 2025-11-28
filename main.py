"""AI Weekly Report"""

import sys
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).parent))

from src.collector import collect_all, save_articles
from src.generator import generate_report, save_report
from src.sender import send_report


def main():
    print("=" * 50)
    print("🚀 AI Weekly Report Generator")
    print("=" * 50)
    
    # 1. RSS 피드 수집
    print("\n[1/3] RSS 피드 수집")
    articles = collect_all()
    save_articles(articles)
    
    if not articles:
        print("❌ 수집된 기사 없음")
        return
    
    # 2. Gemini로 리포트 생성
    print("\n[2/3] 리포트 생성")
    report = generate_report(articles)
    save_report(report)
    
    # 3. Teams/Slack 발송
    print("\n[3/3] 리포트 발송")
    send_report(report)
    
    print("\n" + "=" * 50)
    print("✅ 완료!")
    print("=" * 50)
    
    # 미리보기
    print("\n📋 리포트 미리보기:\n")
    print(report[:1500] + "..." if len(report) > 1500 else report)


if __name__ == "__main__":
    main()