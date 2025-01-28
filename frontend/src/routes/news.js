import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config/api";

function News() {
	const [articles, setArticles] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

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

		getNews();
	}, []);

	if (loading) {
		return <div>Loading...</div>;
	}

	if (error) {
		return <div>Error: {error}</div>;
	}

	return (
		<div className="container">
			{articles.map((article, index) => (
				<div key={index} className="news-article">
					<h2>{article.title}</h2>
					<p>{article.summary}</p>
					<p>Sentiment: {article.sentiment}</p>
					{article.companies.length > 0 && <p>Companies: {article.companies.join(", ")}</p>}
					<a href={article.link} target="_blank" rel="noopener noreferrer">
						Read more
					</a>
				</div>
			))}
		</div>
	);
}

export default News;
