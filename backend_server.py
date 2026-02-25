from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # CORS 허용

# 지원하는 주식 목록
STOCK_LIST = {
    'US': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA'],
    'KR': ['005930.KS', '000660.KS', '005380.KS', '035420.KS', 
           '035720.KS', '006400.KS', '051910.KS', '207940.KS']
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'ok',
        'message': 'AI Trading Simulator Backend is running'
    })

@app.route('/api/stocks', methods=['GET'])
def get_stock_list():
    """지원하는 주식 목록 반환"""
    return jsonify({
        'US': STOCK_LIST['US'],
        'KR': STOCK_LIST['KR']
    })

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """특정 주식의 과거 데이터 가져오기"""
    try:
        # 기간 설정 (기본 1년)
        period = request.args.get('period', '1y')
        
        # yfinance로 데이터 가져오기
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return jsonify({
                'error': f'No data found for {symbol}'
            }), 404
        
        # 데이터 가공
        data = []
        for date, row in hist.iterrows():
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(float(row['Open']), 2),
                'high': round(float(row['High']), 2),
                'low': round(float(row['Low']), 2),
                'close': round(float(row['Close']), 2),
                'price': round(float(row['Close']), 2),
                'volume': int(row['Volume'])
            })
        
        # 주식 정보
        info = ticker.info
        
        return jsonify({
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'currency': info.get('currency', 'USD'),
            'exchange': info.get('exchange', 'Unknown'),
            'sector': info.get('sector', 'Unknown'),
            'data': data[-100:]  # 최근 100일만
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/stock/<symbol>/latest', methods=['GET'])
def get_latest_price(symbol):
    """실시간 최신 가격 가져오기"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='1d')
        
        if hist.empty:
            return jsonify({
                'error': f'No data found for {symbol}'
            }), 404
        
        latest = hist.iloc[-1]
        
        return jsonify({
            'symbol': symbol,
            'price': round(float(latest['Close']), 2),
            'open': round(float(latest['Open']), 2),
            'high': round(float(latest['High']), 2),
            'low': round(float(latest['Low']), 2),
            'volume': int(latest['Volume']),
            'timestamp': hist.index[-1].strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/stock/<symbol>/info', methods=['GET'])
def get_stock_info(symbol):
    """주식 상세 정보 가져오기"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return jsonify({
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'marketCap': info.get('marketCap', 0),
            'currency': info.get('currency', 'USD'),
            'exchange': info.get('exchange', 'Unknown'),
            'website': info.get('website', ''),
            'description': info.get('longBusinessSummary', '')
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/stock/<symbol>/technical', methods=['GET'])
def get_technical_indicators(symbol):
    """기술적 지표 계산"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='3mo')
        
        if hist.empty:
            return jsonify({
                'error': f'No data found for {symbol}'
            }), 404
        
        # 이동평균선
        hist['SMA20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        
        # RSI 계산
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # 최근 데이터
        latest = hist.iloc[-1]
        
        return jsonify({
            'symbol': symbol,
            'sma20': round(float(latest['SMA20']), 2) if not pd.isna(latest['SMA20']) else None,
            'sma50': round(float(latest['SMA50']), 2) if not pd.isna(latest['SMA50']) else None,
            'rsi': round(float(latest['RSI']), 2) if not pd.isna(latest['RSI']) else 50,
            'price': round(float(latest['Close']), 2)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("="*50)
    print("🚀 AI Trading Simulator Backend Starting...")
    print("="*50)
    print("📊 Supported stocks:")
    print(f"   US: {', '.join(STOCK_LIST['US'])}")
    print(f"   KR: {', '.join(STOCK_LIST['KR'])}")
    print("="*50)
    print("🌐 Server running on http://localhost:5000")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
