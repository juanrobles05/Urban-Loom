#!/usr/bin/env python
"""
Health check script for Urban-Loom
Used by Docker HEALTHCHECK
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, '/app')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_prod')

import django
django.setup()

from django.core import management
from django.db import connections
from django.db.utils import OperationalError

def check_database():
    """Check if database is accessible"""
    db_conn = connections['default']
    try:
        db_conn.cursor()
        return True
    except OperationalError:
        return False

def main():
    """Run health checks"""
    print("🏥 Running health checks...")
    
    # Check database
    if not check_database():
        print("❌ Database check failed")
        sys.exit(1)
    print("✅ Database is healthy")
    
    # Can add more checks here
    # - Check if static files are accessible
    # - Check if media directory is writable
    # - Check external API connectivity
    
    print("✅ All health checks passed")
    sys.exit(0)

if __name__ == "__main__":
    main()
