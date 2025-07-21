#!/usr/bin/env python3
"""
Port Monitor Configuration

Customize these settings to match your development environment.
"""

import os

class PortMonitorConfig:
    """Configuration settings for Port Monitor."""
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 8080
    DEBUG = True
    
    # Project Discovery Settings
    # The monitor will look for projects in these directories (in order)
    PROJECT_SEARCH_PATHS = [
        os.path.expanduser("~/coding-projects/active-projects"),
        os.path.expanduser("~/projects"),
        os.path.expanduser("~/dev"),
        os.path.expanduser("~/development"),
        os.path.expanduser("~/code"),
        os.path.expanduser("~/workspace")
    ]
    
    # Port Range Assignments (for documentation)
    PORT_RANGES = {
        'frontend': (3000, 3099),  # React, Vue, Angular, etc.
        'backend': (8000, 8099),   # FastAPI, Flask, Django, etc.
        'legacy': (5000, 5999),    # Flask, Node.js legacy apps
        'databases': (5432, 5499), # PostgreSQL, MySQL, etc.
        'services': (6379, 6399),  # Redis, etc.
        'utilities': (8080, 8089)  # Monitoring, development tools
    }
    
    # Auto-refresh interval (seconds)
    AUTO_REFRESH_INTERVAL = 3
    
    # Project discovery refresh interval (seconds)
    PROJECT_DISCOVERY_INTERVAL = 300  # 5 minutes

# Default configuration instance
config = PortMonitorConfig()