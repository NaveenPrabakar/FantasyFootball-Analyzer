import React, { useState } from "react";
import axios from "axios";

function App() {
  const [playerName, setPlayerName] = useState("");
  const [playerStats, setPlayerStats] = useState(null);
  const [fullStats, setFullStats] = useState(null);

  const handleSearch = async () => {
    if (!playerName) {
      alert("Please enter a player's name.");
      return;
    }

    try {
      const res = await axios.get(`http://127.0.0.1:8000/player-stats/${playerName}`);
      console.log("This is the array", res.data.players[0]);
      setPlayerStats(res.data.players[0]);
      setFullStats(null);
    } catch (error) {
      alert("Error fetching player stats: " + (error.response?.data?.detail || error.message));
      setPlayerStats(null);
    }
  };

  const handleFullStats = async () => {
    if (!playerStats) {
      alert("Please search for a player first.");
      return;
    }

    try {
      const res = await axios.get(`http://127.0.0.1:8000/full-stats/${playerStats.idPlayer}`);
      setFullStats(res.data);
    } catch (error) {
      alert("Error fetching full stats: " + (error.response?.data?.detail || error.message));
    }
  };

  const styles = {
    container: {
      fontFamily: "Verdana, sans-serif",
      width: "100vw",
      height: "100vh",
      margin: "0",
      padding: "20px",
      backgroundColor: "#003B1F",
      color: "#FFFFFF",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
    },
    header: {
      textAlign: "center",
      fontSize: "2.5em",
      fontWeight: "bold",
      marginBottom: "20px",
      borderBottom: "3px solid #FFB612",
    },
    searchBar: {
      width: "80%",
      marginBottom: "20px",
    },
    input: {
      width: "100%",
      padding: "10px",
      marginBottom: "10px",
      border: "2px solid #FFB612",
      borderRadius: "4px",
      backgroundColor: "#FFFFFF",
      color: "#003B1F",
    },
    button: {
      backgroundColor: "#FFB612",
      color: "#003B1F",
      border: "none",
      padding: "12px 24px",
      margin: "10px",
      borderRadius: "6px",
      cursor: "pointer",
      fontWeight: "bold",
    },
    statsBox: {
      width: "80%",
      marginTop: "20px",
      padding: "10px",
      border: "2px solid #FFFFFF",
      borderRadius: "6px",
      backgroundColor: "#145A32",
      color: "#FFFFFF",
    },
    table: {
      width: "100%",
      marginTop: "20px",
      borderCollapse: "collapse",
      textAlign: "left",
    },
    th: {
      padding: "10px",
      backgroundColor: "#FFB612",
    },
    td: {
      padding: "10px",
      borderBottom: "1px solid #ddd",
    },
    img: {
      width: "150px",
      borderRadius: "50%",
      marginBottom: "15px",
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>🏈 NFL Player Stats 🏈</h1>
      <div style={styles.searchBar}>
        <input
          type="text"
          placeholder="Enter player name"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleSearch} style={styles.button}>
          Search
        </button>
      </div>

      {playerStats && (
        <div style={styles.statsBox}>
          <h3>Player Stats</h3>
          <div style={{ textAlign: "center" }}>
            <h2>{playerStats.strPlayer}</h2>
          </div>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Team</th>
                <th style={styles.th}>Position</th>
                <th style={styles.th}>Date of Birth</th>
                <th style={styles.th}>Nationality</th>
                <th style={styles.th}>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={styles.td}>{playerStats.strTeam || "N/A"}</td>
                <td style={styles.td}>{playerStats.strPosition || "N/A"}</td>
                <td style={styles.td}>{playerStats.dateBorn || "N/A"}</td>
                <td style={styles.td}>{playerStats.strNationality || "N/A"}</td>
                <td style={styles.td}>{playerStats.strDescriptionEN || "No description available"}</td>
              </tr>
            </tbody>
          </table>
          <button onClick={handleFullStats} style={styles.button}>
            Full Stats
          </button>
        </div>
      )}

      {fullStats && (
        <div style={styles.statsBox}>
          <h3>Full Stats</h3>
          <pre>{JSON.stringify(fullStats, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
