
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
  </div>
);

export default FullStatsPage;
