import axios from "axios";

// API to fetch the player stats
export const fetchPlayerStats = async (playerName) => {
  try {
    const response = await axios.get(`https://winter-break-project.onrender.com/player-stats/${playerName}`);
    return response;
  } catch (error) {
    console.error(`Error fetching player stats for ${playerName}: ${error.message}`);
    throw new Error(`Error fetching player stats: ${error.message}`);
  }
};

// API to fetch the full stats
export const fetchFullStats = async (playerName) => {
  try {
    const response = await axios.get(`https://winter-break-project.onrender.com/player/career/${playerName}`);
    return response;
  } catch (error) {
    console.error(`Error fetching full stats for ${playerName}: ${error.message}`);
    throw new Error(`Error fetching full stats: ${error.message}`);
  }
};

// API to fetch the graphs
export const fetchPlotImage = async (position, playerName) => {
  const baseUrl = position.toLowerCase() === "quarterback"
    ? "https://winter-break-project.onrender.com"
    : "http://127.0.0.1:8000";
  try {
    const response = await axios.get(`https://winter-break-project.onrender.com/serve_plot/${playerName}`);
    return response;
  } catch (error) {
    console.error(`Error fetching plot images for ${playerName}: ${error.message}`);
    throw new Error(`Error fetching plot images: ${error.message}`);
  }
};

// API to fetch the report of seasons
export const fetchCleanedOutput = async (playerName) => {
  try {
    const response = await axios.get(`https://winter-break-project.onrender.com/AI/${playerName}`);
    console.log(response);
    return response;
  } catch (error) {
    console.error(`Error fetching cleaned output for ${playerName}: ${error.message}`);
    throw new Error(`Error fetching cleaned output: ${error.message}`);
  }
};

// API to fetch image analysis
export const fetchAnalysis = async (playerName) => {
  try {
    const response = await axios.get(`https://winter-break-project.onrender.com/analyze/${playerName}`);
    return response;
  } catch (error) {
    console.error(`Error fetching analysis for ${playerName}: ${error.message}`);
    throw new Error(`Error fetching analysis: ${error.message}`);
  }
};

//API to fetch video link
export const fetchVideo = async (playerName) => {
  try {
    const response = await axios.get(`https://winter-break-project.onrender.com/search/${playerName}`);
    return response;
  } catch (error) {
    console.error(`Error fetching video for ${playerName}: ${error.message}`);
    throw new Error(`Error fetching video: ${error.message}`);
  }
};


