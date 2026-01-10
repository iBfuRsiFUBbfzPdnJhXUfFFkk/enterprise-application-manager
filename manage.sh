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

    # Ensure data directory exists
    mkdir -p data

    # Ensure db.sqlite3 is a file, not a directory
    if [ -d "$DB_FILE" ]; then
        print_warning "Database path exists as directory. Removing..."
        rm -rf "$DB_FILE"
    fi

    # Create empty database file if it doesn't exist
    if [ ! -f "$DB_FILE" ]; then
        touch "$DB_FILE"
        print_info "Created empty database file"
        echo ""
    fi

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
    echo "  q) Exit script"
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
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
            ;;
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
    echo "  q) Exit script"
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
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
            ;;
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
    echo "  q) Exit script"
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
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
            ;;
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
    echo "  4) Verify MinIO connection"
    echo "  0) Back"
    echo "  q) Exit script"
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

            # Use Django management command to create bucket
            if docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py check_minio_bucket --create-if-missing; then
                echo ""
                print_success "MinIO bucket created/verified successfully!"
            else
                echo ""
                print_error "Failed to create MinIO bucket"
                print_info "Make sure MinIO container is running and credentials are correct"
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
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
            ;;
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
    echo "  3) Rebuild Tailwind CSS (in container - auto-builds on startup)"
    echo "  4) Rebuild Tailwind CSS and collect static"
    echo "  5) Create new app"
    echo "  6) Custom manage.py command"
    echo "  7) Check for issues"
    echo "  0) Back"
    echo "  q) Exit script"
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
            print_info "Rebuilding Tailwind CSS..."
            echo ""
            if docker-compose -f "$DOCKER_COMPOSE_FILE" exec web npm run build:css; then
                echo ""
                print_success "Tailwind CSS rebuilt successfully!"
                echo ""
                print_info "Tailwind CSS output: static/css/tailwind.css"
            else
                echo ""
                print_error "Failed to rebuild Tailwind CSS"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            clear
            print_header
            print_info "Rebuilding Tailwind CSS and collecting static files..."
            echo ""

            print_info "Step 1/2: Building Tailwind CSS..."
            if docker-compose -f "$DOCKER_COMPOSE_FILE" exec web npm run build:css; then
                echo ""
                print_success "Tailwind CSS built successfully!"
                echo ""
                print_info "Step 2/2: Collecting static files..."
                if docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py collectstatic --noinput; then
                    echo ""
                    print_success "All static files ready!"
                    echo ""
                    print_info "Files collected to: staticfiles/"
                else
                    echo ""
                    print_error "Failed to collect static files"
                fi
            else
                echo ""
                print_error "Failed to build Tailwind CSS"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
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
        6)
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
        7)
            clear
            print_header
            print_info "Checking for issues..."
            echo ""
            docker-compose -f "$DOCKER_COMPOSE_FILE" exec web python manage.py check
            echo ""
            read -p "Press Enter to continue..."
            ;;
        0) return ;;
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
            ;;
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
    echo "  5) Fix line endings"
    echo "  6) Initialize environment configuration"
    echo "  0) Back"
    echo "  q) Exit script"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s dev_choice
    echo ""

    case $dev_choice in
        1) rebuild_containers ;;
        2) view_environment ;;
        3) ssl_management ;;
        4) docker_status ;;
        5) fix_line_endings ;;
        6) initialize_environment_config ;;
        0) return ;;
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
            ;;
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
    echo "  q) Exit script"
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
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
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

# Generate SSL certificate
generate_ssl_certificate() {
    local CERTS_DIR="${PROJECT_ROOT}/certs"

    print_header
    print_info "Generating SSL certificate..."
    echo ""

    # Create certs directory if it doesn't exist
    mkdir -p "$CERTS_DIR"

    # Get hostname and IP address
    local HOSTNAME=$(hostname -s | tr '[:upper:]' '[:lower:]')
    local LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "")

    echo "Detected system:"
    echo "  Hostname: ${HOSTNAME}"
    if [ -n "$LOCAL_IP" ]; then
        echo "  Local IP: ${LOCAL_IP}"
    fi
    echo ""

    # Create OpenSSL configuration file with Subject Alternative Names
    cat > "${CERTS_DIR}/openssl.cnf" <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=US
ST=Development
L=Local
O=Enterprise Application Manager
OU=Development
CN=localhost

