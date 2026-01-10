#!/bin/bash

# Enterprise Application Manager - Interactive Management Script
# A general-purpose interactive shell for managing the application

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/manage.config.sh"
CONFIG_EXAMPLE="${SCRIPT_DIR}/manage.config.example.sh"

# Load configuration
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
elif [ -f "$CONFIG_EXAMPLE" ]; then
    echo "⚠ Configuration file not found. Creating from example..."
    cp "$CONFIG_EXAMPLE" "$CONFIG_FILE"
    source "$CONFIG_FILE"
    echo "✓ Created manage.config.sh - you can customize it for your environment"
    echo ""
    sleep 2
else
    echo "✗ Error: Neither manage.config.sh nor manage.config.example.sh found!"
    exit 1
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}  ${APP_NAME} - Management${NC}"
    echo -e "${CYAN}================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if Docker is required and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        return 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker Desktop."
        return 1
    fi

    return 0
}

# Get local network IP address
get_network_ip() {
    # Try different methods to get network IP based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        hostname -I 2>/dev/null | awk '{print $1}' || ip route get 1 2>/dev/null | awk '{print $7; exit}' || echo "127.0.0.1"
    else
        echo "127.0.0.1"
    fi
}

# Main menu
show_menu() {
    clear
    print_header
    echo "Select an option:"
    echo ""
    echo "  1) Start application (Docker)"
    echo "  2) Stop application"
    echo "  3) Restart application"
    echo "  4) View logs"
    echo "  5) Shell access"
    echo "  6) Database management"
    echo "  7) MinIO management"
    echo "  8) Django commands"
    echo "  9) Development tools"
    echo "  a) Open in browser"
    echo ""
    echo "  0) Exit"
    echo ""
    echo -n "Enter choice: "
}

# Start application
start_application() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    print_info "Starting application..."
    echo ""

    # Change to project directory
    cd "$PROJECT_ROOT"

    # Start docker-compose
    if docker-compose -f "$DOCKER_COMPOSE_FILE" up -d; then
        echo ""
        print_success "Application started successfully!"
        echo ""
        print_info "Services running:"
        echo "  • Web application: https://localhost:${WEB_PORT}"
        echo "  • MinIO console: ${MINIO_CONSOLE_URL}"
        echo ""
        print_warning "Note: HTTPS uses self-signed certificate - accept security warning in browser"
        echo ""
        print_info "Use option 4 to view logs or option 'a' to open in browser"

        # Show container status
        echo ""
        docker-compose -f "$DOCKER_COMPOSE_FILE" ps
    else
        echo ""
        print_error "Failed to start application"
        return 1
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# Stop application
stop_application() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    print_info "Stopping application..."
    echo ""

    # Change to project directory
    cd "$PROJECT_ROOT"

    # Stop docker-compose
    if docker-compose -f "$DOCKER_COMPOSE_FILE" down; then
        echo ""
        print_success "Application stopped successfully!"
    else
        echo ""
        print_error "Failed to stop application"
        return 1
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# Restart application
restart_application() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    print_info "Restarting application..."
    echo ""

    # Change to project directory
    cd "$PROJECT_ROOT"

    # Restart docker-compose
    if docker-compose -f "$DOCKER_COMPOSE_FILE" restart; then
        echo ""
        print_success "Application restarted successfully!"
        echo ""
        print_info "Services running:"
        echo "  • Web application: https://localhost:${WEB_PORT}"
        echo "  • MinIO console: ${MINIO_CONSOLE_URL}"
        echo ""

        # Show container status
        docker-compose -f "$DOCKER_COMPOSE_FILE" ps
    else
        echo ""
        print_error "Failed to restart application"
        return 1
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# View logs
view_logs() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    echo "Log options:"
    echo "  1) Web application logs (follow)"
    echo "  2) MinIO logs (follow)"
    echo "  3) nginx logs (follow)"
    echo "  4) All logs (follow)"
    echo "  5) Web application logs (last ${LOG_TAIL_LINES} lines)"
    echo "  6) MinIO logs (last ${LOG_TAIL_LINES} lines)"
    echo "  7) nginx logs (last ${LOG_TAIL_LINES} lines)"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s log_choice
    echo ""

    cd "$PROJECT_ROOT"

    case $log_choice in
        1)
            clear
            print_info "Following web application logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f web
            ;;
        2)
            clear
            print_info "Following MinIO logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f minio
            ;;
        3)
            clear
            print_info "Following nginx logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f nginx
            ;;
        4)
            clear
            print_info "Following all logs (Ctrl+C to exit)..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" logs -f
            ;;
        5)
            clear
            print_info "Web application logs (last ${LOG_TAIL_LINES} lines)..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" logs --tail=${LOG_TAIL_LINES} web
            echo ""
            read -p "Press Enter to continue..."
            ;;
        6)
            clear
            print_info "MinIO logs (last ${LOG_TAIL_LINES} lines)..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" logs --tail=${LOG_TAIL_LINES} minio
            echo ""
            read -p "Press Enter to continue..."
            ;;
        7)
            clear
            print_info "nginx logs (last ${LOG_TAIL_LINES} lines)..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" logs --tail=${LOG_TAIL_LINES} nginx
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0) return ;;
        *)
            print_error "Invalid option"
            sleep 1
            ;;
    esac
}

