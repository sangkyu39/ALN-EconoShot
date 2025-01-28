import React from "react";
function NewsCard({ news }) {
	const handleCardClick = (link) => {
		window.open(link, "_blank"); // 새 창에서 링크 열기
	};

	return (
		<div
			className={`card h-100 shadow-sm ${
				news.sentiment === "긍정" ? "border-success" : "border-danger"
			}`}>
			<div className="card-body d-flex flex-column" onClick={() => handleCardClick(news.link)}>
				<h5 className="card-title mb-3 fw-bold">
					<span
						className="text-decoration-none text-dark"
						target="_blank"
						rel="noopener noreferrer">
						{news.title}
					</span>
				</h5>
				<p className="card-text flex-grow-1 mb-4 text-muted">{news.summary}</p>
				<div className="mt-auto d-flex justify-content-between align-items-center">
					<span
						className={`badge ${
							news.sentiment === "긍정" ? "bg-success" : "bg-danger"
						} d-flex align-items-center p-2`}>
						<i
							className={`bi ${
								news.sentiment === "긍정" ? "bi-hand-thumbs-up" : "bi-hand-thumbs-down"
							} me-1`}></i>
						{news.sentiment}
					</span>
					{news.companies.length > 0 && (
						<div className="d-flex align-items-center">
							<i className="bi bi-building me-2 text-primary"></i>
							<div className="companies-scroll">
								{news.companies.map((company, index) => (
									<span key={index} className="badge bg-light text-dark me-1">
										{company}
									</span>
								))}
							</div>
						</div>
					)}
				</div>
			</div>
		</div>
	);
}

export default NewsCard;
