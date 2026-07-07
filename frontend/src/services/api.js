import axios from "axios";

// Backend URL
const API = axios.create({
  baseURL: "https://rag-ai-bot-bxcugefscserf4cx.centralindia-01.azurewebsites.net",
});

export default API;