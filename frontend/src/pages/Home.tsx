import React from 'react';
import { Link } from 'react-router-dom';
import { ChartBarIcon, SearchIcon, SparklesIcon } from '@heroicons/react/solid';

const Home: React.FC = () => {
  return (
    <div className="space-y-16 pt-20">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-nfl-blue via-nfl-blue to-nfl-red text-white py-32 overflow-hidden">
        <div className="absolute inset-0 bg-nfl-pattern opacity-10"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black opacity-50"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.1)_0%,transparent_100%)]"></div>
        <div className="container mx-auto px-4 relative">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-6xl font-bold mb-8 tracking-tight">
              Advanced NFL Player Statistics & Analysis
            </h1>
            <p className="text-2xl mb-12 text-nfl-gray leading-relaxed">
              Discover comprehensive player stats, AI-powered analysis, and future performance predictions.
            </p>
            <Link
              to="/search"
              className="inline-flex items-center px-8 py-4 border-2 border-white text-lg font-medium rounded-full text-white bg-transparent hover:bg-white hover:text-nfl-blue transition-all duration-300 group"
            >
              <SearchIcon className="h-6 w-6 mr-3 group-hover:scale-110 transition-transform" />
              Search Players
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 tracking-tight">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="relative w-16 h-16 mb-6">
                <div className="absolute inset-0 bg-nfl-blue rounded-xl blur-lg opacity-20"></div>
                <ChartBarIcon className="h-16 w-16 text-nfl-blue relative" />
              </div>
              <h3 className="text-2xl font-semibold mb-4">Detailed Statistics</h3>
              <p className="text-gray-600 leading-relaxed">
                Access comprehensive player statistics, career records, and performance metrics.
              </p>
            </div>
            
            <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="relative w-16 h-16 mb-6">
                <div className="absolute inset-0 bg-nfl-blue rounded-xl blur-lg opacity-20"></div>
                <SparklesIcon className="h-16 w-16 text-nfl-blue relative" />
              </div>
              <h3 className="text-2xl font-semibold mb-4">AI Analysis</h3>
              <p className="text-gray-600 leading-relaxed">
                Get intelligent insights and performance analysis powered by advanced AI technology.
              </p>
            </div>
            
            <div className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="relative w-16 h-16 mb-6">
                <div className="absolute inset-0 bg-nfl-blue rounded-xl blur-lg opacity-20"></div>
                <SearchIcon className="h-16 w-16 text-nfl-blue relative" />
              </div>
              <h3 className="text-2xl font-semibold mb-4">Player Search</h3>
              <p className="text-gray-600 leading-relaxed">
                Find detailed information about any NFL player with our powerful search functionality.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative bg-gradient-to-r from-nfl-red to-nfl-blue text-white py-24 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.1)_0%,transparent_100%)]"></div>
        <div className="container mx-auto px-4 text-center relative">
          <h2 className="text-4xl font-bold mb-6 tracking-tight">Ready to Explore?</h2>
          <p className="text-2xl mb-12 text-nfl-gray">
            Start discovering player statistics and insights today.
          </p>
          <Link
            to="/search"
            className="inline-flex items-center px-8 py-4 border-2 border-white text-lg font-medium rounded-full text-white bg-transparent hover:bg-white hover:text-nfl-red transition-all duration-300 group"
          >
            Get Started
            <svg className="w-6 h-6 ml-3 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home; 