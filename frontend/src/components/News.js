/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config/api";
import NewsCard from "./NewsCard";
import "./News.css";
import { useNavigate } from "react-router-dom";

export default function News() {
	const [articles, setArticles] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);
	let navigate = useNavigate();

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
		return (
			<div className="loading-container">
				<div className="loading-content">
					<div className="spinner"></div>
					<h2 className="text">Loading...</h2>
					<p className="text">Please wait a moment</p>
				</div>
			</div>
		);
	}

	if (error) {
		return (
			<div className="error-container">
				<div className="error-content">
					<h2>Error: {error}</h2>
				</div>
			</div>
		);
	}

	return (
		<div className="news-container">
			<h1
				onClick={() => {
					navigate("/");
				}}
				className="news-title">
				Economy News
			</h1>
			<div className="news-grid">
				{articles.map((news, index) => (
					<NewsCard key={index} news={news} />
				))}
			</div>
		</div>
	);
}
