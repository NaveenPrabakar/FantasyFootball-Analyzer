import React from "react";

const VideoComponent = ({ videoUrl }) => {
 
  const embedUrl = videoUrl ? `https://www.youtube.com/embed/${videoUrl}` : '';

  return (
    <div className="video-container">
      <h3>Player Video Highlights</h3>
      {embedUrl ? (
        <iframe
          width="560"
          height="315"
          src={embedUrl}
          title="Player Highlights"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      ) : (
        <p>No video available for this player.</p>
      )}
    </div>
  );
};

export default VideoComponent;

