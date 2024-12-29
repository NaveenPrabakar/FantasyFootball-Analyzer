import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [playerName, setPlayerName] = useState("");
  const [playerStats, setPlayerStats] = useState(null);
  const [fullStats, setFullStats] = useState(null);
  const [showFullStatsPage, setShowFullStatsPage] = useState(false); // Manage the full stats page view
  const [plotImage, setPlotImage] = useState([]);
  const [globalPlayer, setGlobalPlayer] = useState(null);
  const [showImagesPage, setShowImagesPage] = useState(false);


  const fetchPlotImage = async () => {

   
    if(globalPlayer.strPosition?.toLowerCase() === "quarterback"){
      try {
        
        const response = await axios.get(`https://winter-break-project.onrender.com/serve_plot/${playerName}`);
        
        const filePaths = response.data.data;
      
        
        const imageUrls = await Promise.all(
          filePaths.map(async (filePath) => {
            const imageResponse = await axios.get(filePath, { responseType: 'blob' });
            return URL.createObjectURL(imageResponse.data);
          })
        );
      
        
        setPlotImage(imageUrls);
        setShowFullStatsPage(false);
        setPlayerStats(null);
        setShowImagesPage(true); 
      
      } catch (error) {
        console.error("Error fetching plot images:", error);
        setPlotImage(null); 
      }
      
    }
    else if(globalPlayer.strPosition?.toLowerCase() === "rb"){

      try {
        
        const response = await axios.get(`http://127.0.0.1:8000/serve_plot/${playerName}`);
        
        const filePaths = response.data.data;
      
        
        const imageUrls = await Promise.all(
          filePaths.map(async (filePath) => {
            const imageResponse = await axios.get(filePath, { responseType: 'blob' });
            return URL.createObjectURL(imageResponse.data);
          })
        );
      
        
        setPlotImage(imageUrls);
      
      } catch (error) {
        console.error("Error fetching plot images:", error);
        setPlotImage(null); 
      }
      //Implement Later
    }
    else if(globalPlayer.strPosition?.toLowerCase() ==="wr"){

      try {
        
        const response = await axios.get(`http://127.0.0.1:8000/serve_plot/${playerName}`);
        
        const filePaths = response.data.data;
      
        
        const imageUrls = await Promise.all(
          filePaths.map(async (filePath) => {
            const imageResponse = await axios.get(filePath, { responseType: 'blob' });
            return URL.createObjectURL(imageResponse.data);
          })
        );
      
        
        setPlotImage(imageUrls);
      
      } catch (error) {
        console.error("Error fetching plot images:", error);
        setPlotImage(null); 
      }

      //Implement Later
    }
    else if(globalPlayer.strPosition?.toLowerCase() ==="te"){

      try {
        
        const response = await axios.get(`http://127.0.0.1:8000/serve_plot/${playerName}`);
        
        const filePaths = response.data.data;
      
        
        const imageUrls = await Promise.all(
          filePaths.map(async (filePath) => {
            const imageResponse = await axios.get(filePath, { responseType: 'blob' });
            return URL.createObjectURL(imageResponse.data);
          })
        );
      
        
        setPlotImage(imageUrls);
      
      } catch (error) {
        console.error("Error fetching plot images:", error);
        setPlotImage(null); 
      }
      //Implement Later
    }
    else{
      console.error("Invalid position: ", globalPlayer.strPosition)
    }
    
  };


  const handleSearch = async () => {
    if (!playerName) {
      alert("Please enter a player's name.");
      return;
    }

    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/player-stats/${playerName}`
      );
      setPlayerStats(res.data.players[0]);
      setGlobalPlayer(res.data.players[0]);
      setFullStats(null);
      setShowFullStatsPage(false); // Reset view when searching for a new player
      
    } catch (error) {
      alert(
        "Error fetching player stats: " +
          (error.response?.data?.detail || error.message)
      );
      setPlayerStats(null);
    }
  };

  const handleFullStats = async () => {
    if (!playerStats) {
      alert("Please search for a player first.");
      return;
    }

    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/player/career/${playerName}`
      );

      const statsList = res.data.data;

      // Filter only important QB stats
      const filteredStats = statsList.map((stat) => ({
        Season: stat.Season,
        Team: stat.Team,
        G: stat.G,
        Cmp: stat.Cmp,
        Att: stat.Att,
        Yds: stat.Yds,
        TD: stat.TD,
        Int: stat.Int,
        Rate: stat.Rate,
      }));

      setFullStats(Array.isArray(filteredStats) ? filteredStats : []); 
      setShowFullStatsPage(true); 
    } catch (error) {
      alert(
        "Error fetching full stats: " +
          (error.response?.data?.detail || error.message)
      );
      setFullStats(null);
    }
  };

  return (
    <div className="container">
      {showImagesPage && ( // Show only when showImagesPage is true
        <div className="imagesPage">
          {/* Added image gallery block */}
          <h3>Player Stats Visualizations</h3>
          <div className="imageGallery">
            {plotImage.length > 0 ? (
              plotImage.map((url, index) => (
                <img
                  key={index}
                  src={url}
                  alt={`Player Stats Plot ${index + 1}`}
                  className="plotImage"
                />
              ))
            ) : (
              <p>No images available.</p>
            )}
          </div>
          <button onClick={() => setShowImagesPage(false)} className="button">
            Back to Stats
          </button>
        </div>
      )}

      {!showImagesPage && showFullStatsPage && (
        <div className="fullStatsBox">
          <h3>Full Career Stats</h3>
          <table className="statsTable">
            <thead>
              <tr>
                {Object.keys(fullStats[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {fullStats.map((stat, index) => (
                <tr key={index}>
                  {Object.values(stat).map((value, i) => (
                    <td key={i}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <button
            onClick={() => setShowFullStatsPage(false)}
            className="button"
          >
            Back to Player Stats
          </button>
          <button onClick={fetchPlotImage} className="button">
            Visuals
          </button>
        </div>
      )}

      {!showImagesPage && !showFullStatsPage && (
        // Main player stats page remains intact
        <>
          <h1 className="header">🏈 NFL Player Stats 🏈</h1>
          <div className="searchBar">
            <input
              type="text"
              placeholder="Enter player name"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              className="input"
            />
            <button onClick={handleSearch} className="button">
              Search
            </button>
          </div>

          {playerStats && (
            <div className="statsBox animateStats">
              <h3>Player Stats</h3>
              <div style={{ textAlign: "center" }}>
                <h2>{playerStats.strPlayer}</h2>
              </div>
              <table className="table">
                <thead>
                  <tr>
                    <th>Team</th>
                    <th>Position</th>
                    <th>Date of Birth</th>
                    <th>Nationality</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{playerStats.strTeam || "N/A"}</td>
                    <td>{playerStats.strPosition || "N/A"}</td>
                    <td>{playerStats.dateBorn || "N/A"}</td>
                    <td>{playerStats.strNationality || "N/A"}</td>
                    <td>
                      {playerStats.strDescriptionEN ||
                        "No description available"}
                    </td>
                  </tr>
                </tbody>
              </table>
              <button onClick={handleFullStats} className="button">
                Full Stats
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;