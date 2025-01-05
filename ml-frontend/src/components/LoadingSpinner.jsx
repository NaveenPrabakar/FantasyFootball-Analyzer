import React from "react";
import "./LoadingSpinner.css";

const LoadingSpinner = () => {
  return (
    <div className="spinnerContainer">
      <div className="loadingSpinner"></div>
      <p>Loading...</p>
    </div>
  );
};

export default LoadingSpinner;