# Shell access
shell_access() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    echo "Shell options:"
    echo "  1) Django shell (Python)"
    echo "  2) Container bash shell (web)"
    echo "  3) Container shell (minio)"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s shell_choice
    echo ""

    cd "$PROJECT_ROOT"

    case $shell_choice in
        1)
            clear
            print_info "Opening Django shell... (exit() to quit)"
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py shell
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            clear
            print_info "Opening container bash shell... (exit to quit)"
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec web bash
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            clear
            print_info "Opening MinIO container shell... (exit to quit)"
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec minio sh
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0) return ;;
        *)
            print_error "Invalid option"
            sleep 1
            ;;
    esac
}

# Database management
database_management() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    echo "Database options:"
    echo "  1) Run migrations"
    echo "  2) Create migrations"
    echo "  3) Create superuser"
    echo "  4) Reset database"
    echo "  5) Show migrations status"
    echo "  6) Backup database"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s db_choice
    echo ""

    cd "$PROJECT_ROOT"

    case $db_choice in
        1)
            clear
            print_header
            print_info "Running migrations..."
            echo ""
            if docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py migrate; then
                echo ""
                print_success "Migrations completed successfully!"
            else
                echo ""
                print_error "Failed to run migrations"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            clear
            print_header
            print_info "Creating migrations..."
            echo ""
            echo -n "Enter app name (or leave empty for all apps): "
            read app_name
            echo ""
            if [ -z "$app_name" ]; then
                docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py makemigrations
            else
                docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py makemigrations "$app_name"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            clear
            print_header
            print_info "Creating superuser..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py createsuperuser
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            clear
            print_header
            print_warning "WARNING: This will delete all data in the database!"
            echo ""
            read -p "Are you sure? Type 'yes' to confirm: " confirm
            if [ "$confirm" == "yes" ]; then
                print_info "Resetting database..."
                echo ""

                # Stop containers
                docker-compose -f "$DOCKER_COMPOSE_FILE" down

                # Remove database file
                if [ -f "$DB_FILE" ]; then
                    rm "$DB_FILE"
                    print_success "Database file removed"
                fi

                # Restart containers
                docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

                # Run migrations
                echo ""
                print_info "Running migrations..."
                docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py migrate

                echo ""
                print_success "Database reset complete!"
            else
                print_info "Database reset cancelled"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
            clear
            print_header
            print_info "Migrations status:"
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py showmigrations
            echo ""
            read -p "Press Enter to continue..."
            ;;
        6)
            clear
            print_header
            mkdir -p "$BACKUP_ROOT/$DB_BACKUP_DIR"
            TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
            BACKUP_FILE="$BACKUP_ROOT/$DB_BACKUP_DIR/db_backup_${TIMESTAMP}.sqlite3"
            print_info "Backing up database..."
            echo ""
            if [ -f "$DB_FILE" ]; then
                cp "$DB_FILE" "$BACKUP_FILE"
                print_success "Database backed up to: $BACKUP_FILE"
            else
                print_error "Database file not found: $DB_FILE"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0) return ;;
        *)
            print_error "Invalid option"
            sleep 1
            ;;
    esac
}

