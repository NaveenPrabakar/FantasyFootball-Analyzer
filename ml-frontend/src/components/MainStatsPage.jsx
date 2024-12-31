
import React from "react";

const MainStatsPage = ({ playerStats, onFullStats }) => (
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
    <button onClick={onFullStats} className="button">
      Full Stats
    </button>
  </div>
);

export default MainStatsPage;
