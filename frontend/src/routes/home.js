/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config/api";
import { useNavigate } from "react-router-dom";
function Home() {
	let navigate = useNavigate();

	return (
		<div className="container mx-auto p-4">
			<p>HELLO</p>
			<div onClick={()=>{navigate("/news")}}>뉴스 보러가기</div>
		</div>
	);
}

export default Home;
