
import React, { useState } from "react";
import {
  fetchPlayerStats,
  fetchFullStats,
  fetchPlotImage,
  fetchCleanedOutput,
  fetchAnalysis,
  fetchVideo
} from "./services/api";
import SearchBar from "./components/SearchBar";
import MainStatsPage from "./components/MainStatsPage";
import FullStatsPage from "./components/FullStatsPage";
import ParticlesBackground from './components/ParticlesBackground';
import ImagesPage from "./components/ImagesPage";
import ReportCardPage from "./components/ReportCardPage"
import LoadingSpinner from "./components/LoadingSpinner";
import Video from "./components/Video";
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
  const [analysis, setAnalysis] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [showVideoPage, setShowVideoPage] = useState(false);

  const handleSearch = async () => {
    if (!playerName) {
      alert("Please enter a player's name.");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetchPlayerStats(playerName);
      setPlayerStats(response.data.players[0]);
      setGlobalPlayer(response.data.players[0]);
      setFullStats(null);
      setShowFullStatsPage(false);
    } catch (error) {
      alert(`Error fetching player stats: ${error.message}`);
    }
    finally{
      setIsLoading(false);
    }
  };

  const handleFetchCleanedOutput = async () => {

    setIsLoading(true);

    try {
      const response = await fetchCleanedOutput(playerName);
      console.log(response.data)
      setCleanedOutput(response.data); 
      setShowReportCard(true);
    } catch (error) {
      alert(`Error fetching cleaned output: ${error.message}`);
    }
    finally{
      setIsLoading(false);
    }
  };

  const handleFullStats = async () => {
    if (!playerStats) {
      alert("Please search for a player first.");
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetchFullStats(playerName);
      setFullStats(response.data.data);
      setShowFullStatsPage(true);
    } catch (error) {
      alert(`Error fetching full stats: ${error.message}`);
    }
    finally{
      setIsLoading(false);
    }
  };

  const handleFetchPlotImage = async () => {
    setIsLoading(true);
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

      const response2 = await fetchAnalysis(playerName)
      const arr = response2.data;

      setPlotImage(imageUrls);
      setAnalysis(arr);
      setShowImagesPage(true);
    } catch (error) {
      alert(`Error fetching plot images: ${error.message}`);
    }
    finally{
      setIsLoading(false);
    }
  };

  const handleFetchVideo = async () => {
    if (!playerName) {
      alert("Please search for a player first.");
      return;
    }

    setIsLoading(true)
  
    try {
      const response = await fetchVideo(playerName);
      const videoUrl = response.data;
      setVideoUrl(videoUrl);
      setShowVideoPage(true);
      
    } catch (error) {
      alert(`Error fetching video: ${error.message}`);
      throw error;
    }
    finally{
      setIsLoading(false)
    }
  };

  return (
    <div className="container">
      <ParticlesBackground />  
      {isLoading ? (
        <LoadingSpinner />
      
      ) : showVideoPage ? (
        <Video
          videoUrl={videoUrl}
          onBack={() => setShowVideoPage(false)} 
        />
      
      ) : showImagesPage ? (
        <ImagesPage
          plotImage={plotImage}
          analysis={analysis}
          onBack={() => setShowImagesPage(false)}
        />
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
  
          {playerStats && (
            <MainStatsPage
              playerStats={playerStats}
              onFullStats={handleFullStats}
              onFetchCleanedOutput={handleFetchCleanedOutput}
              OnVideo= {handleFetchVideo} 
            />
          )}
        </>
      )}
    </div>
  );
};

export default App;
