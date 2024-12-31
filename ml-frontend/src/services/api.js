
import axios from "axios";

export const fetchPlayerStats = (playerName) => 
  axios.get(`https://winter-break-project.onrender.com/player-stats/${playerName}`);

export const fetchFullStats = (playerName) => 
  axios.get(`https://winter-break-project.onrender.com/player/career/${playerName}`);

export const fetchPlotImage = (position, playerName) => {

  console.log(position)
  console.log(playerName)

  const baseUrl = position.toLowerCase() === "quarterback"
    ? "https://winter-break-project.onrender.com"
    : "http://127.0.0.1:8000";
  return axios.get(`https://winter-break-project.onrender.com/serve_plot/${playerName}`);
};
