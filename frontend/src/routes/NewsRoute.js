/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config/api";
import { ThumbsUp, ThumbsDown, Building2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import News from "../components/News";

function NewsRoute() {

	return (
    <div className="container mx-auto p-4">
      <News />
    </div>
  );
}

export default NewsRoute;