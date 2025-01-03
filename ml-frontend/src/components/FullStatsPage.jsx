
import React from "react";

const FullStatsPage = ({ fullStats, onBack, onVisuals }) => (
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
    <button onClick={onBack} className="button">
      Back to Player Stats
    </button>
    <button onClick={onVisuals} className="button">
      Visuals
    </button>
      <div className="corner-gif top-left"></div>
      <div className="corner-gif top-right"></div>
      <div className="corner-gif bottom-left"></div>
      <div className="corner-gif bottom-right"></div>
      <div className="corner-gif middle-left"></div>
      <div className="corner-gif middle-right"></div>
  </div>
);

export default FullStatsPage;
