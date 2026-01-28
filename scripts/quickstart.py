#!/usr/bin/env python3
"""
Sentinel Quick Start Script

This script helps initialize the Sentinel backend for first-time setup.
"""

import os
import sys
from pathlib import Path

def main():
    """Run the quick start setup."""
    print("=" * 60)
    print("Sentinel Backend - Quick Start")
    print("=" * 60)
    print()
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Error: Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print("✅ Python version check passed")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: No virtual environment detected")
        print("   It's recommended to use a virtual environment")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("   Exiting...")
            sys.exit(0)
    else:
        print("✅ Virtual environment detected")
    
    # Check for .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  No .env file found")
        print("   Creating .env from .env.example...")
        
        env_example = Path(".env.example")
        if env_example.exists():
            with open(env_example) as src:
                with open(env_file, 'w') as dst:
                    dst.write(src.read())
            print("✅ Created .env file")
            print("   ⚠️  Please edit .env and add your configuration")
        else:
            print("❌ Error: .env.example not found")
    else:
        print("✅ .env file exists")
    
    # Check if requirements are installed
    print("\nChecking dependencies...")
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        print("✅ Core dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit .env and add your configuration")
    print("2. Ensure PostgreSQL is running")
    print("3. Create database: createdb sentinel")
    print("4. Run migrations: alembic upgrade head")
    print("5. Start server: uvicorn app.main:app --reload")
    print("\nDocumentation: /docs")
    print("=" * 60)


if __name__ == "__main__":
    main()
