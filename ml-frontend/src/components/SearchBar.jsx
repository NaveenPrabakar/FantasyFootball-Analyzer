import React from "react";

const SearchBar = ({ playerName, setPlayerName, onSearch }) => (
  <div>
    <div className="searchBar">
      <input
        type="text"
        placeholder="Enter player name"
        value={playerName}
        onChange={(e) => setPlayerName(e.target.value)}
        className="input"
      />
      <button onClick={onSearch} className="button">
        Search
      </button>
    </div>

    <div className="animationContainer">
      <div className="player player-left">
        <div className="helmet"></div>
        <div className="shoulderPads"></div>
        <div className="body"></div>
        <div className="arm left"></div>
        <div className="arm right"></div>
        <div className="leg left"></div>
        <div className="leg right"></div>
      </div>
      <div className="football-animation"></div>
      <div className="player player-right">
        <div className="helmet"></div>
        <div className="shoulderPads"></div>
        <div className="body"></div>
        <div className="arm left"></div>
        <div className="arm right"></div>
        <div className="leg left"></div>
        <div className="leg right"></div>
      </div>
    </div>
  </div>
);

export default SearchBar;



