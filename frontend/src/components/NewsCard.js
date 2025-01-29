import React from "react";
import "./NewsCard.css";

export default function NewsCard({ news }) {
	const handleCardClick = (link) => {
		window.open(link, "_blank");
	};

	return (
		<div
			className={`news-card ${news.sentiment === "긍정" ? "positive" : news.sentiment === "부정" ? "negative" : "neutral"}`}
			onClick={() => handleCardClick(news.link)}>
			<div>
				<h2>{news.title}</h2>
				<p>{news.summary}</p>
			</div>
			<div className="news-footer">
				<span className="sentiment">
					{news.sentiment === "긍정" ? "GOOD" : news.sentiment === "부정" ? "BAD" : "NEUTRAL"}
				</span>
				{news.companies.length > 0 && (
					<div className="companies">
						{news.companies.map((company, index) => (
							<span key={index} className="company-tag">
								{company}
							</span>
						))}
					</div>
				)}
			</div>
		</div>
	);
}
