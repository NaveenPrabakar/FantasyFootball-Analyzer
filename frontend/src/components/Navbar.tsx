import React from 'react';
import { Link } from 'react-router-dom';
import { SearchIcon, HomeIcon, ChartBarIcon } from '@heroicons/react/solid';
import nflLogo from '../assets/nfl-logo.svg';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-gradient-to-r from-nfl-blue via-nfl-blue to-nfl-red shadow-lg backdrop-blur-sm bg-opacity-90 fixed w-full z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-20">
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="relative">
              <div className="absolute inset-0 bg-white rounded-full blur-sm opacity-30 group-hover:opacity-50 transition-opacity"></div>
              <img src={nflLogo} alt="NFL Logo" className="h-10 w-10 relative" />
            </div>
            <span className="text-white text-2xl font-bold tracking-wider">NFL STATS</span>
          </Link>
          
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-white hover:text-nfl-red flex items-center space-x-2 group">
              <div className="relative">
                <div className="absolute inset-0 bg-white rounded-full blur-sm opacity-0 group-hover:opacity-20 transition-opacity"></div>
                <HomeIcon className="h-6 w-6 relative" />
              </div>
              <span className="font-medium tracking-wide">Home</span>
            </Link>
            <Link to="/search" className="text-white hover:text-nfl-red flex items-center space-x-2 group">
              <div className="relative">
                <div className="absolute inset-0 bg-white rounded-full blur-sm opacity-0 group-hover:opacity-20 transition-opacity"></div>
                <SearchIcon className="h-6 w-6 relative" />
              </div>
              <span className="font-medium tracking-wide">Search Players</span>
            </Link>
            <Link to="/stats" className="text-white hover:text-nfl-red flex items-center space-x-2 group">
              <div className="relative">
                <div className="absolute inset-0 bg-white rounded-full blur-sm opacity-0 group-hover:opacity-20 transition-opacity"></div>
                <ChartBarIcon className="h-6 w-6 relative" />
              </div>
              <span className="font-medium tracking-wide">Statistics</span>
            </Link>
          </div>

          <div className="md:hidden">
            <button className="text-white hover:text-nfl-red transition-colors">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 