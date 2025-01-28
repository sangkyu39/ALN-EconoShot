/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react"
import axios from "axios"
import { API_BASE_URL } from "../config/api"

import NewsCard from "./NewsCard"
import "./News.css"

function News() {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const getNews = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/news/`)
        setArticles(response.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    getNews()
  }, [])

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-content">
          <div className="spinner-grow text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <h2 className="mt-3">뉴스를 불러오는 중...</h2>
          <p className="text-muted">잠시만 기다려 주세요.</p>
        </div>
      </div>
    )
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>
  }

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

