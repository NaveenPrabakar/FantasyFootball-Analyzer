import React from "react";

const MainStatsPage = ({ playerStats, onFullStats, onFetchCleanedOutput, OnVideo }) => (
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
          <td>{playerStats.strDescriptionEN || "No description available"}</td>
        </tr>
      </tbody>
    </table>

    
    <div className="button-container">
      <button onClick={onFullStats} className="button">
        Full Stats
      </button>
      <button onClick={onFetchCleanedOutput} className="button">
        AI Analysis
      </button>
      <button onClick={OnVideo} className="button">
        Film
      </button>
    </div>
  </div>
);

export default MainStatsPage;

