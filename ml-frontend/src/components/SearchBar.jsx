
import React from "react";

const SearchBar = ({ playerName, setPlayerName, onSearch }) => (
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
);

export default SearchBar;
