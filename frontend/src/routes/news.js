/* eslint-disable react/jsx-pascal-case */
/* eslint-disable no-unused-vars */
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import axios from "axios";
import { API_BASE_URL } from "../config/api";

function News() {
	const getNews = () => {
		axios
			.get(`${API_BASE_URL}/news/`)
			.then((res) => {
				console.log(res);
			})
			.catch((err) => {
				console.log(err);
			});
	};
	getNews();
	return (
		<div className="container">
			<p>123</p>
		</div>
	);
}

export default News;
