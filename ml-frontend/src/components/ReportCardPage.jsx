import React from "react";
import "./ReportCardPage.css"; 

const ReportCardPage = ({ cleanedOutput, onBack }) => {
    return (
      <div className="report-card">
        <h2>Player Report Card</h2>
        {cleanedOutput && cleanedOutput.length > 0 ? (
          <ul>
            {cleanedOutput.map((item, index) => (
              <li key={index}>{item}</li>  
            ))}
          </ul>
        ) : (
          <p>No data available for the report card.</p>
        )}
        <button onClick={onBack}>Back</button>
      </div>
    );
  };

export default ReportCardPage;
