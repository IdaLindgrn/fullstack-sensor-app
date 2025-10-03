# Sensor Monitoring System

A small web app to manage sensors and visualize temperature and humidity readings.

## Quick Start

Requirements: Docker & Docker Compose (Make optional).

### Setup

1. Clone the repository
2. Build and start services:

   ```bash
   make build
   make up
   ```

3. Initialize the database:

   ```bash
   make migrate
   make seed
   ```

4. Access the application at

- **Frontend**: http://localhost:3000
- **Backend API docs**: http://localhost:8000/api/docs

### Run Tests

```bash
make test
```

## Default demo account

- **Email**: admin@example.com
- **Password**: admin123

## API Overview

Base URL: `http://localhost:8000/api/`

### Auth

| Method | Endpoint          | Description                                                               |
| ------ | ----------------- | ------------------------------------------------------------------------- |
| POST   | `/auth/register/` | Register with `email`, `username`, `password` → returns `{ token, user }` |
| POST   | `/auth/token/`    | Login with `email`, `password` → returns `{ token, user }`                |

### Sensors

| Method | Endpoint         | Description                                             |
| ------ | ---------------- | ------------------------------------------------------- |
| GET    | `/sensors/`      | List sensors (requires `Authorization: Bearer <token>`) |
| POST   | `/sensors/`      | Create sensor                                           |
| GET    | `/sensors/{id}/` | Get sensor                                              |
| PATCH  | `/sensors/{id}/` | Update sensor                                           |
| DELETE | `/sensors/{id}/` | Delete sensor                                           |

### Readings

| Method | Endpoint                  | Description                                               |
| ------ | ------------------------- | --------------------------------------------------------- |
| GET    | `/sensors/{id}/readings/` | List readings (optional `timestamp_from`, `timestamp_to`) |
| POST   | `/sensors/{id}/readings/` | Create reading (`temperature`, `humidity`, `timestamp`)   |

## Notes

- The backend uses JWTs. The frontend stores the token and includes it in Authorization headers.
- Seeded readings come from backend/sensor_readings_wide.csv when you run make seed.
