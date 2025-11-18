# web-availability-monitor
<div align="center">

# 🌐 Website Availability Monitor 🌐

### Professional real-time monitoring with uptime tracking and beautiful dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/GuezelS/web-availability-monitor)

**Monitor websites • Calculate uptime • Track performance • Web dashboard**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [API](#-api-documentation) • [Configuration](#%EF%B8%8F-configuration)

</div>

---
## 📑 Table of Contents

### Getting Started
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)

### Usage & Documentation
- [Using the Monitor](#usage)
- [Dashboard Guide](#using-the-dashboard)
- [API Documentation](#api-documentation)

### Development
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Contributing](#contributing)

### Additional
- [Roadmap](#roadmap)
- [License](#license)
- [Author](#author)
## ✨ Features

<table>
<tr>
<td width="50%">

### 🔄 Automatic Monitoring
- **Continuous availability checks** every 30 seconds (configurable)
- **Automatic retry mechanism** with 3 attempts on failures
- **Configurable timeout settings** for request handling
- **SQLite database storage** with 30-day data retention

</td>
<td width="50%">

### 📊 Analytics & Reporting
- **Uptime percentage tracking** across multiple time periods
- **Response time statistics** including average, min, max, and median
- **Outage period detection** with start/end timestamps and duration
- **Performance trend analysis** based on historical data

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Web Dashboard
- **Responsive web interface** accessible on all devices
- **Automatic page refresh** every 30 seconds for live updates
- **Visual status indicators** with color-coded badges
- **Real-time metrics display** showing current monitoring state

</td>
<td width="50%">

### 🔌 RESTful API
- **JSON response format** for easy integration
- **Multiple endpoints** for uptime, performance, and status data
- **Health check endpoint** for system monitoring
- **Programmatic access** to all monitoring data

</td>
</tr>
</table>
---

## 📸 Screenshots

Below are previews of the real-time monitoring dashboard and its features.

---

## 📸 Screenshots

Below are previews of the real-time monitoring dashboard and its features.

---

### 🖥️ Full Dashboard View
<img src="assets/Screenshot 2025-11-17%20at%2015.00.49.png" alt="Dashboard Overview" width="800">

*Real-time monitoring dashboard with comprehensive statistics*

---

### ⚡ Instant URL Check
<img src="assets/Screenshot 2025-11-17%20at%2015.00.49.png" alt="Instant Check Form" width="800">

*On-demand website availability testing*

---

### 📈 Uptime Breakdown
<img src="docs/images/uptime-breakdown.png" alt="Uptime Analytics" width="800">

*Time-period based uptime tracking (24h, 7d, 30d)*

---

### 🚀 Performance Metrics
<img src="docs/images/performance-metrics.png" alt="Performance Statistics" width="800">

*Response time analysis with min, max, and median values*

---

### 📋 Recent Checks Table
<img src="docs/images/recent-checks.png" alt="Check History" width="800">

*Complete monitoring log with timestamps and status indicators*

---

### 🟢 Active Status Bar
<img src="docs/images/status-bar.png" alt="Status Bar" width="800">

*Live monitoring status with auto-refresh countdown*

---

## 🚀 Quick Start

Get up and running in **60 seconds**:
```bash
# 1. Clone the repository
git clone https://github.com/GuezelS/web-availability-monitor.git
cd web-availability-monitor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure monitoring
cp .env.example .env
# Edit .env and set your MONITOR_URL

# 5. Start monitoring
python run.py &          # Background monitoring
python app.py            # Web dashboard

# 6. Open browser
# Visit: http://localhost:5000
```

✅ **Done!** Your monitoring dashboard is now running!

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Python package manager
- **Git** - [Download](https://git-scm.com/downloads)

### Step-by-Step Installation

#### 1. Clone Repository
```bash
git clone https://github.com/GuezelS/web-availability-monitor.git
cd web-availability-monitor
```

#### 2. Set Up Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` file:
```env
MONITOR_URL=https://your-website.com
CHECK_INTERVAL=30
TIMEOUT=5
DATA_RETENTION_DAYS=30
FLASK_PORT=5000
```

---

## 💻 Usage

### Running the Monitor

#### Option 1: Background Monitoring Only
```bash
python run.py
```

This will:
- ✅ Check your website every 30 seconds
- ✅ Save results to SQLite database
- ✅ Log status to console

**Example output:**
```
==================================================
🌐 Website Availability Monitor
==================================================
✅ Database initialized
🏁 Starting monitoring for https://google.com
⏳ Checking every 30 seconds
[INFO] ✅ https://google.com is UP - 200 (0.347s)
```

#### Option 2: Web Dashboard Only
```bash
python app.py
```

Access dashboard at: **http://localhost:5000**

#### Option 3: Both (Recommended)

**Terminal 1:**
```bash
python run.py
```

**Terminal 2:**
```bash
python app.py
```

---

### Using the Dashboard

#### Main Dashboard

Navigate to `http://localhost:5000` to see:

- **Overall Uptime** - Percentage since monitoring started
- **Total Checks** - Number of monitoring operations
- **Average Response Time** - Mean load time in seconds
- **Failed Checks** - Count of unsuccessful checks

#### Instant URL Check

1. Enter any URL in the check form
2. Click **"Check Now "**
3. Get immediate results with:
   - Status (UP/DOWN)
   - Response time
   - HTTP status code
   - Timestamp

**Examples:**
```
✅ github.com
✅ https://google.com
✅ youtube.com
❌ fake-website.com (will show as DOWN)
```

#### Auto-Refresh

Dashboard automatically refreshes every **30 seconds** to show latest data.

---

## 📊 API Documentation

All API endpoints return JSON responses.

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "total_checks": 1234
}
```

### GET `/api/status`

Complete monitoring report.

**Response:**
```json
{
  "uptime": {
    "overall": 98.5,
    "last_24h": 99.2,
    "last_7d": 98.8,
    "last_30d": 98.5
  },
  "performance": {
    "total_checks": 2880,
    "successful_checks": 2835,
    "failed_checks": 45,
    "avg_response_time": 0.347,
    "min_response_time": 0.123,
    "max_response_time": 2.456,
    "median_response_time": 0.289
  },
  "outages": {
    "total_outages": 3,
    "periods": [...]
  },
  "report_generated": "2025-11-17 10:30:00",
  "report_period_hours": 24
}
```

### GET `/api/uptime`

Uptime percentages only.

**Response:**
```json
{
  "overall": 98.5,
  "last_24h": 99.2,
  "last_7d": 98.8,
  "last_30d": 98.5
}
```

### GET `/api/recent`

Last 20 checks.

**Response:**
```json
[
  {
    "id": 1234,
    "timestamp": "2025-11-17 10:30:00",
    "url": "https://google.com",
    "success": true,
    "response_time": 0.347,
    "status_code": 200
  },
  ...
]
```

### POST `/check`

Instant URL check (form submission).

**Parameters:**
- `url` (string, required) - Website URL to check

**Returns:** Redirect to dashboard with result

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file with these settings:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `MONITOR_URL` | Website to monitor | - | `https://google.com` |
| `CHECK_INTERVAL` | Seconds between checks | `30` | `60` |
| `TIMEOUT` | Request timeout (seconds) | `5` | `10` |
| `DATA_RETENTION_DAYS` | Days to keep data | `30` | `90` |
| `FLASK_PORT` | Dashboard port | `5000` | `8000` |

### Example Configuration

**Quick check (every minute):**
```env
MONITOR_URL=https://your-site.com
CHECK_INTERVAL=60
TIMEOUT=5
```

**Long-term monitoring:**
```env
MONITOR_URL=https://your-site.com
CHECK_INTERVAL=300
DATA_RETENTION_DAYS=90
```

---

## 📁 Project Structure
```
web-availability-monitor/
├── 📄 README.md                    # Project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                # Environment configuration template
├── 📄 .gitignore                  # Git ignore rules
├── 🐍 run.py                      # Main monitoring entry point
├── 🌐 app.py                      # Flask web application
│
├── 📂 src/                        # Source code
│   ├── __init__.py               # Package initialization
│   ├── monitor.py                # Website availability checking
│   ├── database.py               # SQLite database operations
│   ├── analytics.py              # Uptime and performance calculations
│   ├── scheduler.py              # Background task scheduling
│   └── logger.py                 # Colored console logging
│
├── 📂 templates/                  # Jinja2 HTML templates
│   └── index.html                # Dashboard (includes embedded CSS/JS)
│
├── 📂 data/                       # Database storage
│   ├── .gitkeep
│   └── monitoring.db             # SQLite database (created at runtime)
│
└── 📂 tests/                      # Test suite
    ├── __init__.py
    └── test_database_integration.py
```

---

## 🛠️ Technologies Used

### Backend
- **[Python 3.8+](https://www.python.org/)** - Core programming language for all backend logic
- **[Flask 3.0](https://flask.palletsprojects.com/)** - Web framework for dashboard and REST API
- **[APScheduler 3.10.4](https://apscheduler.readthedocs.io/)** - Background scheduler for periodic monitoring
- **[Requests 2.31.0](https://requests.readthedocs.io/)** - HTTP client for website availability checks
- **[SQLite 3](https://www.sqlite.org/)** - Embedded database for monitoring history

### Frontend
- **HTML5/CSS3** - Responsive web interface with modern design
- **[Jinja2](https://jinja.palletsprojects.com/)** - Template engine (bundled with Flask)
- **JavaScript** - Client-side auto-refresh functionality

### Development Tools
- **[python-dotenv 1.0.0](https://github.com/theskumar/python-dotenv)** - Environment configuration management
- **[colorlog 6.8.0](https://github.com/borntyping/python-colorlog)** - Color-coded console logging

---

## 🧪 Testing

Run integration tests:
```bash
python tests/test_database_integration.py
```

**Expected output:**
```
Testing database integration...
✅ All tests passed!
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/BetterFeature`)
3. **Commit** your changes (`git commit -m 'Add some BetterFeature'`)
4. **Push** to the branch (`git push origin feature/BetterFeature`)
5. **Open** a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
```
MIT License

Copyright (c) 2025 Sevdenur Güzel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 👤 Author

**Sevdenur Güzel** @ SAP

- GitHub: [@GuezelS](https://github.com/GuezelS)
- LinkedIn: [Sevdenur Güzel](https://linkedin.com/in/your-profile)
- Email: sevdenur.guezel@sap.com

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/GuezelS/web-availability-monitor?style=social)
![GitHub forks](https://img.shields.io/github/forks/GuezelS/web-availability-monitor?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/GuezelS/web-availability-monitor?style=social)

---

<div align="center">

**Made with 💜 by Sevdenur Güzel @ SAP**

[Report Bug](https://github.com/GuezelS/web-availability-monitor/issues) • [Request Feature](https://github.com/GuezelS/web-availability-monitor/issues)

</div>