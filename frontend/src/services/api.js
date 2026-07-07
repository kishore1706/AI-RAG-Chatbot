import axios from "axios";

// Backend URL
const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export default API;