# MinIO management
minio_management() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    echo "MinIO options:"
    echo "  1) Create bucket"
    echo "  2) Show credentials"
    echo "  3) Open MinIO console in browser"
    echo "  4) Migrate files to MinIO"
    echo "  5) Verify MinIO connection"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s minio_choice
    echo ""

    cd "$PROJECT_ROOT"

    case $minio_choice in
        1)
            clear
            print_header
            print_info "Creating MinIO bucket..."
            echo ""
            if [ -f "./minio-create-bucket" ]; then
                ./minio-create-bucket
            else
                print_error "minio-create-bucket script not found"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            clear
            print_header
            print_info "MinIO Credentials:"
            echo ""
            if [ -f "$ENV_FILE" ]; then
                echo "Console URL: ${MINIO_CONSOLE_URL}"
                echo ""
                grep "MINIO_ROOT_USER=" "$ENV_FILE" || echo "MINIO_ROOT_USER not set"
                grep "MINIO_ROOT_PASSWORD=" "$ENV_FILE" || echo "MINIO_ROOT_PASSWORD not set"
                echo ""
                print_info "Access MinIO console at: ${MINIO_CONSOLE_URL}"
            else
                print_error "$ENV_FILE not found"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            clear
            print_header
            print_info "Opening MinIO console in browser..."
            echo ""
            if [ -n "$DEFAULT_BROWSER" ]; then
                $DEFAULT_BROWSER "$MINIO_CONSOLE_URL" &> /dev/null || print_error "Failed to open browser"
                print_success "MinIO console: ${MINIO_CONSOLE_URL}"
            else
                print_info "Browser not configured. Open manually: ${MINIO_CONSOLE_URL}"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            clear
            print_header
            print_info "Migrating files to MinIO..."
            echo ""
            echo "Migration options:"
            echo "  1) Dry run (preview changes)"
            echo "  2) Migrate all files"
            echo "  3) Verify migration"
            echo "  0) Cancel"
            echo ""
            echo -n "Enter choice: "
            read -n 1 -s migrate_choice
            echo ""

            case $migrate_choice in
                1)
                    print_info "Running dry run..."
                    docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py migrate_to_minio --dry-run
                    ;;
                2)
                    print_info "Migrating files..."
                    docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py migrate_to_minio
                    ;;
                3)
                    print_info "Verifying migration..."
                    docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py migrate_to_minio --verify
                    ;;
                0)
                    print_info "Migration cancelled"
                    ;;
            esac
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
            clear
            print_header
            print_info "Verifying MinIO connection..."
            echo ""
            if docker ps --format '{{.Names}}' | grep -q "$MINIO_CONTAINER"; then
                print_success "MinIO container is running"
                echo ""
                docker-compose -f "$DOCKER_COMPOSE_FILE" ps minio
            else
                print_error "MinIO container is not running"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0) return ;;
        *)
            print_error "Invalid option"
            sleep 1
            ;;
    esac
}

