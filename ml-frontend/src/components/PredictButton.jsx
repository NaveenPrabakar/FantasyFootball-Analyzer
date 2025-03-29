import React from 'react';

const PredictButton = ({ onPredict }) => {
  return (
    <button className="predict-btn" onClick={onPredict}>
      Predict Stats
    </button>
  );
};
