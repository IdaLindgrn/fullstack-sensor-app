import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import SensorList from './components/SensorList';
import SensorDetail from './components/SensorDetail';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <Router>
      <div className="App">
        {token && (
          <nav className="navbar">
            <h1>Sensor Dashboard</h1>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </nav>
        )}
        <Routes>
          <Route path="/login" element={
            token ? <Navigate to="/sensors" /> : <Login onLogin={handleLogin} />
          } />
          <Route path="/register" element={
            token ? <Navigate to="/sensors" /> : <Register onLogin={handleLogin} />
          } />
          <Route path="/sensors" element={
            token ? <SensorList token={token} /> : <Navigate to="/login" />
          } />
          <Route path="/sensors/:id" element={
            token ? <SensorDetail token={token} /> : <Navigate to="/login" />
          } />
          <Route path="/" element={<Navigate to="/sensors" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;