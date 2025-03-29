import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchIcon } from '@heroicons/react/solid';
import axios from 'axios';

interface Player {
  idPlayer: string;
  strPlayer: string;
  strTeam: string;
  strPosition: string;
  dateBorn: string;
  strNationality: string;
  strDescriptionEN: string;
}

const PlayerSearch: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`http://localhost:8000/player-stats/${searchQuery}`);
      const data = response.data;
      
      if (data.players && data.players.length > 0) {
        setPlayers(data.players);
      } else {
        setError('No players found with that name.');
        setPlayers([]);
      }
    } catch (err) {
      setError('Error fetching player data. Please try again.');
      setPlayers([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayerClick = (playerName: string) => {
    navigate(`/player/${encodeURIComponent(playerName)}`);
  };

  return (
    <div className="max-w-4xl mx-auto pt-20 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4 tracking-tight">Search NFL Players</h1>
        <p className="text-xl text-gray-600">Find detailed statistics and analysis for any NFL player</p>
      </div>
      
      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-12">
        <div className="flex gap-4">
          <div className="flex-1 relative group">
            <div className="absolute inset-0 bg-nfl-blue rounded-xl blur-lg opacity-20 group-hover:opacity-30 transition-opacity"></div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter player name..."
              className="w-full px-6 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-nfl-blue focus:border-transparent bg-white/80 backdrop-blur-sm text-lg transition-all duration-300"
            />
            <SearchIcon className="h-6 w-6 text-gray-400 absolute right-4 top-1/2 transform -translate-y-1/2 group-hover:text-nfl-blue transition-colors" />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-4 bg-gradient-to-r from-nfl-blue to-nfl-red text-white rounded-xl hover:shadow-lg hover:shadow-nfl-blue/20 transition-all duration-300 disabled:opacity-50 font-medium text-lg"
          >
            {loading ? (
              <div className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Searching...
              </div>
            ) : 'Search'}
          </button>
        </div>
      </form>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg mb-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {players.length > 0 && (
        <div className="space-y-6">
          {players.map((player) => (
            <div
              key={player.idPlayer}
              onClick={() => handlePlayerClick(player.strPlayer)}
              className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 cursor-pointer group"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-2xl font-semibold mb-3 group-hover:text-nfl-blue transition-colors">{player.strPlayer}</h2>
                  <p className="text-gray-600 mb-2 text-lg">{player.strTeam} • {player.strPosition}</p>
                  <p className="text-sm text-gray-500">
                    Born: {new Date(player.dateBorn).toLocaleDateString()}
                  </p>
                </div>
                <div className="text-right">
                  <span className="inline-block px-4 py-2 bg-gradient-to-r from-nfl-blue to-nfl-red text-white rounded-full text-sm font-medium">
                    {player.strPosition}
                  </span>
                </div>
              </div>
              {player.strDescriptionEN && (
                <p className="mt-6 text-gray-700 line-clamp-2 text-lg leading-relaxed">
                  {player.strDescriptionEN}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PlayerSearch; 