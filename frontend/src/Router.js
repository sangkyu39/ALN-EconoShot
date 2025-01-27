/* eslint-disable react/jsx-pascal-case */
/* eslint-disable no-unused-vars */
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import News from "./routes/news.js";

function Routing() {
	return (
		<div className="container">
			<p>123</p>
			<News />
		</div>
	);
}

export default Routing;
