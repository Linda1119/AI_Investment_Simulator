# 📈 AI 투자 학습 시뮬레이터

실제 주식 데이터를 기반으로 투자를 연습할 수 있는 웹 시뮬레이터입니다.

## 🛠 Tech Stack
- **Frontend**: HTML, CSS, JavaScript (Single File)
- **Backend**: Python, Flask
- **Data**: yfinance (실시간 주식 데이터)

## ✨ 주요 기능
- 미국/한국 주식 실시간 가격 조회
- 주식 매수/매도 시뮬레이션
- 스탑로스 자동 매도 설정
- AI 예측 차트 (30일)
- 실제 주가 차트 조회
- 포트폴리오 수익률 추적
- 매수/매도 호가 표시

## 📦 지원 종목
- **미국**: AAPL, GOOGL, MSFT, TSLA, AMZN, META, NVDA
- **한국**: 삼성전자, SK하이닉스, 현대차 등

## 🚀 실행 방법
```bash
pip install flask flask-cors yfinance pandas
python backend_server.py
```
이후 `FRONTED_FIN_FIXED.html` 브라우저로 열기
