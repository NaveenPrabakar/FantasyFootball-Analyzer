import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import PlayerSearch from './pages/PlayerSearch';
import PlayerStats from './pages/PlayerStats';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-nfl-light">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<PlayerSearch />} />
            <Route path="/player/:name" element={<PlayerStats />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App; 