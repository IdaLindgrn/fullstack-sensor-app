import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './SensorDetails.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SensorDetail({ token }) {
  const { id } = useParams();
  const [sensor, setSensor] = useState(null);
  const [readings, setReadings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [dateRange, setDateRange] = useState({ from: '', to: '' });
  const [newReading, setNewReading] = useState({
    temperature: '',
    humidity: '',
    timestamp: new Date().toISOString().slice(0, 16)
  });

  const fetchSensor = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/sensors/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSensor(response.data);
    } catch (err) {
      setError('Failed to load sensor');
    }
  };

  const fetchReadings = async () => {
    setLoading(true);
    try {
      const params = {};
      if (dateRange.from) params.timestamp_from = dateRange.from;
      if (dateRange.to) params.timestamp_to = dateRange.to;

      const response = await axios.get(`${API_URL}/api/sensors/${id}/readings/`, {
        headers: { Authorization: `Bearer ${token}` },
        params
      });
      setReadings(response.data);
    } catch (err) {
      setError('Failed to load readings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSensor();
    fetchReadings();
  }, [id, dateRange]);

  const handleCreateReading = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/sensors/${id}/readings/`, {
        ...newReading,
        temperature: parseFloat(newReading.temperature),
        humidity: parseFloat(newReading.humidity),
        timestamp: new Date(newReading.timestamp).toISOString()
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setShowModal(false);
      setNewReading({ temperature: '', humidity: '', timestamp: new Date().toISOString().slice(0, 16) });
      fetchReadings();
    } catch (err) {
      setError('Failed to create reading');
    }
  };

  const chartData = readings.map(r => ({
    time: new Date(r.timestamp).toLocaleString(),
    temperature: r.temperature,
    humidity: r.humidity
  })).reverse();

  if (!sensor) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <Link to="/sensors" className="back-link">← Back to Sensors</Link>
      
      <div className="sensor-header">
        <div>
          <h2>{sensor.name}</h2>
          <p className="model">{sensor.model}</p>
          {sensor.description && <p className="description">{sensor.description}</p>}
        </div>
        <button className="btn btn-success" onClick={() => setShowModal(true)}>
          + Add Reading
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <h3>Date Range Filter</h3>
        <div className="date-filters">
          <input
            type="datetime-local"
            value={dateRange.from}
            onChange={(e) => setDateRange({...dateRange, from: e.target.value})}
            placeholder="From"
          />
          <input
            type="datetime-local"
            value={dateRange.to}
            onChange={(e) => setDateRange({...dateRange, to: e.target.value})}
            placeholder="To"
          />
          <button 
            className="btn btn-primary" 
            onClick={() => setDateRange({ from: '', to: '' })}
          >
            Clear
          </button>
        </div>
      </div>

      {readings.length > 0 ? (
        <div className="card chart-card">
          <h3>Temperature & Humidity Over Time</h3>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" angle={-45} textAnchor="end" height={100} />
              <YAxis yAxisId="left" label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }} />
              <YAxis yAxisId="right" orientation="right" label={{ value: 'Humidity (%)', angle: 90, position: 'insideRight' }} />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="temperature" stroke="#e74c3c" name="Temperature (°C)" />
              <Line yAxisId="right" type="monotone" dataKey="humidity" stroke="#3498db" name="Humidity (%)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="empty-state">
          <p>No readings yet. Add one to see the chart!</p>
        </div>
      )}

      {showModal && (
        <div className="modal" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Add New Reading</h3>
            <form onSubmit={handleCreateReading}>
              <input
                type="number"
                step="0.1"
                placeholder="Temperature (°C)"
                value={newReading.temperature}
                onChange={(e) => setNewReading({...newReading, temperature: e.target.value})}
                required
              />
              <input
                type="number"
                step="0.1"
                placeholder="Humidity (%)"
                value={newReading.humidity}
                onChange={(e) => setNewReading({...newReading, humidity: e.target.value})}
                required
              />
              <input
                type="datetime-local"
                value={newReading.timestamp}
                onChange={(e) => setNewReading({...newReading, timestamp: e.target.value})}
                required
              />
              <div className="modal-actions">
                <button type="button" className="btn" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-success">Add Reading</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default SensorDetail;