
import React, { useState } from "react";
import {
  fetchPlayerStats,
  fetchFullStats,
  fetchPlotImage,
  fetchCleanedOutput
} from "./services/api";
import SearchBar from "./components/SearchBar";
import MainStatsPage from "./components/MainStatsPage";
import FullStatsPage from "./components/FullStatsPage";
import ImagesPage from "./components/ImagesPage";
import ReportCardPage from "./components/ReportCardPage"
import "./App.css";
import axios from "axios";

function App() {
  const [playerName, setPlayerName] = useState("");
  const [playerStats, setPlayerStats] = useState(null);
  const [fullStats, setFullStats] = useState(null);
  const [showFullStatsPage, setShowFullStatsPage] = useState(false);
  const [plotImage, setPlotImage] = useState([]);
  const [globalPlayer, setGlobalPlayer] = useState(null);
  const [showImagesPage, setShowImagesPage] = useState(false);
  const [cleanedOutput, setCleanedOutput] = useState([]); 
  const [showReportCard, setShowReportCard] = useState(false);

  const handleSearch = async () => {
    if (!playerName) {
      alert("Please enter a player's name.");
      return;
    }
    try {
      const response = await fetchPlayerStats(playerName);
      setPlayerStats(response.data.players[0]);
      setGlobalPlayer(response.data.players[0]);
      setFullStats(null);
      setShowFullStatsPage(false);
    } catch (error) {
      alert(`Error fetching player stats: ${error.message}`);
    }
  };

  const handleFetchCleanedOutput = async () => {
    try {
      const response = await fetchCleanedOutput(playerName);
      console.log(response.data)
      setCleanedOutput(response.data); 
      setShowReportCard(true);
    } catch (error) {
      alert(`Error fetching cleaned output: ${error.message}`);
    }
  };

  const handleFullStats = async () => {
    if (!playerStats) {
      alert("Please search for a player first.");
      return;
    }
    try {
      const response = await fetchFullStats(playerName);
      setFullStats(response.data.data);
      setShowFullStatsPage(true);
    } catch (error) {
      alert(`Error fetching full stats: ${error.message}`);
    }
  };

  const handleFetchPlotImage = async () => {
    try {
      const response = await fetchPlotImage(globalPlayer.strPosition, playerName);
      console.log(response.data.data)

      const filePaths = response.data.data;

      const imageUrls = await Promise.all(
        filePaths.map(async (filePath) => {
          const imageResponse = await axios.get(filePath, { responseType: 'blob' });
          return URL.createObjectURL(imageResponse.data);
        })
      );

      setPlotImage(imageUrls);
      setShowImagesPage(true);
    } catch (error) {
      alert(`Error fetching plot images: ${error.message}`);
    }
  };

  return (
    <div className="container">
      {showImagesPage ? (
        <ImagesPage plotImage={plotImage} onBack={() => setShowImagesPage(false)} />
      ) : showFullStatsPage ? (
        <FullStatsPage
          fullStats={fullStats}
          onBack={() => setShowFullStatsPage(false)}
          onVisuals={handleFetchPlotImage}
        />
      ) : showReportCard ? (
        <ReportCardPage
          cleanedOutput={cleanedOutput}
          onBack={() => setShowReportCard(false)}
        />
      ) : (
        <>
          <h1 className="header">🏈 NFL Player Stats 🏈</h1>
          <SearchBar
            playerName={playerName}
            setPlayerName={setPlayerName}
            onSearch={handleSearch}
          />
          <button className="report-button" onClick={handleFetchCleanedOutput}>
            Show Report Card
          </button>

          {playerStats && (
            <MainStatsPage playerStats={playerStats} onFullStats={handleFullStats} />
          )}
        </>
      )}
    </div>
  );
}

export default App;