[v3_req]
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = ${HOSTNAME}
DNS.3 = ${HOSTNAME}.local
DNS.4 = *.${HOSTNAME}.local
IP.1 = 127.0.0.1
IP.2 = ::1
EOF

    # Add local IP if detected
    if [ -n "$LOCAL_IP" ]; then
        echo "IP.3 = ${LOCAL_IP}" >> "${CERTS_DIR}/openssl.cnf"
    fi

    # Generate private key
    print_info "Generating private key..."
    if ! openssl genrsa -out "${CERTS_DIR}/privkey.pem" 2048 2>&1 | grep -v "^Generating"; then
        print_error "Failed to generate private key"
        return 1
    fi

    # Generate certificate signing request
    print_info "Generating certificate signing request..."
    if ! openssl req -new -key "${CERTS_DIR}/privkey.pem" \
        -out "${CERTS_DIR}/cert.csr" \
        -config "${CERTS_DIR}/openssl.cnf" 2>&1 | grep -v "^..*"; then
        print_error "Failed to generate certificate signing request"
        return 1
    fi

    # Generate self-signed certificate (valid for 365 days)
    print_info "Generating self-signed certificate (valid for 365 days)..."
    if ! openssl x509 -req -days 365 \
        -in "${CERTS_DIR}/cert.csr" \
        -signkey "${CERTS_DIR}/privkey.pem" \
        -out "${CERTS_DIR}/fullchain.pem" \
        -extensions v3_req \
        -extfile "${CERTS_DIR}/openssl.cnf" 2>&1 | grep -v "^..*"; then
        print_error "Failed to generate self-signed certificate"
        rm -f "${CERTS_DIR}/cert.csr"
        return 1
    fi

    # Clean up CSR
    rm -f "${CERTS_DIR}/cert.csr"

    # Set permissions
    chmod 600 "${CERTS_DIR}/privkey.pem" 2>/dev/null || true
    chmod 644 "${CERTS_DIR}/fullchain.pem" 2>/dev/null || true

    echo ""
    print_success "SSL certificate generated successfully!"
    echo ""
    echo "Certificate files:"
    echo "  Private key: ${CERTS_DIR}/privkey.pem"
    echo "  Certificate: ${CERTS_DIR}/fullchain.pem"
    echo ""
    echo "Certificate includes:"
    echo "  - localhost"
    echo "  - 127.0.0.1"
    echo "  - ${HOSTNAME}"
    echo "  - ${HOSTNAME}.local"
    if [ -n "$LOCAL_IP" ]; then
        echo "  - ${LOCAL_IP}"
    fi
    echo ""
    print_warning "Note: This is a self-signed certificate for development only."
    echo "      Browsers will show a security warning. Click 'Advanced' and 'Proceed'."
    echo ""

    return 0
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
    echo "  q) Exit script"
    echo ""
    echo -n "Enter choice: "
    read -n 1 -s ssl_choice
    echo ""

    cd "$PROJECT_ROOT"

    case $ssl_choice in
        1)
            clear
            generate_ssl_certificate
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

            generate_ssl_certificate
            cert_exit=$?

            if [ $cert_exit -eq 0 ]; then
                echo ""
                print_info "Restarting nginx container..."

                if check_docker; then
                    docker-compose -f "$DOCKER_COMPOSE_FILE" restart nginx
                    if [ $? -eq 0 ]; then
                        echo ""
                        print_success "SSL certificate regenerated and nginx restarted!"
                        echo ""
                        print_info "Access your application at:"
                        echo "  - https://localhost:${WEB_PORT}"
                        echo "  - https://${HOSTNAME}.local:${WEB_PORT} (network)"
                    else
                        echo ""
                        print_error "Failed to restart nginx"
                    fi
                else
                    print_error "Docker is not running"
                fi
            else
                echo ""
                print_error "Certificate generation failed"
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
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
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

