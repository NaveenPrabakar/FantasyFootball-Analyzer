import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const BACKEND_URL = "https://winter-break-project.onrender.com";

interface CareerStats {
  Season: string;
  Age: number;
  Team: string;
  Pos: string;
  G: number;
  [key: string]: any;
}

interface NextSeasonData {
  [key: string]: string | number | null;
}

interface Predictions {
  message: string;
  next_season_data: NextSeasonData;
}

const PlayerStats: React.FC = () => {
  const { name } = useParams<{ name: string }>();
  const [playerInfo, setPlayerInfo] = useState<any>(null);
  const [careerStats, setCareerStats] = useState<CareerStats[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedStat, setSelectedStat] = useState('Yds');
  const [plots, setPlots] = useState<string[]>([]);
  const [analysis, setAnalysis] = useState<string[]>([]);
  const [aiAnalysis, setAiAnalysis] = useState<string[]>([]);
  const [highlights, setHighlights] = useState<string>('');
  const [predictions, setPredictions] = useState<Predictions | null>(null);

  useEffect(() => {
    const fetchPlayerData = async () => {
      try {
        const [
          infoResponse,
          statsResponse,
          plotsResponse,
          analysisResponse,
          highlightsResponse
        ] = await Promise.all([
          axios.get(`${BACKEND_URL}/player-stats/${name}`),
          axios.get(`${BACKEND_URL}/player/career/${name}`),
          axios.get(`${BACKEND_URL}/serve_plot/${name}`),
          axios.get(`${BACKEND_URL}/analyze/${name}`),
          axios.get(`${BACKEND_URL}/search/${name}`),
          )
        ]);

        if (infoResponse.data.players && infoResponse.data.players.length > 0) {
          setPlayerInfo(infoResponse.data.players[0]);
        }
        
        if (statsResponse.data.data) {
          setCareerStats(statsResponse.data.data);
        }

        if (plotsResponse.data.data) {
          setPlots(plotsResponse.data.data);
        }

        if (analysisResponse.data) {
          setAnalysis(analysisResponse.data);
        }

        if (highlightsResponse.data) {
          setHighlights(highlightsResponse.data);
        }

      } catch (err) {
        setError('Error fetching player data. Please try again.');
        console.error('Error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayerData();
  }, [name]);

  const chartData = {
    labels: careerStats.map(stat => stat.Season),
    datasets: [
      {
        label: selectedStat,
        data: careerStats.map(stat => stat[selectedStat]),
        borderColor: 'rgb(1, 51, 105)',
        backgroundColor: 'rgba(1, 51, 105, 0.5)',
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: `${selectedStat} Over Time`,
      },
    },
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-nfl-blue"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Player Header */}
      {playerInfo && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center space-x-4">
            <div className="flex-1">
              <h1 className="text-3xl font-bold mb-2">{playerInfo.strPlayer}</h1>
              <p className="text-gray-600">
                {playerInfo.strTeam} • {playerInfo.strPosition}
              </p>
            </div>
            <div className="text-right">
              <span className="inline-block px-4 py-2 bg-nfl-blue text-white rounded-full">
                {playerInfo.strPosition}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Player Plots */}
      {plots.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">Performance Plots</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {plots.map((plot, index) => (
              <img
                key={index}
                src={plot}
                alt={`Performance Plot ${index + 1}`}
                className="w-full h-auto rounded-lg"
              />
            ))}
          </div>
        </div>
      )}

      {/* Stats Chart */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Career Statistics</h2>
          <select
            value={selectedStat}
            onChange={(e) => setSelectedStat(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-nfl-blue focus:border-transparent"
          >
            <option value="Yds">Yards</option>
            <option value="TD">Touchdowns</option>
            <option value="G">Games</option>
            <option value="Cmp%">Completion %</option>
            <option value="Y/A">Yards/Attempt</option>
          </select>
        </div>
        <div className="h-96">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      {/* AI Analysis */}
      {analysis.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">AI Analysis</h2>
          <div className="space-y-4">
            {analysis.map((item, index) => (
              <p key={index} className="text-gray-700">{item}</p>
            ))}
          </div>
        </div>
      )}

      {/* Player Highlights */}
      {highlights && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">Player Highlights</h2>
          <div className="aspect-w-16 aspect-h-9">
            <iframe
              src={`https://www.youtube.com/embed/${highlights}`}
              title="Player Highlights"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="w-full h-full rounded-lg"
            />
          </div>
        </div>
      )}

      {/* Predictions */}
    
      {/* Career Stats Table */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4">Detailed Career Stats</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Season
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Team
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Games
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Yards
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Touchdowns
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {careerStats.map((stat, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {stat.Season}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {stat.Team}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {stat.G}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {stat.Yds}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {stat.TD}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default PlayerStats; 
