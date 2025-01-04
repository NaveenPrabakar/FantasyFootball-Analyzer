import React from "react";
import "./ImagesPage.css"; 

const ImagesPage = ({ plotImage, analysis, onBack }) => (
  <div className="imagesPage">
    <h3>Player Stats Visualizations</h3>
    <div className="imageAnalysisContainer">
      {plotImage.length > 0 ? (
        plotImage.map((url, index) => (
          <div key={index} className="imageAnalysisBox">
            <div className="imageContainer">
              <img
                src={url}
                alt={`Player Stats Plot ${index + 1}`}
                className="plotImage"
              />
            </div>
            <div className="analysisContainer">
              {analysis[index] && <p>{analysis[index]}</p>}
            </div>
          </div>
        ))
      ) : (
        <p>No images available.</p>
      )}
    </div>
    <button onClick={onBack} className="button">
      Back to Stats
    </button>
  </div>
);

export default ImagesPage;



