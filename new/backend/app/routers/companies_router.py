"""
companies_router.py

- 국내 기업 정보는 DART-FSS 라이브러리를 통해 가져와서 DB에 저장
- 해외 기업 정보는 yfinance를 통해 가져와서 DB에 저장
- 저장된 기업 목록 조회
"""
from fastapi import APIRouter, HTTPException
import os
import logging
import dart_fss
import yfinance as yf

from ..database import get_db
from ..models import CompanyItem
from ..config import DART_API_KEY  # .env 에 DART_API_KEY 저장
from sqlite3 import Error

router = APIRouter()
logger = logging.getLogger(__name__)

# 1) DART-FSS 초기화
# .env에서 불러온 DART_API_KEY를 dart_fss에 설정
dart_fss.set_api_key(DART_API_KEY)

@router.get("/init-domestic")
def init_domestic_companies():
    """
    [국내 기업 초기화]
    - DART-FSS 라이브러리를 사용하여 상장기업 전체 목록을 가져옴
    - 회사 고유정보(corp_name, stock_code 등)를 데이터베이스에 저장
    - 시총(capital_stock) 제한 없이 모든 회사 정보를 저장
    """
    conn = get_db()
    cur = conn.cursor()
    try:
        # DART-FSS의 get_corp_list()로 상장사 전체 목록 가져오기
        corp_list = dart_fss.get_corp_list()

        # DB에 삽입 전 기존 데이터를 지우고 싶다면 아래 주석 해제
        # cur.execute("DELETE FROM companies WHERE country = 'KR'")

        count_inserted = 0

        for corp in corp_list:
            # DartFSS Corp 객체의 정보
            corp_name = corp.corp_name          # 예: "삼성전자"
            stock_code = corp.stock_code        # 예: "005930" (상장사만 존재)
            if not stock_code:
                # 비상장 기업인 경우 stock_code가 None일 수 있음
                continue

            # industry는 DartFSS가 제공하지 않을 수 있으므로 일단 빈 문자열
            # dart_fss에 sector 정보가 있을 수도 있지만, 정확도 보장은 안 됨
            industry = ""
            
            # market_cap도 기본적으로 0으로 설정 (여기서는 시총 제한 X)
            market_cap = 0

            # companies 테이블에 INSERT
            cur.execute("""
                INSERT INTO companies (corp_name, stock_code, country, industry, market_cap)
                VALUES (?, ?, ?, ?, ?)
            """, (corp_name, stock_code, "KR", industry, market_cap))
            count_inserted += 1

        conn.commit()
        return {"message": f"국내 기업 {count_inserted}개 정보를 DB에 저장 완료"}
    except Error as db_err:
        logger.error(f"DB 오류: {db_err}")
        return {"error": str(db_err)}
    except Exception as e:
        logger.error(f"[init-domestic] 기업 정보 저장 실패: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

@router.get("/init-foreign")
def init_foreign_companies():
    """
    [해외 기업 초기화]
    - yfinance 라이브러리를 통해 해외 기업 정보를 가져옴
    - 예시로 AAPL, MSFT, TSLA 등 일부 대형주를 DB에 저장
    - 실제로는 더 많은 티커 목록을 확장하거나, 사용자 입력으로 받는 식으로 구현 가능
    """
    # 원하는 해외 주식 티커들을 미리 정의
    foreign_tickers = ["AAPL", "MSFT", "TSLA"]

    conn = get_db()
    cur = conn.cursor()
    try:
        # DB에 삽입 전 기존 데이터를 지우고 싶다면 아래 주석 해제
        # cur.execute("DELETE FROM companies WHERE country = 'US'")

        count_inserted = 0

        for ticker in foreign_tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info

                # 예시로 longName, industry, sector 등을 가져옴
                corp_name = info.get("longName", ticker)  # 없으면 ticker로 대체
                stock_code = info.get("symbol", ticker)   # ticker 심볼
                # 'industry' 또는 'sector'가 없는 경우 대비
                industry = info.get("industry", "")
                # yfinance로 시가총액 구하기
                market_cap = info.get("marketCap", 0)

                # companies 테이블에 INSERT
                cur.execute("""
                    INSERT INTO companies (corp_name, stock_code, country, industry, market_cap)
                    VALUES (?, ?, ?, ?, ?)
                """, (corp_name, stock_code, "US", industry, market_cap))
                count_inserted += 1
            except Exception as yf_err:
                # 특정 티커가 잘못되었거나 데이터가 없을 수 있으므로 예외 처리
                logger.error(f"{ticker} 정보 가져오기 실패: {yf_err}")

        conn.commit()
        return {"message": f"해외 기업 {count_inserted}개 정보를 DB에 저장 완료"}
    except Error as db_err:
        logger.error(f"DB 오류: {db_err}")
        return {"error": str(db_err)}
    except Exception as e:
        logger.error(f"[init-foreign] 해외 기업 정보 저장 실패: {e}")
        return {"error": str(e)}
    finally:
        conn.close()

@router.get("/list-companies")
def list_companies(country: str = None):
    """
    [기업 목록 조회]
    - DB에 저장된 회사 목록을 조회
    - ?country=KR 또는 ?country=US 로 필터링 가능
    - 파라미터를 지정하지 않으면 모든 기업을 조회
    """
    query = "SELECT corp_name, stock_code, country, industry, market_cap FROM companies"
    params = []
    if country:
        query += " WHERE country = ?"
        params.append(country)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    # 결과를 JSON 형태로 반환
    result = []
    for r in rows:
        result.append({
            "corp_name": r["corp_name"],
            "stock_code": r["stock_code"],
            "country": r["country"],
            "industry": r["industry"],
            "market_cap": r["market_cap"]
        })
    return result
