#!/bin/bash

# Smart Study Assistant - Development Run Script
# This script sets up and runs the entire application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Smart Study Assistant Setup${NC}"
echo -e "${GREEN}================================${NC}"

# Check Python
echo -e "\n${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.9+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}Python ${PYTHON_VERSION} found${NC}"

# Check Node
echo -e "\n${YELLOW}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}Node.js ${NODE_VERSION} found${NC}"

# Setup Python Backend
echo -e "\n${YELLOW}Setting up Python backend...${NC}"

if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo -e "${RED}Failed to find virtual environment activation script${NC}"
    exit 1
fi

echo -e "${GREEN}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirment.txt

# Setup Frontend
echo -e "\n${YELLOW}Setting up Node.js frontend...${NC}"

if [ ! -d "node_modules" ]; then
    echo -e "${GREEN}Installing Node dependencies...${NC}"
    npm install
fi

# Create data directory
mkdir -p data

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"

echo -e "\n${YELLOW}To start the application:${NC}"
echo -e "\n${GREEN}Terminal 1 (Backend):${NC}"
echo -e "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo -e "  uvicorn api:app --reload --port 8000"

echo -e "\n${GREEN}Terminal 2 (Frontend):${NC}"
echo -e "  npm run dev"

echo -e "\n${GREEN}Then open: http://localhost:3000${NC}"

echo -e "\n${YELLOW}Or use Docker Compose:${NC}"
echo -e "  docker-compose up --build"

echo -e "\n${YELLOW}For more information, see SETUP.md${NC}\n"