# Django commands
django_commands() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    echo "Django commands:"
    echo "  1) Run tests"
    echo "  2) Collect static files"
    echo "  3) Create new app"
    echo "  4) Custom manage.py command"
    echo "  5) Check for issues"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s django_choice
    echo ""

    cd "$PROJECT_ROOT"

    case $django_choice in
        1)
            clear
            print_header
            print_info "Running tests..."
            echo ""
            echo -n "Enter app name (or leave empty for all tests): "
            read test_app
            echo ""
            if [ -z "$test_app" ]; then
                docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py test
            else
                docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py test "$test_app"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            clear
            print_header
            print_info "Collecting static files..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py collectstatic --noinput
            echo ""
            print_success "Static files collected!"
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            clear
            print_header
            print_info "Creating new Django app..."
            echo ""
            echo -n "Enter app name: "
            read app_name

            if [ -z "$app_name" ]; then
                print_error "App name cannot be empty"
            else
                echo ""
                if docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py startapp "$app_name"; then
                    echo ""
                    print_success "App '$app_name' created successfully!"
                    echo ""
                    print_warning "Don't forget to:"
                    echo "  1. Add '$app_name' to INSTALLED_APPS in settings"
                    echo "  2. Create models in $app_name/models.py"
                    echo "  3. Run makemigrations and migrate"
                else
                    echo ""
                    print_error "Failed to create app"
                fi
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            clear
            print_header
            print_info "Custom Django command..."
            echo ""
            echo -n "Enter manage.py command (without 'python manage.py'): "
            read custom_cmd

            if [ -z "$custom_cmd" ]; then
                print_error "Command cannot be empty"
            else
                echo ""
                docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py $custom_cmd
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
            clear
            print_header
            print_info "Checking for issues..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py check
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0) return ;;
        *)
            print_error "Invalid option"
            sleep 1
            ;;
    esac
}

# Development tools
development_tools() {
    clear
    print_header
    echo "Development tools:"
    echo "  1) Rebuild containers"
    echo "  2) View environment variables"
    echo "  3) SSL certificate management"
    echo "  4) Docker status"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s dev_choice
    echo ""

    case $dev_choice in
        1) rebuild_containers ;;
        2) view_environment ;;
        3) ssl_management ;;
        4) docker_status ;;
        0) return ;;
        *) print_error "Invalid option" ;;
    esac
}

# Rebuild containers
rebuild_containers() {
    clear
    print_header

    if ! check_docker; then
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    echo "Rebuild options:"
    echo ""
    echo "  1) Quick rebuild (uses cache)"
    echo "  2) Force rebuild (--no-cache, fresh build)"
    echo "  3) Force rebuild + remove old images"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s rebuild_choice
    echo ""

    case $rebuild_choice in
        1)
            rebuild_quick
            ;;
        2)
            rebuild_force false
            ;;
        3)
            rebuild_force true
            ;;
        0)
            return
            ;;
        *)
            print_error "Invalid option"
            sleep 1
            ;;
    esac
}

