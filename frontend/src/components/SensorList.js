import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './SensorList.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SensorList({ token }) {
  const [sensors, setSensors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [newSensor, setNewSensor] = useState({ name: '', model: '', description: '' });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchSensors = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/sensors/`, {
        headers: { Authorization: `Bearer ${token}` },
        params: { page, q: search }
      });
      setSensors(response.data.items);
      setTotalPages(Math.ceil(response.data.count / 10));
    } catch (err) {
      setError('Failed to load sensors');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSensors();
  }, [page, search]);

  const handleCreateSensor = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/api/sensors/`, newSensor, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setShowModal(false);
      setNewSensor({ name: '', model: '', description: '' });
      fetchSensors();
    } catch (err) {
      setError('Failed to create sensor');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Delete this sensor and all its readings?')) {
      try {
        await axios.delete(`${API_URL}/api/sensors/${id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchSensors();
      } catch (err) {
        setError('Failed to delete sensor');
      }
    }
  };

  if (loading && sensors.length === 0) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <div className="header">
        <h2>My Sensors</h2>
        <button className="btn btn-success" onClick={() => setShowModal(true)}>
          + Add Sensor
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="search-box">
        <input
          type="text"
          placeholder="Search sensors"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="sensor-grid">
        {sensors.map(sensor => (
          <div key={sensor.id} className="sensor-card">
            <h3>{sensor.name}</h3>
            <p className="model">{sensor.model}</p>
            {sensor.description && <p className="description">{sensor.description}</p>}
            <div className="card-actions">
              <Link to={`/sensors/${sensor.id}`} className="btn btn-primary">View</Link>
              <button className="btn btn-danger" onClick={() => handleDelete(sensor.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>

      {sensors.length === 0 && !loading && (
        <div className="empty-state">
          <p>No sensors found. Create one to get started!</p>
        </div>
      )}

      {totalPages > 1 && (
        <div className="pagination">
          <button 
            className="btn btn-primary" 
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            Previous
          </button>
          <span>Page {page} of {totalPages}</span>
          <button 
            className="btn btn-primary" 
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            Next
          </button>
        </div>
      )}

      {showModal && (
        <div className="modal" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Add New Sensor</h3>
            <form onSubmit={handleCreateSensor}>
              <input
                type="text"
                placeholder="Sensor name"
                value={newSensor.name}
                onChange={(e) => setNewSensor({...newSensor, name: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Model"
                value={newSensor.model}
                onChange={(e) => setNewSensor({...newSensor, model: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Description"
                value={newSensor.description}
                onChange={(e) => setNewSensor({...newSensor, description: e.target.value})}
              />
              <div className="modal-actions">
                <button type="button" className="btn" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-success">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default SensorList;