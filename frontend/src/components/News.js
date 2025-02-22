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
  const [searchQuery, setSearchQuery] = useState("");
  let navigate = useNavigate();

  // 초기 뉴스 데이터 불러오기
  useEffect(() => {
    const getNews = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/news/get-stored`);
        setArticles(response.data);
        console.log("초기 데이터:", response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    getNews();
  }, []);

  // 검색 기능: GET 요청으로 뉴스 데이터 불러오기
  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${API_BASE_URL}/news/fetch-latest?query=${encodeURIComponent(searchQuery)}`
      );
      // 기존 articles와 새 응답 데이터를 합친 배열 생성
      setArticles((prevArticles) => {
        console.log("이전 articles:", prevArticles);
        const combinedArticles = [...prevArticles, ...response.data];
        console.log("합쳐진 articles:", combinedArticles);
        return combinedArticles;
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

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
      <div className="news-header">
        <h1
          onClick={() => {
            navigate("/");
          }}
          className="news-title"
        >
          Economy News
        </h1>
        {/* 검색 창 추가 */}
        <div className="search-container">
          <input
            type="text"
            placeholder="Search news..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button onClick={handleSearch}>Search</button>
        </div>
      </div>
      <div className="news-grid">
        {articles.map((news, index) => (
          // 만약 news에 고유 id가 있다면 key={news.id}를 사용하세요.
          <NewsCard key={news.id || index} news={news} />
        ))}
      </div>
    </div>
  );
}