# Fix line endings
fix_line_endings() {
    clear
    print_header
    print_info "Fix Line Endings for Docker Compatibility"
    echo ""
    print_warning "This will renormalize all files according to .gitattributes"
    echo ""
    echo "Line ending rules:"
    echo "  • Shell scripts (.sh) -> LF (Unix)"
    echo "  • Docker files -> LF (Unix)"
    echo "  • PowerShell scripts (.ps1) -> CRLF (Windows)"
    echo ""
    read -p "Continue? (y/N): " confirm

    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "Operation cancelled"
        echo ""
        read -p "Press Enter to continue..."
        return
    fi

    echo ""
    print_info "Step 1/3: Removing files from git index..."
    git rm --cached -r . >/dev/null 2>&1

    print_info "Step 2/3: Resetting git index..."
    git reset --hard >/dev/null 2>&1

    print_info "Step 3/3: Renormalizing line endings..."
    git add --renormalize . >/dev/null 2>&1

    echo ""
    print_success "Line endings fixed!"
    echo ""

    # Check if there are any changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "The following files were normalized:"
        echo ""
        git status --short
        echo ""
        print_info "You should commit these changes with:"
        echo "  git commit -m 'chore: normalize line endings'"
    else
        print_success "No files needed normalization."
    fi

    echo ""
    print_info "Rebuild Docker containers to apply changes:"
    echo "  docker compose down"
    echo "  docker compose up --build"
    echo ""
    read -p "Press Enter to continue..."
}

