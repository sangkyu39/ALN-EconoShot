/* eslint-disable react/jsx-pascal-case */
/* eslint-disable no-unused-vars */
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NewsRoute from "./routes/NewsRoute.js";

function Routing() {
	return (
		<div className="container">
			<Router>
				<Routes>
					<Route path="*" element={<NewsRoute />} />
				</Routes>
			</Router>
		</div>
	);
}

export default Routing;
