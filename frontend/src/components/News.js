import NewsCard from "./NewsCard"
import "./News.css"
/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config/api";
import { ThumbsUp, ThumbsDown, Building2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
function News() {
  const [articles, setArticles] = useState([
		{
			title: "Trump’s Immigration Crackdown Could Play Havoc with the Economy",
			link: "https://www.msn.com/en-us/money/other/trump-s-immigration-crackdown-could-play-havoc-with-the-economy/ar-AA1xYHcR",
			summary:
				"If the Trump administration succeeds in deporting millions of immigrants, it will slow economic growth and productivity gains.",
			sentiment: "부정",
			companies: [],
		},
		{
			title: "Analysis-Global Economy Takes Trump Guessing-Game in Stride",
			link: "https://www.usnews.com/news/top-news/articles/2025-01-27/analysis-global-economy-takes-trump-guessing-game-in-stride",
			summary:
				"FRANKFURT (Reuters) - Global economic policymakers had been braced for an economic firestorm from the new U.S. administration but instead got a surprisingly restrained start from Donald Trump, who remains big on rhetoric but more cautious on action - for now.",
			sentiment: "부정",
			companies: ["NEW"],
		},
		{
			title: "The Arrival Of DeepSeek Is Unambiguously Great For The U.S. Economy",
			link: "https://www.forbes.com/sites/johntamny/2025/01/27/the-arrival-of-deepseek-is-unambiguously-great-for-the-us-economy/",
			summary:
				"What’s produced outside the U.S. will have the same economic impact as what's produced within. Or more realistically, a much greater economic impact.",
			sentiment: "부정",
			companies: [],
		},
		{
			title: "Could a ‘nightlife manager’ help revitalize Providence’s after-dark economy?",
			link: "https://www.bostonglobe.com/2025/01/27/metro/providence-nightlife-mayor-economy-entertainment-tourism-sector-night/",
			summary:
				"The sector is a critical part of the city’s character, but revenue remains below pre-COVID levels and business owners say they need support. “So many of us in city government are so oriented around the traditional 9-to-5 and not the other 9-to-5,",
			sentiment: "부정",
			companies: ["LS"],
		},
		{
			title:
				"The Russian war economy is facing a ‘moment of truth’ as Putin’s dwindling cash reserves raise odds of a financial crash, expert says",
			link: "https://www.msn.com/en-us/money/markets/the-russian-war-economy-is-facing-a-moment-of-truth-as-putin-s-dwindling-cash-reserves-raise-odds-of-a-financial-crash-expert-says/ar-AA1xUiHo",
			summary:
				"As the risk of a financial crash rises, Russia’s imperiled economy is about to pose serious constraints on Putin’s war.”",
			sentiment: "부정",
			companies: ["SK"],
		},
		{
			title:
				"The U.S. economy was already revved up before Trump took office. Could it get a lot better?",
			link: "https://www.msn.com/en-us/money/economy/the-u-s-economy-was-already-revved-up-before-trump-took-office-could-it-get-a-lot-better/ar-AA1xQl0R",
			summary:
				"Donald Trump has vowed to turbo-charge the U.S. economy, but it’s been expanding well above its typical speed for more than two years and it probably finished 2024 with another burst of strong growth.",
			sentiment: "부정",
			companies: [],
		},
		{
			title:
				"How much do working immigrants help Mississippi economy, pay taxes? What does state spend?",
			link: "https://www.usatoday.com/story/news/2025/01/27/immigrants-pay-mississippi-taxes-work-ms-spend-local-business-what-cost-state-illegal-immigration/77906212007/",
			summary:
				"Immigrants in U.S. illegally work in Mississippi communities, pay taxes, shop at local businesses. What does illegal immigration cost the state?",
			sentiment: "부정",
			companies: ["EG"],
		},
		{
			title: "The economy's strong. Why are more Americans barely making credit card payments?",
			link: "https://www.usatoday.com/story/money/personalfinance/2025/01/26/economic-warning-behind-credit-cards-financial-stress/77887274007/",
			summary:
				"Despite a strong economy, the share of Americans making only the minimum credit card payment hit a 12-year high and delinquenices are rising.",
			sentiment: "부정",
			companies: ["NICE"],
		},
		{
			title: "Science Park says it adds £50m into economy",
			link: "https://www.bbc.com/news/articles/c2d33ndkd2wo",
			summary:
				"Exeter Science Park says it is generating £50m for the local economy and for the first time in its 10-year history, is balancing the books financially. Previously, it had required additional funding to remain viable as it struggled to repay council loans.",
			sentiment: "긍정",
			companies: [],
		},
		{
			title: "Thailand sees economy growing up to 3.5% this year on stimulus, foreign investment",
			link: "https://www.msn.com/en-us/money/markets/thailand-sees-economy-growing-up-to-3-5-this-year-on-stimulus-foreign-investment/ar-AA1xVlhI",
			summary:
				"Thailand's economy is expected to grow between 3% and 3.5% this year, driven by stimulus measures and strong foreign investment, while tourist numbers should surpass 2024 figures, the finance minister said on Monday.",
			sentiment: "부정",
			companies: [],
		},
		{
			title: "전남도, 경제위기 속 민생경제 활성화 5대 지원책 온힘",
			link: "http://www.breaknews.com/1088297",
			summary:
				"지역경제 활성화도 도모한다. 전남도와 시군 공공기관, 민간기업, 금융기관 등... Jeollanam-do, 5 major support measures to vitalize the people's economy amid economic crisis Province... ",
			sentiment: "긍정",
			companies: [],
		},
		{
			title: "생성형 AI가 경제도 예측…경영진 발언 분석해 GDP 적중",
			link: "https://n.news.naver.com/mnews/article/092/0002360044?sid=105",
			summary:
				"금융위기와 팬데믹 시기의 예측력 검증 연구진이 개발한 AI Economy Score는 2008년 금융위기 시기의 경제 하락을 정확하게 예측했다. 다만 2020년 코로나19 팬데믹의 경우 첫 분기 GDP 성장률 예측에는 실패했는데... ",
			sentiment: "부정",
			companies: [],
		},
		{
			title: "충북도-충북신용보증재단-NH농협은행, 소상공인 금융지원 협약",
			link: "http://www.breaknews.com/1087044",
			summary:
				"충청북도 경제 활력 제고를 위한 ‘충청북도 소기업.소상공인 금융지원... local economy, Chungcheongbuk-do, Chungcheongbuk-do Credit Guarantee Foundation, and financial institutions will work... ",
			sentiment: "긍정",
			companies: [],
		},
		{
			title: "화성특례시, ‘민생경제 활성화 종합대책’ 선도적 추진",
			link: "http://www.breaknews.com/1087975",
			summary:
				"지역 경제의 중요한 역할을 담당하는 중소기업을 대상으로 금융 부담을 대폭... People's Economy'. Hwaseong Special City plans to execute 62% of this year's budget in the first half of the... ",
			sentiment: "긍정",
			companies: ["LF", "대상"],
		},
		{
			title: '[토큰포스트 마감 브리핑] 금융위원장 "법인 가상자산 계좌 허용·스테...',
			link: "https://www.tokenpost.kr/article-216485",
			summary:
				'플레이 경제(Play Economy) 모델을 구축할 예정이라고 밝혔다. 솔라나 옵션 블록 트레이드...2월 말 $400 베팅... 금융위원장 "법인 가상자산 계좌 허용·스테이블코인 입법 속도 내겠다" 뉴스1에 따르면 김병환... ',
			sentiment: "부정",
			companies: ["레이"],
		},
		{
			title: "경기도, 1분기 35% 11조원 재정집행으로 민생경제 회복 앞장",
			link: "http://www.breaknews.com/1087134",
			summary:
				"김동연 지사는 연초부터 경제살리기 현장방문을 진행 중이다. 1월 13일 설렁탕집에서 신년 기자회견을 연 데 이어 14일 시흥시에서는 자영업자를 대상으로 금융상담... ",
			sentiment: "부정",
			companies: ["대상"],
		},
		{
			title: "현대차·기아, 1차 부품 협력사 매출 90조 돌파..국가경제 기여",
			link: "http://www.breaknews.com/1086818",
			summary:
				"국가경제에 기여하고 있는 것으로 조사됐다. 이들 협력사들의 매출액은 2023년... Contribution to National Economy Among the first-tier suppliers that directly supply parts to Hyundai Motor... ",
			sentiment: "긍정",
			companies: [],
		},
		{
			title: "대구신용보증재단, 신한은행과‘중소기업·소상공인 금융지원 협약보증...",
			link: "http://www.breaknews.com/1087613",
			summary:
				"지역 경제를 위해 재단과 은행이 함께 힘을 모았다”라며, “이자비용 부담과 자금조달 어려움을 겪는 기업에 대한 금융지원을 확대하기 위해 은행과의 협업체계를... ",
			sentiment: "긍정",
			companies: [],
		},
		{
			title: "대구시, 서민경제 위기 극복 지원...中企.소상공인 지원 나선다",
			link: "http://www.breaknews.com/1086538",
			summary:
				"관내 금융 사각지대를 해소하고 지역 경제 회복을 가속화할 방침이다. 특성화... > Daegu City, Focused Support for ‘Overcoming the People’s Economy Crisis’... Establishing Support... ",
			sentiment: "긍정",
			companies: ["EG"],
		},
		{
			title: "광주시-76개 기관·단체 원팀 뭉쳐 ‘광주경제 다함께 착착착’ 펼친다",
			link: "http://www.breaknews.com/1087812",
			summary:
				"강 시장은 이어 “광주의 경제·금융계, 시의회, 공공기관, 지자체 등 광주를... Gwangju City-76 organizations and groups unite as one team to unfold ‘Gwangju Economy Together, Step by... ",
			sentiment: "긍정",
			companies: [],
		},
	]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);
	const navigate = useNavigate();
	useEffect(() => {
		const getNews = async () => {
			try {
				const response = await axios.get(`${API_BASE_URL}/news/`);
				setArticles(response.data);
				console.log(response.data);
			} catch (err) {
				setError(err.message);
			} finally {
				setLoading(false);
			}
		};
		setLoading(false);
		// getNews();
	}, []);

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">경제 뉴스 대시보드</h1>
      <div className="row">
        {articles.map((news, index) => (
          <div className="col-md-4 mb-4" key={index}>
            <NewsCard news={news} />
          </div>
        ))}
      </div>
    </div>
  )
}

export default News

