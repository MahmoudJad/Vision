#!/bin/bash

# Vision Docker Management Script

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/docker/docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to start services
start_services() {
    print_status "Starting Vision services..."
    check_docker
    
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        print_warning ".env file not found. Creating default .env file..."
        # The .env file should already be created by this script
    fi
    
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d
    
    print_status "Waiting for database to be ready..."
    sleep 10
    
    print_status "Running database migrations..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T vision alembic upgrade head || true
    
    print_status "Services started successfully!"
    print_status "API: http://localhost:8000"
    print_status "API Docs: http://localhost:8000/docs"
    print_status "PgAdmin: http://localhost:5050 (admin@admin.com / root)"
}

# Function to stop services
stop_services() {
    print_status "Stopping Vision services..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down
    print_status "Services stopped."
}

# Function to restart services
restart_services() {
    print_status "Restarting Vision services..."
    stop_services
    start_services
}

# Function to rebuild and restart services
rebuild_services() {
    print_status "Rebuilding and restarting Vision services..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down
    docker-compose -f "$DOCKER_COMPOSE_FILE" up --build -d
    
    print_status "Waiting for database to be ready..."
    sleep 10
    
    print_status "Running database migrations..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T vision alembic upgrade head || true
    
    print_status "Services rebuilt and started successfully!"
}

# Function to show logs
show_logs() {
    docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f "${1:-vision}"
}

# Function to run shell
run_shell() {
    docker-compose -f "$DOCKER_COMPOSE_FILE" exec vision bash
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T vision pytest
}

# Function to show status
show_status() {
    print_status "Checking service status..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" ps
}

# Main script logic
case "$1" in
    "start")
        start_services
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "rebuild")
        rebuild_services
        ;;
    "logs")
        show_logs "$2"
        ;;
    "shell")
        run_shell
        ;;
    "test")
        run_tests
        ;;
    "status")
        show_status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|rebuild|logs [service]|shell|test|status}"
        echo ""
        echo "Commands:"
        echo "  start    - Start all services"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  rebuild  - Rebuild and restart all services"
        echo "  logs     - Show logs (optionally specify service name)"
        echo "  shell    - Open shell in vision container"
        echo "  test     - Run tests"
        echo "  status   - Show service status"
        exit 1
        ;;
esac