# Quick rebuild (uses cache)
rebuild_quick() {
    clear
    print_header

    print_warning "This will rebuild containers using cached layers."
    echo ""
    read -p "Continue? (y/N): " confirm

    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "Rebuild cancelled"
        echo ""
        read -p "Press Enter to continue..."
        return 0
    fi

    print_info "Rebuilding containers..."
    echo ""

    cd "$PROJECT_ROOT"

    # Stop containers
    print_info "Step 1/3: Stopping containers..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" down

    echo ""
    print_info "Step 2/3: Building containers..."
    echo ""

    # Rebuild and start
    if docker-compose -f "$DOCKER_COMPOSE_FILE" up -d --build; then
        echo ""
        print_info "Step 3/3: Starting services..."
        echo ""
        print_success "Containers rebuilt and started successfully!"
        echo ""
        print_info "Services running:"
        echo "  • Web application: https://localhost:${WEB_PORT}"
        echo "  • MinIO console: ${MINIO_CONSOLE_URL}"
        echo ""

        # Show container status
        docker-compose -f "$DOCKER_COMPOSE_FILE" ps
    else
        echo ""
        print_error "Failed to rebuild containers"
        return 1
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# Force rebuild (--no-cache)
rebuild_force() {
    local remove_images=$1
    clear
    print_header

    print_warning "This will force rebuild ALL containers from scratch (--no-cache)."
    if [ "$remove_images" = true ]; then
        print_warning "Old images will also be removed to free disk space."
    fi
    echo ""
    read -p "Continue? (y/N): " confirm

    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "Rebuild cancelled"
        echo ""
        read -p "Press Enter to continue..."
        return 0
    fi

    print_info "Force rebuilding containers..."
    echo ""

    cd "$PROJECT_ROOT"

    # Stop containers
    print_info "Step 1/4: Stopping containers..."
    if [ "$remove_images" = true ]; then
        docker-compose -f "$DOCKER_COMPOSE_FILE" down --rmi local
        print_success "Containers stopped and old images removed"
    else
        docker-compose -f "$DOCKER_COMPOSE_FILE" down
        print_success "Containers stopped"
    fi

    echo ""
    print_info "Step 2/4: Force rebuilding images (--no-cache)..."
    echo ""

    # Build with no cache
    if docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache; then
        echo ""
        print_success "Images rebuilt successfully!"
    else
        echo ""
        print_error "Failed to rebuild images"
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi

    echo ""
    print_info "Step 3/4: Starting containers..."
    echo ""

    # Start containers
    if docker-compose -f "$DOCKER_COMPOSE_FILE" up -d; then
        echo ""
        print_info "Step 4/4: Verifying services..."
        echo ""
        print_success "All containers started successfully!"
        echo ""
        print_info "Services running:"
        echo "  • Web application: https://localhost:${WEB_PORT}"
        echo "  • MinIO console: ${MINIO_CONSOLE_URL}"
        echo ""

        # Show container status
        docker-compose -f "$DOCKER_COMPOSE_FILE" ps
    else
        echo ""
        print_error "Failed to start containers"
        return 1
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# View environment
view_environment() {
    clear
    print_header
    print_info "Environment Variables:"
    echo ""

    if [ -f "$ENV_FILE" ]; then
        # Mask sensitive values
        cat "$ENV_FILE" | sed 's/\(PASSWORD\|SECRET\|KEY\)=.*/\1=********/g'
    else
        print_error "$ENV_FILE not found"
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# SSL management
ssl_management() {
    clear
    print_header

    # Get hostname for display
    HOSTNAME=$(hostname -s)

    echo "SSL Certificate Management:"
    echo ""
    echo "  1) Generate SSL certificate"
    echo "  2) View certificate info"
    echo "  3) Regenerate and restart nginx"
    echo "  4) Trust SSL certificate (macOS)"
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s ssl_choice
    echo ""

    cd "$PROJECT_ROOT"

    case $ssl_choice in
        1)
            clear
            print_header
            print_info "Generating SSL certificate..."
            echo ""
            if [ -f "./generate-ssl-cert.sh" ]; then
                ./generate-ssl-cert.sh
            else
                print_error "generate-ssl-cert.sh not found"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            clear
            print_header
            print_info "SSL Certificate Information:"
            echo ""
            if [ -f "certs/fullchain.pem" ]; then
                echo "=== Certificate Details ==="
                openssl x509 -in certs/fullchain.pem -noout -text | grep -A 1 "Subject:"
                echo ""
                echo "=== Valid Dates ==="
                openssl x509 -in certs/fullchain.pem -noout -dates
                echo ""
                print_info "Certificate includes:"
                echo "  - localhost"
                echo "  - ${HOSTNAME}.local (network access)"
                echo "  - Local IP addresses"
            else
                print_error "Certificate not found. Run option 1 to generate."
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            clear
            print_header
            print_info "Regenerating SSL certificate and restarting nginx..."
            echo ""

            if [ -f "./generate-ssl-cert.sh" ]; then
                ./generate-ssl-cert.sh
                echo ""
                print_info "Restarting nginx container..."

                if check_docker; then
                    docker-compose -f "$DOCKER_COMPOSE_FILE" restart nginx
                    echo ""
                    print_success "SSL certificate regenerated and nginx restarted!"
                    echo ""
                    print_info "Access your application at:"
                    echo "  - https://localhost:${WEB_PORT}"
                    echo "  - https://${HOSTNAME}.local:${WEB_PORT} (network)"
                else
                    print_error "Docker is not running"
                fi
            else
                print_error "generate-ssl-cert.sh not found"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            clear
            print_header
            print_info "Trust SSL certificate in macOS Keychain..."
            echo ""

            if [ ! -f "certs/fullchain.pem" ]; then
                print_error "Certificate not found. Generate it first (option 1)."
                echo ""
                read -p "Press Enter to continue..."
                return
            fi

            print_warning "This requires administrator privileges (sudo)"
            echo ""
            print_info "Adding certificate to system keychain..."
            echo "  Certificate: ${PROJECT_ROOT}/certs/fullchain.pem"
            echo ""

            if sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain "${PROJECT_ROOT}/certs/fullchain.pem"; then
                echo ""
                print_success "Certificate added to macOS keychain successfully!"
                echo ""
                print_info "Your browser will no longer show security warnings for:"
                echo "  - https://localhost:${WEB_PORT}"
                echo "  - https://${HOSTNAME}.local:${WEB_PORT}"
                echo ""
                print_warning "Note: You may need to restart your browser for changes to take effect"
            else
                echo ""
                print_error "Failed to add certificate to keychain"
                echo ""
                print_info "You can manually add it by opening Keychain Access and dragging"
                echo "  the certificate file (certs/fullchain.pem) to the System keychain"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0)
            return
            ;;
        *)
            print_error "Invalid option"
            sleep 1
            ;;
    esac
}

