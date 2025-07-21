#!/usr/bin/env python3
"""
Port Monitor - Real-Time Port Monitoring Dashboard

A beautiful, terminal-style web dashboard for monitoring port usage across
all your active coding projects. Perfect for managing multiple development
servers and preventing port conflicts.

Author: Port Monitor Contributors
License: MIT
Repository: https://github.com/teamsumdigital/port-monitor
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import socket
import subprocess
import json
import os
import glob
from typing import Dict, List, Optional, Any
from datetime import datetime

app = Flask(__name__)
CORS(app)

class PortMonitor:
    """Enhanced port monitoring for all active projects."""
    
    def __init__(self, projects_path=None):
        # Default to looking for 'projects' or 'coding-projects' in user's home
        if projects_path is None:
            home = os.path.expanduser("~")
            possible_paths = [
                os.path.join(home, "coding-projects", "active-projects"),
                os.path.join(home, "projects"),
                os.path.join(home, "dev"),
                os.path.join(home, "development"),
                os.path.join(home, "code")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.active_projects_path = path
                    break
            else:
                # If none exist, default to first option and let user create it
                self.active_projects_path = possible_paths[0]
        else:
            self.active_projects_path = projects_path
            
        self.port_cache = {}
        self.last_update = None
        self.project_configs = self._discover_projects()
        
    def _discover_projects(self) -> Dict[str, Dict]:
        """Auto-discover projects and their expected ports."""
        projects = {}
        
        if not os.path.exists(self.active_projects_path):
            print(f"📁 Projects directory not found: {self.active_projects_path}")
            print(f"💡 Create it with: mkdir -p {self.active_projects_path}")
            return projects
            
        for project_dir in os.listdir(self.active_projects_path):
            project_path = os.path.join(self.active_projects_path, project_dir)
            
            if os.path.isdir(project_path) and not project_dir.startswith('.'):
                config = self._analyze_project(project_dir, project_path)
                if config:
                    projects[project_dir] = config
                    
        return projects
    
    def _analyze_project(self, name: str, path: str) -> Optional[Dict]:
        """Analyze a project directory to determine its port configuration."""
        config = {
            'name': name,
            'path': path,
            'type': 'unknown',
            'ports': {},
            'status': 'unknown',
            'framework': 'unknown',
            'description': ''
        }
        
        # Check for different project types and their typical ports
        if os.path.exists(os.path.join(path, 'package.json')):
            # Node.js/React project
            config['type'] = 'frontend'
            config['framework'] = self._detect_frontend_framework(path)
            config['ports']['frontend'] = self._detect_frontend_port(path)
            
        if os.path.exists(os.path.join(path, 'main.py')) or os.path.exists(os.path.join(path, 'app.py')):
            # Python backend project
            config['type'] = 'fullstack' if config['type'] == 'frontend' else 'backend'
            config['framework'] = f"{config['framework']}, Python" if config['framework'] != 'unknown' else 'Python'
            config['ports']['backend'] = self._detect_backend_port(path)
            
        if os.path.exists(os.path.join(path, 'docker-compose.yml')):
            # Docker project
            docker_ports = self._parse_docker_ports(path)
            config['ports'].update(docker_ports)
            config['framework'] = f"{config['framework']}, Docker"
            
        # Add generic description
        config['description'] = self._generate_description(config)
        
        return config if config['ports'] else None
    
    def _detect_frontend_framework(self, path: str) -> str:
        """Detect frontend framework from package.json."""
        package_json_path = os.path.join(path, 'package.json')
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                deps = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                if 'react' in deps:
                    if 'vite' in deps:
                        return 'React + Vite'
                    elif 'next' in deps:
                        return 'Next.js'
                    else:
                        return 'React'
                elif 'vue' in deps:
                    return 'Vue.js'
                elif 'angular' in deps:
                    return 'Angular'
                else:
                    return 'Node.js'
        except:
            return 'Node.js'
    
    def _detect_frontend_port(self, path: str) -> int:
        """Detect frontend port from various config files."""
        # Check vite.config.ts/js
        vite_configs = glob.glob(os.path.join(path, 'vite.config.*'))
        if vite_configs:
            return 3000  # Vite default
            
        # Check package.json scripts
        package_json_path = os.path.join(path, 'package.json')
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                scripts = package_data.get('scripts', {})
                for script in scripts.values():
                    if '--port' in script:
                        parts = script.split('--port')
                        if len(parts) > 1:
                            port_part = parts[1].strip().split()[0]
                            try:
                                return int(port_part)
                            except:
                                pass
        except:
            pass
            
        return 3000  # Default
    
    def _detect_backend_port(self, path: str) -> int:
        """Detect backend port from .env files and code."""
        # Check .env files
        env_files = ['.env', '.env.example', 'backend/.env']
        for env_file in env_files:
            env_path = os.path.join(path, env_file)
            if os.path.exists(env_path):
                try:
                    with open(env_path, 'r') as f:
                        for line in f:
                            if line.startswith('PORT='):
                                return int(line.split('=')[1].strip())
                except:
                    pass
                    
        return 8000  # Default
    
    def _parse_docker_ports(self, path: str) -> Dict[str, int]:
        """Parse ports from docker-compose.yml."""
        ports = {}
        compose_path = os.path.join(path, 'docker-compose.yml')
        
        try:
            import yaml
            with open(compose_path, 'r') as f:
                compose_data = yaml.safe_load(f)
                
            services = compose_data.get('services', {})
            for service_name, service_config in services.items():
                service_ports = service_config.get('ports', [])
                for port_mapping in service_ports:
                    if isinstance(port_mapping, str):
                        host_port = int(port_mapping.split(':')[0])
                        ports[f'docker_{service_name}'] = host_port
                        
        except Exception:
            pass
            
        return ports
    
    def _generate_description(self, config: Dict) -> str:
        """Generate a generic description for a project."""
        framework = config.get('framework', 'Unknown')
        project_type = config.get('type', 'unknown')
        
        if 'React' in framework:
            return 'React web application'
        elif 'Vue' in framework:
            return 'Vue.js web application'  
        elif 'Angular' in framework:
            return 'Angular web application'
        elif 'Next.js' in framework:
            return 'Next.js web application'
        elif 'FastAPI' in framework:
            return 'FastAPI backend service'
        elif 'Flask' in framework:
            return 'Flask web service'
        elif 'Python' in framework:
            return 'Python application'
        elif 'Docker' in framework:
            return 'Containerized application'
        elif project_type == 'frontend':
            return 'Frontend web application'
        elif project_type == 'backend':
            return 'Backend API service'
        elif project_type == 'fullstack':
            return 'Full-stack web application'
        else:
            return 'Development project'
    
    def is_port_in_use(self, port: int) -> bool:
        """Check if a port is currently in use."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def get_port_process_info(self, port: int) -> Optional[Dict]:
        """Get detailed information about the process using a port."""
        try:
            result = subprocess.run(
                ['lsof', '-i', f':{port}', '-Fn'], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                info = {}
                
                for line in lines:
                    if line.startswith('p'):
                        info['pid'] = line[1:]
                    elif line.startswith('n'):
                        info['name'] = line[1:]
                    elif line.startswith('c'):
                        info['command'] = line[1:]
                        
                return info
        except Exception:
            pass
            
        return None

    def get_port_process_info_by_pid(self, pid: int) -> Optional[Dict]:
        """Get detailed information about a process by PID."""
        try:
            result = subprocess.run(
                ['ps', '-p', str(pid), '-o', 'pid=,ppid=,user=,comm=,command='], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split(None, 4)
                if len(parts) >= 4:
                    return {
                        'pid': parts[0],
                        'ppid': parts[1],
                        'user': parts[2],
                        'command': parts[3],
                        'full_command': parts[4] if len(parts) > 4 else parts[3]
                    }
        except Exception:
            pass
            
        return None
    
    def get_all_port_status(self) -> Dict[str, Any]:
        """Get comprehensive port status for all projects."""
        current_time = datetime.now()
        
        # Update project discovery every 5 minutes
        if not self.last_update or (current_time - self.last_update).seconds > 300:
            self.project_configs = self._discover_projects()
            self.last_update = current_time
        
        status = {
            'timestamp': current_time.isoformat(),
            'projects': {},
            'summary': {
                'total_projects': len(self.project_configs),
                'active_ports': 0,
                'available_ports': 0,
                'conflicts': [],
                'monitored_path': self.active_projects_path
            }
        }
        
        all_ports_in_use = {}
        
        for project_name, config in self.project_configs.items():
            project_status = {
                'name': project_name,
                'type': config.get('type', 'unknown'),
                'framework': config.get('framework', 'unknown'),
                'description': config.get('description', ''),
                'path': config['path'],
                'ports': {}
            }
            
            for port_type, port_number in config['ports'].items():
                in_use = self.is_port_in_use(port_number)
                process_info = self.get_port_process_info(port_number) if in_use else None
                
                port_status = {
                    'port': port_number,
                    'in_use': in_use,
                    'process': process_info,
                    'status': 'active' if in_use else 'available'
                }
                
                project_status['ports'][port_type] = port_status
                
                if in_use:
                    status['summary']['active_ports'] += 1
                    if port_number in all_ports_in_use:
                        status['summary']['conflicts'].append({
                            'port': port_number,
                            'projects': [all_ports_in_use[port_number], project_name]
                        })
                    else:
                        all_ports_in_use[port_number] = project_name
                else:
                    status['summary']['available_ports'] += 1
            
            status['projects'][project_name] = project_status
        
        return status

# Global port monitor instance
monitor = PortMonitor()

@app.route('/')
def dashboard():
    """Serve the main terminal dashboard."""
    return render_template('terminal-dashboard.html')

@app.route('/classic')
def classic_dashboard():
    """Serve the classic dashboard."""
    return render_template('dashboard.html')

@app.route('/api/ports')
def get_ports():
    """API endpoint for port status data."""
    return jsonify(monitor.get_all_port_status())

@app.route('/api/projects')
def get_projects():
    """API endpoint for project discovery."""
    return jsonify({
        'projects': monitor.project_configs,
        'count': len(monitor.project_configs),
        'monitored_path': monitor.active_projects_path
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Port Monitoring Dashboard',
        'timestamp': datetime.now().isoformat(),
        'monitored_projects': len(monitor.project_configs),
        'monitored_path': monitor.active_projects_path
    })

@app.route('/api/kill/<int:pid>', methods=['POST'])
def kill_process(pid):
    """Kill a process by PID."""
    try:
        import signal
        import os
        
        # Validate PID exists
        try:
            os.kill(pid, 0)  # This doesn't kill, just checks if PID exists
        except OSError:
            return jsonify({
                'success': False,
                'error': f'Process {pid} not found or already terminated'
            }), 404
        
        # Get process info before killing
        process_info = monitor.get_port_process_info_by_pid(pid)
        
        # Kill the process
        os.kill(pid, signal.SIGTERM)
        
        # Wait a moment then force kill if still running
        import time
        time.sleep(1)
        
        try:
            os.kill(pid, 0)  # Check if still running
            # If we get here, process is still running, force kill
            os.kill(pid, signal.SIGKILL)
        except OSError:
            # Process is already dead, which is what we want
            pass
            
        return jsonify({
            'success': True,
            'message': f'Process {pid} terminated successfully',
            'process_info': process_info
        })
        
    except PermissionError:
        return jsonify({
            'success': False,
            'error': f'Permission denied: Cannot kill process {pid} (try running as administrator)'
        }), 403
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to kill process {pid}: {str(e)}'
        }), 500

