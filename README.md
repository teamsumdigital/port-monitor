# 🔌 Port Monitor

A beautiful, real-time web dashboard for monitoring port usage across all your active coding projects. Built with a sleek terminal aesthetic and designed for developers who manage multiple services.

![Port Monitor Terminal](https://img.shields.io/badge/Terminal-Style-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🖥️ **Terminal-Style Interface**
- **GitHub Dark Theme**: Professional terminal color scheme with syntax highlighting
- **JetBrains Mono Font**: Crisp, modern monospace typography
- **Real Terminal Window**: Authentic title bar with window controls
- **Command Prompt**: Simulated bash prompt with blinking cursor

### 🔄 **Real-Time Monitoring**
- **3-second refresh**: Live updates of all port statuses
- **Auto-discovery**: Automatically finds projects in common directories
- **Process identification**: Shows exactly what's using each port (PID, command, user)
- **Conflict detection**: Instantly alerts you to port conflicts

### ⚡ **One-Click Actions**
- **Kill Process**: Actually terminate processes using ports (not just copy commands!)
- **Open in Browser**: Direct links to running services
- **Copy Commands**: Clipboard integration for `lsof`, `kill`, etc.
- **Visual Feedback**: Beautiful notifications for all actions

### 🎯 **Smart Project Detection**
- **React/Vue/Angular**: Detects frontend frameworks and expected ports
- **FastAPI/Flask/Django**: Backend service detection
- **Docker Compose**: Port mapping discovery
- **Environment Files**: Reads `.env` files for port configuration

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/teamsumdigital/port-monitor.git
cd port-monitor
```

### 2. **Start the Monitor**
```bash
./start.sh
```

### 3. **Open in Browser**
Navigate to: **http://localhost:8080**

That's it! The monitor will automatically discover projects in common directories like:
- `~/coding-projects/active-projects`
- `~/projects`
- `~/dev`
- `~/development`
- `~/code`

## 📊 What You'll See

```
🖥️ port-monitor.sh • ~/projects
user@localhost:~$ port-monitor --live --auto-discover |

📊 SYSTEM OVERVIEW
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Projects: 5 │ Active: 3   │ Available:7 │ Conflicts:0 │
└─────────────┴─────────────┴─────────────┴─────────────┘

🔌 ACTIVE PROJECTS
┌──────────────┬────────────────┬─────────────────┬─────────────┐
│ Project      │ Framework      │ Ports           │ Actions     │
├──────────────┼────────────────┼─────────────────┼─────────────┤
│ my-react-app │ React + Vite   │ ● 3000 frontend │ kill open   │
│ api-server   │ FastAPI        │ ● 8000 backend  │ kill open   │
│ old-flask    │ Flask          │ ○ 5000 backend  │             │
└──────────────┴────────────────┴─────────────────┴─────────────┘
```

## 🎮 Dashboard Controls

### **Auto-Refresh Controls**
- **pause/resume**: Toggle 3-second auto-refresh
- **refresh**: Manual refresh
- **show active/show all**: Filter projects by port status

### **Keyboard Shortcuts**
- `Ctrl+R` (⌘+R): Refresh now
- `Ctrl+Space` (⌘+Space): Toggle auto-refresh

### **Port Actions**
- **kill**: Terminate the process using the port
- **open**: Open `http://localhost:[PORT]` in browser
- **lsof**: Copy `lsof -i :[PORT]` command
- **copy**: Copy `kill -9 [PID]` command

## 🛠️ Advanced Usage

### **Background Mode**
```bash
# Start in background
./start-background.sh

# Stop the monitor
./stop.sh
```

### **Custom Project Directory**
Edit `config.py` to add your project directories:
```python
PROJECT_SEARCH_PATHS = [
    os.path.expanduser("~/my-custom-projects"),
    os.path.expanduser("~/work"),
    # ... add your paths
]
```

### **Port Range Configuration**
Customize port assignments in `config.py`:
```python
PORT_RANGES = {
    'frontend': (3000, 3099),
    'backend': (8000, 8099),
    'databases': (5432, 5499),
    # ... customize as needed
}
```

## 🔧 API Endpoints

Port Monitor provides a REST API for integration:

### **GET /api/ports**
Complete port status for all projects
```json
{
  "timestamp": "2025-01-21T12:00:00",
  "projects": {
    "my-app": {
      "name": "my-app",
      "type": "fullstack",
      "framework": "React + Vite, FastAPI",
      "ports": {
        "frontend": {
          "port": 3000,
          "in_use": true,
          "process": {"pid": "1234", "command": "vite"}
        }
      }
    }
  },
  "summary": {
    "total_projects": 5,
    "active_ports": 3,
    "available_ports": 7,
    "conflicts": []
  }
}
```

### **GET /api/health**
Service health check
```json
{
  "status": "healthy",
  "service": "Port Monitoring Dashboard",
  "monitored_projects": 5
}
```

### **POST /api/kill/{pid}**
Kill a process by PID
```json
{
  "success": true,
  "message": "Process 1234 terminated successfully"
}
```

## 🎨 Project Detection

Port Monitor automatically detects these project types:

| Framework | Detection Method | Default Port |
|-----------|-----------------|--------------|
| **React + Vite** | `vite.config.*` files | 3000 |
| **Next.js** | `next` in package.json | 3000 |
| **Vue.js** | `vue` in dependencies | 3000 |
| **Angular** | `angular` in dependencies | 4200 |
| **FastAPI** | `main.py` or `app.py` | 8000 |
| **Flask** | `flask` in dependencies | 5000 |
| **Docker** | `docker-compose.yml` | From compose file |

### **Custom Project Configuration**
Projects are detected by:
1. **package.json** for Node.js projects
2. **main.py/app.py** for Python projects  
3. **docker-compose.yml** for containerized apps
4. **.env files** for port configuration

## 📁 Directory Structure

```
port-monitor/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── start.sh                  # Start the monitor
├── start-background.sh       # Start in background
├── stop.sh                   # Stop the monitor
├── templates/
│   ├── terminal-dashboard.html   # Terminal-style dashboard
│   └── dashboard.html           # Classic glass-style dashboard
└── README.md                # This file
```

## 🔒 Security & Privacy

Port Monitor is designed to be completely safe and private:
- **No data collection**: All monitoring is local-only
- **No external connections**: Never sends data outside your machine
- **Process permissions**: Only kills processes you have permission to kill
- **Open source**: Full transparency - inspect the code yourself

## 🚀 Installation & Setup

### **Requirements**
- **Python 3.7+**
- **macOS or Linux** (for `lsof` command)
- **Modern web browser**

### **Quick Install**
```bash
# Clone and run
git clone https://github.com/teamsumdigital/port-monitor.git
cd port-monitor
./start.sh
```

### **Manual Setup**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python3 app.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### **Development Setup**
```bash
git clone https://github.com/teamsumdigital/port-monitor.git
cd port-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## 📋 Troubleshooting

### **Port Monitor Won't Start**
```bash
# Check if port 8080 is in use
lsof -i :8080

# Kill process using port 8080
kill -9 $(lsof -ti :8080)

# Restart Port Monitor
./start.sh
```

### **No Projects Detected**
- Ensure projects exist in supported directories (`~/projects`, `~/dev`, etc.)
- Check that projects have recognizable files (`package.json`, `main.py`, etc.)
- Edit `config.py` to add custom project paths

### **Kill Button Not Working**
- Ensure you have permission to kill the process
- Check that the process still exists (it might have already exited)
- Try the manual command shown in error messages

### **Permission Errors**
```bash
# On macOS, you might need to grant terminal permissions
# System Preferences → Security & Privacy → Privacy → Developer Tools
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Terminal Design**: Inspired by GitHub's terminal aesthetic
- **Font**: JetBrains Mono for beautiful monospace typography
- **Icons**: Unicode emojis for cross-platform compatibility
- **Colors**: GitHub dark theme color palette

## 🔗 Links

- **GitHub Repository**: https://github.com/teamsumdigital/port-monitor
- **Issues & Bug Reports**: https://github.com/teamsumdigital/port-monitor/issues
- **Feature Requests**: https://github.com/teamsumdigital/port-monitor/discussions

---

**Built with ❤️ for developers who manage multiple projects and are tired of port conflicts!**

### 📊 **Perfect For:**
- **Multi-project development environments**
- **Teams managing multiple services**
- **DevOps and development workflows**
- **Anyone who wants beautiful, functional tooling**

**🌐 Start monitoring your ports in style: `./start.sh` and visit http://localhost:8080**