# Docker status
docker_status() {
    clear
    print_header
    print_info "Docker Status:"
    echo ""

    echo "=== Docker Information ==="
    if check_docker; then
        docker --version
        docker-compose --version
        echo ""
        print_success "Docker is running"
    else
        print_error "Docker is not running"
    fi
    echo ""

    echo "=== Application Containers ==="
    cd "$PROJECT_ROOT"
    docker-compose -f "$DOCKER_COMPOSE_FILE" ps
    echo ""

    echo "=== Resource Usage ==="
    docker stats --no-stream $(docker-compose -f "$DOCKER_COMPOSE_FILE" ps -q) 2>/dev/null || print_warning "No running containers"
    echo ""

    read -p "Press Enter to continue..."
}

# Open browser
open_browser() {
    clear
    print_header

    # Get network IP and hostname
    NETWORK_IP=$(get_network_ip)
    HOSTNAME=$(hostname -s)

    print_info "Open application in browser:"
    echo ""
    echo "Available URLs:"
    echo "  1) https://localhost:${WEB_PORT}"
    echo "  2) https://127.0.0.1:${WEB_PORT}"
    echo "  3) https://${NETWORK_IP}:${WEB_PORT} (network IP)"
    echo "  4) https://${HOSTNAME}.local:${WEB_PORT} (network .local domain)"
    echo ""
    echo "  0) Back"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s browser_choice
    echo ""

    local url=""

    case $browser_choice in
        1)
            url="https://localhost:${WEB_PORT}"
            ;;
        2)
            url="https://127.0.0.1:${WEB_PORT}"
            ;;
        3)
            url="https://${NETWORK_IP}:${WEB_PORT}"
            ;;
        4)
            url="https://${HOSTNAME}.local:${WEB_PORT}"
            ;;
        0)
            return
            ;;
        *)
            print_error "Invalid option"
            sleep 1
            return
            ;;
    esac

    echo ""
    print_info "Opening: $url"
    echo ""

    if [ -z "$DEFAULT_BROWSER" ]; then
        print_warning "No browser configured in manage.config.sh"
        print_info "Set DEFAULT_BROWSER (e.g., 'open', 'google-chrome', 'firefox')"
        echo ""
        print_info "You can manually open: $url"
    else
        if $DEFAULT_BROWSER "$url" &> /dev/null; then
            print_success "Browser opened successfully!"
            echo ""
            print_info "URL: $url"
            echo ""
            print_warning "Note: You may see a security warning about self-signed certificate"
            echo "  - This is normal for local development"
            echo "  - Click 'Advanced' or 'Accept Risk' to continue"
        else
            print_error "Failed to open browser"
            echo ""
            print_info "Try opening manually: $url"
        fi
    fi

    echo ""
    read -p "Press Enter to continue..."
}

# Main loop
main() {
    while true; do
        show_menu
        read -n 1 -s choice
        echo ""  # Print newline after single char input

        case $choice in
            1) start_application ;;
            2) stop_application ;;
            3) restart_application ;;
            4) view_logs ;;
            5) shell_access ;;
            6) database_management ;;
            7) minio_management ;;
            8) django_commands ;;
            9) development_tools ;;
            a|A) open_browser ;;
            0)
                clear
                print_success "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option"
                sleep 1
                ;;
        esac
    done
}

# Run main function
main
