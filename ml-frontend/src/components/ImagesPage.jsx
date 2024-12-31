
import React from "react";

const ImagesPage = ({ plotImage, onBack }) => (
  <div className="imagesPage">
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
    <button onClick={onBack} className="button">
      Back to Stats
    </button>
  </div>
);

export default ImagesPage;