# Initialize environment configuration
initialize_environment_config() {
    clear
    print_header
    print_info "Initialize Environment Configuration (.env)"
    echo ""

    local env_path="${PROJECT_ROOT}/${ENV_FILE}"
    local temp_env=""

    # Helper function to get existing value from .env file
    get_env_value() {
        local key="$1"
        local default="$2"
        if [ -f "$temp_env" ]; then
            local value=$(grep "^${key}=" "$temp_env" 2>/dev/null | cut -d'=' -f2-)
            # Strip ALL surrounding quotes (both single and double) to prevent double-quoting
            # Loop to remove multiple layers of quotes
            while [[ $value =~ ^\"(.*)\"$ ]] || [[ $value =~ ^\'(.*)\'$ ]]; do
                value="${BASH_REMATCH[1]}"
            done
            echo "${value:-$default}"
        else
            echo "$default"
        fi
    }

    # Read existing .env file if it exists
    if [ -f "$env_path" ]; then
        print_info "Reading existing .env file..."
        # Create temporary copy for reading
        temp_env="${env_path}.tmp"
        cp "$env_path" "$temp_env"
        echo ""
        print_warning "Existing .env file will be backed up and replaced with normalized version"
        echo ""
        read -p "Continue? (y/N): " confirm

        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            [ -f "$temp_env" ] && rm -f "$temp_env"
            print_info "Operation cancelled"
            echo ""
            read -p "Press Enter to continue..."
            return
        fi

        # Backup existing .env
        local backup_path="${env_path}.backup-$(date +%Y%m%d-%H%M%S)"
        cp "$env_path" "$backup_path"
        print_info "Backed up to: $backup_path"
    fi

    print_info "Generating random secrets..."
    echo ""

    # Generate random values for secrets
    local existing_django=$(get_env_value "DJANGO_SECRET_KEY" "")
    local django_secret="${existing_django:-$(openssl rand -base64 50 | tr -d '\n' | tr '+/' 'Az')}"

    local existing_encryption=$(get_env_value "ENCRYPTION_SECRET" "")
    local encryption_secret="${existing_encryption:-$(openssl rand -base64 32 | tr -d '\n')}"

    local minio_suffix=$(openssl rand -hex 8)
    local existing_minio_user=$(get_env_value "MINIO_ROOT_USER" "")
    local minio_user="${existing_minio_user:-admin-${minio_suffix}}"

    local existing_minio_pass=$(get_env_value "MINIO_ROOT_PASSWORD" "")
    local minio_password="${existing_minio_pass:-$(openssl rand -base64 32 | tr '+/' 'xy')}"

    # Get hostname for network access
    local hostname=$(hostname -s | tr '[:upper:]' '[:lower:]')

    # Build .env content with all sections
    cat > "$env_path" << EOF
# Django Settings
# IMPORTANT: In .env files, escape \$ with \$\$ and % with %%
# Example: "my-key\$123" becomes "my-key\$\$123"
DJANGO_SECRET_KEY="${django_secret}"
DEBUG=$(get_env_value "DEBUG" "True")

# Allowed Hosts - Add your hostname/domain for network access
# JSON array format - add your machine's hostname.local for mDNS access
# Example: ["127.0.0.1","0.0.0.0","localhost","${hostname}.local"]
ALLOWED_HOSTS=$(get_env_value "ALLOWED_HOSTS" '["127.0.0.1","0.0.0.0","localhost"]')

# Database (SQLite)
# Currently using db.sqlite3 in project root (data/db.sqlite3 in Docker)

# LDAP Configuration (if enabled)
SHOULD_USE_LDAP=$(get_env_value "SHOULD_USE_LDAP" "False")
AUTH_LDAP_SERVER_URI="$(get_env_value "AUTH_LDAP_SERVER_URI" "ldap://ldap.example.com")"
AUTH_LDAP_BIND_DN="$(get_env_value "AUTH_LDAP_BIND_DN" "domain\\\\username")"
AUTH_LDAP_BIND_PASSWORD="$(get_env_value "AUTH_LDAP_BIND_PASSWORD" "password")"
AUTH_LDAP_SEARCH_BASE="$(get_env_value "AUTH_LDAP_SEARCH_BASE" "dc=example,dc=com")"
AUTH_LDAP_SEARCH_FILTER="$(get_env_value "AUTH_LDAP_SEARCH_FILTER" "(sAMAccountName=%(user)s)")"
AUTH_LDAP_USER_ATTR_MAP=$(get_env_value "AUTH_LDAP_USER_ATTR_MAP" '{"first_name": "givenName", "last_name": "sn", "email": "mail"}')

# Email Configuration
EMAIL_HOST="$(get_env_value "EMAIL_HOST" "localhost")"
EMAIL_PORT=$(get_env_value "EMAIL_PORT" "25")
EMAIL_USE_TLS=$(get_env_value "EMAIL_USE_TLS" "False")
EMAIL_USE_SSL=$(get_env_value "EMAIL_USE_SSL" "False")
EMAIL_FROM="$(get_env_value "EMAIL_FROM" "noreply@example.com")"

# Encryption
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_SECRET="${encryption_secret}"

# MinIO Object Storage
MINIO_ROOT_USER=${minio_user}
MINIO_ROOT_PASSWORD=${minio_password}
MINIO_ENDPOINT=$(get_env_value "MINIO_ENDPOINT" "minio:9000")
MINIO_ACCESS_KEY=${minio_user}
MINIO_SECRET_KEY=${minio_password}
MINIO_BUCKET_NAME=$(get_env_value "MINIO_BUCKET_NAME" "enterprise-app-media")
MINIO_USE_SSL=$(get_env_value "MINIO_USE_SSL" "false")
USE_MINIO=$(get_env_value "USE_MINIO" "true")

# Public domain for file URLs (used to generate accessible URLs for MinIO files)
# Set this to your machine's hostname and port for network access
# Auto-detected: ${hostname}.local:50478
PUBLIC_DOMAIN=$(get_env_value "PUBLIC_DOMAIN" "${hostname}.local:50478")

# CSRF Trusted Origins (for HTTPS network access)
# Required when accessing via HTTPS with custom hostname/port
# Comma-separated list of full URLs including protocol, hostname, and port
# Example: https://${hostname}.local:50478
CSRF_TRUSTED_ORIGINS_EXTRA=$(get_env_value "CSRF_TRUSTED_ORIGINS_EXTRA" "")

# WebAuthn / Passkey Configuration
WEBAUTHN_ENABLED=$(get_env_value "WEBAUTHN_ENABLED" "True")
WEBAUTHN_RP_NAME="$(get_env_value "WEBAUTHN_RP_NAME" "Enterprise Application Manager")"
WEBAUTHN_RP_ID=$(get_env_value "WEBAUTHN_RP_ID" "localhost")
WEBAUTHN_ORIGIN=$(get_env_value "WEBAUTHN_ORIGIN" "http://localhost:8000")
EOF

    # Clean up temp file
    [ -f "$temp_env" ] && rm -f "$temp_env"

    print_success "Environment configuration initialized!"
    echo ""
    print_info "Generated new secrets:"
    [ -z "$existing_django" ] && echo "  Django Secret: ${django_secret}"
    [ -z "$existing_encryption" ] && echo "  Encryption Secret: ${encryption_secret}"
    if [ -z "$existing_minio_user" ]; then
        echo "  MinIO User: ${minio_user}"
        echo "  MinIO Password: ${minio_password}"
    fi
    echo ""
    print_info "Existing values were preserved"
    echo ""
    print_warning "Review $env_path and update values as needed"
    echo ""
    print_info "Restart Docker to apply changes:"
    echo "  docker compose down"
    echo "  docker compose up -d"
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
    echo "  q) Exit script"
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
        q|Q)
            clear
            print_success "Goodbye!"
            exit 0
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