@app.route('/api/kill-port/<int:port>', methods=['POST'])
def kill_port(port):
    """Kill all processes using a specific port."""
    try:
        import signal
        import os
        import time
        
        # Find processes using the port
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            return jsonify({
                'success': False,
                'error': f'No processes found using port {port}'
            }), 404
        
        pids = [int(pid.strip()) for pid in result.stdout.strip().split('\n') if pid.strip()]
        killed_processes = []
        
        for pid in pids:
            try:
                process_info = monitor.get_port_process_info_by_pid(pid)
                os.kill(pid, signal.SIGTERM)
                
                # Wait and force kill if needed
                time.sleep(0.5)
                try:
                    os.kill(pid, 0)
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
                    
                killed_processes.append({
                    'pid': pid,
                    'process_info': process_info
                })
                
            except Exception as e:
                continue
        
        return jsonify({
            'success': True,
            'message': f'Killed {len(killed_processes)} processes using port {port}',
            'killed_processes': killed_processes
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to kill processes on port {port}: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Port Monitoring Dashboard...")
    print(f"📊 Dashboard: http://localhost:8080")
    print(f"🔌 API: http://localhost:8080/api/ports")
    print(f"📁 Monitoring: {monitor.active_projects_path}")
    print(f"📦 Found {len(monitor.project_configs)} projects")
    
    app.run(host='0.0.0.0', port=8080, debug=True)