# Enterprise Application Manager - Interactive Management Script (PowerShell)
# A general-purpose interactive shell for managing the application

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigFile = Join-Path $ScriptDir "manage.config.ps1"
$ConfigExample = Join-Path $ScriptDir "manage.config.example.ps1"

# Load configuration
if (Test-Path $ConfigFile) {
    . $ConfigFile
} elseif (Test-Path $ConfigExample) {
    Write-Host "⚠ Configuration file not found. Creating from example..." -ForegroundColor Yellow
    Copy-Item $ConfigExample $ConfigFile
    . $ConfigFile
    Write-Host "✓ Created manage.config.ps1 - you can customize it for your environment" -ForegroundColor Green
    Write-Host ""
    Start-Sleep -Seconds 2
} else {
    Write-Host "✗ Error: Neither manage.config.ps1 nor manage.config.example.ps1 found!" -ForegroundColor Red
    exit 1
}

# Helper functions
function Print-Header {
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "  $AppName - Management" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
}

function Print-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Print-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Print-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Print-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

# Check if Docker is required and running
function Test-Docker {
    $dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
    if (-not $dockerCmd) {
        Print-Error "Docker is not installed"
        return $false
    }

    try {
        $null = docker info 2>&1
        if ($LASTEXITCODE -ne 0) {
            Print-Error "Docker is not running. Please start Docker Desktop."
            return $false
        }
    } catch {
        Print-Error "Docker is not running. Please start Docker Desktop."
        return $false
    }

    return $true
}

# Get local network IP address
function Get-NetworkIP {
    try {
        $ip = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*", "Wi-Fi*" -ErrorAction SilentlyContinue |
              Where-Object { $_.IPAddress -notlike "169.254.*" -and $_.IPAddress -ne "127.0.0.1" } |
              Select-Object -First 1 -ExpandProperty IPAddress

        if ($ip) {
            return $ip
        }
    } catch {
        # Fallback to localhost
    }

    return "127.0.0.1"
}

# Main menu
function Show-Menu {
    Clear-Host
    Print-Header
    Write-Host "Select an option:"
    Write-Host ""
    Write-Host "  1) Start application (Docker)"
    Write-Host "  2) Stop application"
    Write-Host "  3) Restart application"
    Write-Host "  4) View logs"
    Write-Host "  5) Shell access"
    Write-Host "  6) Database management"
    Write-Host "  7) MinIO management"
    Write-Host "  8) Django commands"
    Write-Host "  9) Development tools"
    Write-Host "  a) Open in browser"
    Write-Host ""
    Write-Host "  0) Exit"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "
}

# Start application
function Start-Application {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Print-Info "Starting application..."
    Write-Host ""

    # Change to project directory
    Push-Location $ProjectRoot

    try {
        # Ensure data directory exists
        $dataDir = Join-Path $ProjectRoot "data"
        if (-not (Test-Path $dataDir)) {
            New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
            Print-Info "Created data directory"
        }

        # Ensure db.sqlite3 is a file, not a directory
        $dbPath = Join-Path $ProjectRoot $DbFile
        if (Test-Path $dbPath -PathType Container) {
            Print-Warning "Database path exists as directory. Removing..."
            Remove-Item $dbPath -Force -Recurse
        }

        # Create empty database file if it doesn't exist
        if (-not (Test-Path $dbPath)) {
            New-Item -ItemType File -Path $dbPath -Force | Out-Null
            Print-Info "Created empty database file"
        }

        # Start docker-compose
        $composeFile = Join-Path $ProjectRoot $DockerComposeFile
        docker-compose -f $composeFile up -d

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Print-Success "Application started successfully!"
            Write-Host ""
            Print-Info "Services running:"
            Write-Host "  • Web application: https://localhost:$WebPort"
            Write-Host "  • MinIO console: $MinioConsoleUrl"
            Write-Host ""
            Print-Warning "Note: HTTPS uses self-signed certificate - accept security warning in browser"
            Write-Host ""
            Print-Info "Use option 4 to view logs or option 'a' to open in browser"

            # Show container status
            Write-Host ""
            docker-compose -f $composeFile ps
        } else {
            Write-Host ""
            Print-Error "Failed to start application"
        }
    } finally {
        Pop-Location
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Stop application
function Stop-Application {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Print-Info "Stopping application..."
    Write-Host ""

    Push-Location $ProjectRoot

    try {
        $composeFile = Join-Path $ProjectRoot $DockerComposeFile
        docker-compose -f $composeFile down

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Print-Success "Application stopped successfully!"
        } else {
            Write-Host ""
            Print-Error "Failed to stop application"
        }
    } finally {
        Pop-Location
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Restart application
function Restart-Application {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Print-Info "Restarting application..."
    Write-Host ""

    Push-Location $ProjectRoot

    try {
        $composeFile = Join-Path $ProjectRoot $DockerComposeFile
        docker-compose -f $composeFile restart

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Print-Success "Application restarted successfully!"
            Write-Host ""
            Print-Info "Services running:"
            Write-Host "  • Web application: https://localhost:$WebPort"
            Write-Host "  • MinIO console: $MinioConsoleUrl"
            Write-Host ""

            # Show container status
            docker-compose -f $composeFile ps
        } else {
            Write-Host ""
            Print-Error "Failed to restart application"
        }
    } finally {
        Pop-Location
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
}

# View logs
function Show-Logs {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host "Log options:"
    Write-Host "  1) Web application logs (follow)"
    Write-Host "  2) MinIO logs (follow)"
    Write-Host "  3) nginx logs (follow)"
    Write-Host "  4) All logs (follow)"
    Write-Host "  5) Web application logs (last $LogTailLines lines)"
    Write-Host "  6) MinIO logs (last $LogTailLines lines)"
    Write-Host "  7) nginx logs (last $LogTailLines lines)"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $logChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile

    try {
        switch ($logChoice) {
            '1' {
                Clear-Host
                Print-Info "Following web application logs (Ctrl+C to exit)..."
                Write-Host ""
                docker-compose -f $composeFile logs -f web
            }
            '2' {
                Clear-Host
                Print-Info "Following MinIO logs (Ctrl+C to exit)..."
                Write-Host ""
                docker-compose -f $composeFile logs -f minio
            }
            '3' {
                Clear-Host
                Print-Info "Following nginx logs (Ctrl+C to exit)..."
                Write-Host ""
                docker-compose -f $composeFile logs -f nginx
            }
            '4' {
                Clear-Host
                Print-Info "Following all logs (Ctrl+C to exit)..."
                Write-Host ""
                docker-compose -f $composeFile logs -f
            }
            '5' {
                Clear-Host
                Print-Info "Web application logs (last $LogTailLines lines)..."
                Write-Host ""
                docker-compose -f $composeFile logs --tail=$LogTailLines web
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '6' {
                Clear-Host
                Print-Info "MinIO logs (last $LogTailLines lines)..."
                Write-Host ""
                docker-compose -f $composeFile logs --tail=$LogTailLines minio
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '7' {
                Clear-Host
                Print-Info "nginx logs (last $LogTailLines lines)..."
                Write-Host ""
                docker-compose -f $composeFile logs --tail=$LogTailLines nginx
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '0' { return }
            default {
                Print-Error "Invalid option"
                Start-Sleep -Seconds 1
            }
        }
    } finally {
        Pop-Location
    }
}

# Shell access
function Show-ShellAccess {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host "Shell options:"
    Write-Host "  1) Django shell (Python)"
    Write-Host "  2) Container bash shell (web)"
    Write-Host "  3) Container shell (minio)"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $shellChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile

    try {
        switch ($shellChoice) {
            '1' {
                Clear-Host
                Print-Info "Opening Django shell... (exit() to quit)"
                Write-Host ""
                docker-compose -f $composeFile exec web python manage.py shell
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '2' {
                Clear-Host
                Print-Info "Opening container bash shell... (exit to quit)"
                Write-Host ""
                docker-compose -f $composeFile exec web bash
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '3' {
                Clear-Host
                Print-Info "Opening MinIO container shell... (exit to quit)"
                Write-Host ""
                docker-compose -f $composeFile exec minio sh
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '0' { return }
            default {
                Print-Error "Invalid option"
                Start-Sleep -Seconds 1
            }
        }
    } finally {
        Pop-Location
    }
}

# Database management
function Show-DatabaseManagement {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host "Database options:"
    Write-Host "  1) Run migrations"
    Write-Host "  2) Create migrations"
    Write-Host "  3) Create superuser"
    Write-Host "  4) Reset database"
    Write-Host "  5) Show migrations status"
    Write-Host "  6) Backup database"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $dbChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile

    try {
        switch ($dbChoice) {
            '1' {
                Clear-Host
                Print-Header
                Print-Info "Running migrations..."
                Write-Host ""
                docker-compose -f $composeFile exec web python manage.py migrate

                if ($LASTEXITCODE -eq 0) {
                    Write-Host ""
                    Print-Success "Migrations completed successfully!"
                } else {
                    Write-Host ""
                    Print-Error "Failed to run migrations"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '2' {
                Clear-Host
                Print-Header
                Print-Info "Creating migrations..."
                Write-Host ""
                $appName = Read-Host "Enter app name (or leave empty for all apps)"
                Write-Host ""

                if ([string]::IsNullOrWhiteSpace($appName)) {
                    docker-compose -f $composeFile exec web python manage.py makemigrations
                } else {
                    docker-compose -f $composeFile exec web python manage.py makemigrations $appName
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '3' {
                Clear-Host
                Print-Header
                Print-Info "Creating superuser..."
                Write-Host ""
                docker-compose -f $composeFile exec web python manage.py createsuperuser
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '4' {
                Clear-Host
                Print-Header
                Print-Warning "WARNING: This will delete all data in the database!"
                Write-Host ""
                $confirm = Read-Host "Are you sure? Type 'yes' to confirm"

                if ($confirm -eq "yes") {
                    Print-Info "Resetting database..."
                    Write-Host ""

                    # Stop containers
                    docker-compose -f $composeFile down

                    # Remove database file
                    $dbPath = Join-Path $ProjectRoot $DbFile
                    if (Test-Path $dbPath) {
                        Remove-Item $dbPath -Force
                        Print-Success "Database file removed"
                    }

                    # Restart containers
                    docker-compose -f $composeFile up -d

                    # Run migrations
                    Write-Host ""
                    Print-Info "Running migrations..."
                    Start-Sleep -Seconds 3  # Wait for containers to start
                    docker-compose -f $composeFile exec web python manage.py migrate

                    Write-Host ""
                    Print-Success "Database reset complete!"
                } else {
                    Print-Info "Database reset cancelled"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '5' {
                Clear-Host
                Print-Header
                Print-Info "Migrations status:"
                Write-Host ""
                docker-compose -f $composeFile exec web python manage.py showmigrations
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '6' {
                Clear-Host
                Print-Header
                $backupDir = Join-Path $BackupRoot $DbBackupDir
                if (-not (Test-Path $backupDir)) {
                    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
                }

                $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
                $backupFile = Join-Path $backupDir "db_backup_${timestamp}.sqlite3"
                Print-Info "Backing up database..."
                Write-Host ""

                $dbPath = Join-Path $ProjectRoot $DbFile
                if (Test-Path $dbPath) {
                    Copy-Item $dbPath $backupFile
                    Print-Success "Database backed up to: $backupFile"
                } else {
                    Print-Error "Database file not found: $dbPath"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '0' { return }
            default {
                Print-Error "Invalid option"
                Start-Sleep -Seconds 1
            }
        }
    } finally {
        Pop-Location
    }
}

# MinIO management
function Show-MinioManagement {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host "MinIO options:"
    Write-Host "  1) Create bucket"
    Write-Host "  2) Show credentials"
    Write-Host "  3) Open MinIO console in browser"
    Write-Host "  4) Migrate files to MinIO"
    Write-Host "  5) Verify MinIO connection"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $minioChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile

    try {
        switch ($minioChoice) {
            '1' {
                Clear-Host
                Print-Header
                Print-Info "Creating MinIO bucket..."
                Write-Host ""

                $bucketScript = Join-Path $ProjectRoot "minio-create-bucket"
                if (Test-Path $bucketScript) {
                    & $bucketScript
                } else {
                    Print-Error "minio-create-bucket script not found"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '2' {
                Clear-Host
                Print-Header
                Print-Info "MinIO Credentials:"
                Write-Host ""

                $envPath = Join-Path $ProjectRoot $EnvFile
                if (Test-Path $envPath) {
                    Write-Host "Console URL: $MinioConsoleUrl"
                    Write-Host ""

                    $envContent = Get-Content $envPath
                    $minioUser = $envContent | Where-Object { $_ -match "^MINIO_ROOT_USER=" }
                    $minioPass = $envContent | Where-Object { $_ -match "^MINIO_ROOT_PASSWORD=" }

                    if ($minioUser) { Write-Host $minioUser } else { Write-Host "MINIO_ROOT_USER not set" }
                    if ($minioPass) { Write-Host $minioPass } else { Write-Host "MINIO_ROOT_PASSWORD not set" }

                    Write-Host ""
                    Print-Info "Access MinIO console at: $MinioConsoleUrl"
                } else {
                    Print-Error "$EnvFile not found"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '3' {
                Clear-Host
                Print-Header
                Print-Info "Opening MinIO console in browser..."
                Write-Host ""

                try {
                    Start-Process $MinioConsoleUrl
                    Print-Success "MinIO console: $MinioConsoleUrl"
                } catch {
                    Print-Error "Failed to open browser"
                    Print-Info "Please open manually: $MinioConsoleUrl"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '4' {
                Clear-Host
                Print-Header
                Print-Info "Migrating files to MinIO..."
                Write-Host ""
                Write-Host "Migration options:"
                Write-Host "  1) Dry run (preview changes)"
                Write-Host "  2) Migrate all files"
                Write-Host "  3) Verify migration"
                Write-Host "  0) Cancel"
                Write-Host ""
                Write-Host -NoNewline "Enter choice: "

                $migrateChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
                Write-Host ""

                switch ($migrateChoice) {
                    '1' {
                        Print-Info "Running dry run..."
                        docker-compose -f $composeFile exec web python manage.py migrate_to_minio --dry-run
                    }
                    '2' {
                        Print-Info "Migrating files..."
                        docker-compose -f $composeFile exec web python manage.py migrate_to_minio
                    }
                    '3' {
                        Print-Info "Verifying migration..."
                        docker-compose -f $composeFile exec web python manage.py migrate_to_minio --verify
                    }
                    '0' {
                        Print-Info "Migration cancelled"
                    }
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '5' {
                Clear-Host
                Print-Header
                Print-Info "Verifying MinIO connection..."
                Write-Host ""

                $containers = docker ps --format "{{.Names}}"
                if ($containers -match $MinioContainer) {
                    Print-Success "MinIO container is running"
                    Write-Host ""
                    docker-compose -f $composeFile ps minio
                } else {
                    Print-Error "MinIO container is not running"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '0' { return }
            default {
                Print-Error "Invalid option"
                Start-Sleep -Seconds 1
            }
        }
    } finally {
        Pop-Location
    }
}

# Django commands
function Show-DjangoCommands {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host "Django commands:"
    Write-Host "  1) Run tests"
    Write-Host "  2) Collect static files"
    Write-Host "  3) Create new app"
    Write-Host "  4) Custom manage.py command"
    Write-Host "  5) Check for issues"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $djangoChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile

    try {
        switch ($djangoChoice) {
            '1' {
                Clear-Host
                Print-Header
                Print-Info "Running tests..."
                Write-Host ""
                $testApp = Read-Host "Enter app name (or leave empty for all tests)"
                Write-Host ""

                if ([string]::IsNullOrWhiteSpace($testApp)) {
                    docker-compose -f $composeFile exec web python manage.py test
                } else {
                    docker-compose -f $composeFile exec web python manage.py test $testApp
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '2' {
                Clear-Host
                Print-Header
                Print-Info "Collecting static files..."
                Write-Host ""
                docker-compose -f $composeFile exec web python manage.py collectstatic --noinput
                Write-Host ""
                Print-Success "Static files collected!"
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '3' {
                Clear-Host
                Print-Header
                Print-Info "Creating new Django app..."
                Write-Host ""
                $appName = Read-Host "Enter app name"

                if ([string]::IsNullOrWhiteSpace($appName)) {
                    Print-Error "App name cannot be empty"
                } else {
                    Write-Host ""
                    docker-compose -f $composeFile exec web python manage.py startapp $appName

                    if ($LASTEXITCODE -eq 0) {
                        Write-Host ""
                        Print-Success "App '$appName' created successfully!"
                        Write-Host ""
                        Print-Warning "Don't forget to:"
                        Write-Host "  1. Add '$appName' to INSTALLED_APPS in settings"
                        Write-Host "  2. Create models in $appName\models.py"
                        Write-Host "  3. Run makemigrations and migrate"
                    } else {
                        Write-Host ""
                        Print-Error "Failed to create app"
                    }
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '4' {
                Clear-Host
                Print-Header
                Print-Info "Custom Django command..."
                Write-Host ""
                $customCmd = Read-Host "Enter manage.py command (without 'python manage.py')"

                if ([string]::IsNullOrWhiteSpace($customCmd)) {
                    Print-Error "Command cannot be empty"
                } else {
                    Write-Host ""
                    docker-compose -f $composeFile exec web python manage.py $customCmd
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '5' {
                Clear-Host
                Print-Header
                Print-Info "Checking for issues..."
                Write-Host ""
                docker-compose -f $composeFile exec web python manage.py check
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '0' { return }
            default {
                Print-Error "Invalid option"
                Start-Sleep -Seconds 1
            }
        }
    } finally {
        Pop-Location
    }
}

# Development tools
function Show-DevelopmentTools {
    Clear-Host
    Print-Header
    Write-Host "Development tools:"
    Write-Host "  1) Rebuild containers"
    Write-Host "  2) View environment variables"
    Write-Host "  3) SSL certificate management"
    Write-Host "  4) Docker status"
    Write-Host "  5) Fix line endings"
    Write-Host "  6) Initialize environment configuration"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $devChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    switch ($devChoice) {
        '1' { Show-RebuildContainers }
        '2' { Show-Environment }
        '3' { Show-SslManagement }
        '4' { Show-DockerStatus }
        '5' { Fix-LineEndings }
        '6' { Initialize-EnvironmentConfig }
        '0' { return }
        default { Print-Error "Invalid option" }
    }
}

# Rebuild containers
function Show-RebuildContainers {
    Clear-Host
    Print-Header

    if (-not (Test-Docker)) {
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host "Rebuild options:"
    Write-Host ""
    Write-Host "  1) Quick rebuild (uses cache)"
    Write-Host "  2) Force rebuild (--no-cache, fresh build)"
    Write-Host "  3) Force rebuild + remove old images"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $rebuildChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    switch ($rebuildChoice) {
        '1' { Invoke-RebuildQuick }
        '2' { Invoke-RebuildForce -RemoveImages $false }
        '3' { Invoke-RebuildForce -RemoveImages $true }
        '0' { return }
        default {
            Print-Error "Invalid option"
            Start-Sleep -Seconds 1
        }
    }
}

# Quick rebuild (uses cache)
function Invoke-RebuildQuick {
    Clear-Host
    Print-Header

    Print-Warning "This will rebuild containers using cached layers."
    Write-Host ""
    $confirm = Read-Host "Continue? (y/N)"

    if ($confirm -notmatch '^[Yy]$') {
        Print-Info "Rebuild cancelled"
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Print-Info "Rebuilding containers..."
    Write-Host ""

    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile

    try {
        # Stop containers
        Print-Info "Step 1/3: Stopping containers..."
        docker-compose -f $composeFile down

        Write-Host ""
        Print-Info "Step 2/3: Building containers..."
        Write-Host ""

        # Rebuild and start
        docker-compose -f $composeFile up -d --build

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Print-Info "Step 3/3: Starting services..."
            Write-Host ""
            Print-Success "Containers rebuilt and started successfully!"
            Write-Host ""
            Print-Info "Services running:"
            Write-Host "  • Web application: https://localhost:$WebPort"
            Write-Host "  • MinIO console: $MinioConsoleUrl"
            Write-Host ""

            # Show container status
            docker-compose -f $composeFile ps
        } else {
            Write-Host ""
            Print-Error "Failed to rebuild containers"
        }
    } finally {
        Pop-Location
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Force rebuild (--no-cache)
function Invoke-RebuildForce {
    param([bool]$RemoveImages)

    Clear-Host
    Print-Header

    Print-Warning "This will force rebuild ALL containers from scratch (--no-cache)."
    if ($RemoveImages) {
        Print-Warning "Old images will also be removed to free disk space."
    }
    Write-Host ""
    $confirm = Read-Host "Continue? (y/N)"

    if ($confirm -notmatch '^[Yy]$') {
        Print-Info "Rebuild cancelled"
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Print-Info "Force rebuilding containers..."
    Write-Host ""

    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile

    try {
        # Stop containers
        Print-Info "Step 1/4: Stopping containers..."
        if ($RemoveImages) {
            docker-compose -f $composeFile down --rmi local
            Print-Success "Containers stopped and old images removed"
        } else {
            docker-compose -f $composeFile down
            Print-Success "Containers stopped"
        }

        Write-Host ""
        Print-Info "Step 2/4: Force rebuilding images (--no-cache)..."
        Write-Host ""

        # Build with no cache
        docker-compose -f $composeFile build --no-cache

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Print-Success "Images rebuilt successfully!"
        } else {
            Write-Host ""
            Print-Error "Failed to rebuild images"
            Write-Host ""
            Read-Host "Press Enter to continue"
            return
        }

        Write-Host ""
        Print-Info "Step 3/4: Starting containers..."
        Write-Host ""

        # Start containers
        docker-compose -f $composeFile up -d

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Print-Info "Step 4/4: Verifying services..."
            Write-Host ""
            Print-Success "All containers started successfully!"
            Write-Host ""
            Print-Info "Services running:"
            Write-Host "  • Web application: https://localhost:$WebPort"
            Write-Host "  • MinIO console: $MinioConsoleUrl"
            Write-Host ""

            # Show container status
            docker-compose -f $composeFile ps
        } else {
            Write-Host ""
            Print-Error "Failed to start containers"
        }
    } finally {
        Pop-Location
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
}

# View environment
function Show-Environment {
    Clear-Host
    Print-Header
    Print-Info "Environment Variables:"
    Write-Host ""

    $envPath = Join-Path $ProjectRoot $EnvFile
    if (Test-Path $envPath) {
        # Mask sensitive values
        Get-Content $envPath | ForEach-Object {
            if ($_ -match '(PASSWORD|SECRET|KEY)=') {
                $_ -replace '(PASSWORD|SECRET|KEY)=.*', '$1=********'
            } else {
                $_
            }
        }
    } else {
        Print-Error "$EnvFile not found"
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
}

# SSL management
function Show-SslManagement {
    Clear-Host
    Print-Header

    $hostname = $env:COMPUTERNAME.ToLower()

    Write-Host "SSL Certificate Management:"
    Write-Host ""
    Write-Host "  1) Generate SSL certificate"
    Write-Host "  2) View certificate info"
    Write-Host "  3) Regenerate and restart nginx"
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $sslChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    Push-Location $ProjectRoot

    try {
        switch ($sslChoice) {
            '1' {
                Clear-Host
                Print-Header
                Print-Info "Generating SSL certificate..."
                Write-Host ""

                $sslScript = Join-Path $ProjectRoot "generate-ssl-cert.ps1"
                if (Test-Path $sslScript) {
                    & $sslScript
                    if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
                        Write-Host ""
                        Print-Success "Certificate generation completed!"
                    } else {
                        Write-Host ""
                        Print-Error "Certificate generation failed with exit code: $LASTEXITCODE"
                    }
                } else {
                    Print-Error "generate-ssl-cert.ps1 not found"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '2' {
                Clear-Host
                Print-Header
                Print-Info "SSL Certificate Information:"
                Write-Host ""

                $certPath = Join-Path $ProjectRoot "certs\fullchain.pem"
                if (Test-Path $certPath) {
                    Write-Host "=== Certificate Details ==="
                    openssl x509 -in $certPath -noout -text | Select-String -Pattern "Subject:"
                    Write-Host ""
                    Write-Host "=== Valid Dates ==="
                    openssl x509 -in $certPath -noout -dates
                    Write-Host ""
                    Print-Info "Certificate includes:"
                    Write-Host "  - localhost"
                    Write-Host "  - $hostname.local (network access)"
                    Write-Host "  - Local IP addresses"
                } else {
                    Print-Error "Certificate not found. Run option 1 to generate."
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '3' {
                Clear-Host
                Print-Header
                Print-Info "Regenerating SSL certificate and restarting nginx..."
                Write-Host ""

                $sslScript = Join-Path $ProjectRoot "generate-ssl-cert.ps1"
                if (Test-Path $sslScript) {
                    & $sslScript

                    if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
                        Write-Host ""
                        Print-Info "Restarting nginx container..."

                        if (Test-Docker) {
                            $composeFile = Join-Path $ProjectRoot $DockerComposeFile
                            docker-compose -f $composeFile restart nginx

                            if ($LASTEXITCODE -eq 0) {
                                Write-Host ""
                                Print-Success "SSL certificate regenerated and nginx restarted!"
                                Write-Host ""
                                Print-Info "Access your application at:"
                                Write-Host "  - https://localhost:$WebPort"
                                Write-Host "  - https://$hostname.local:$WebPort (network)"
                            } else {
                                Write-Host ""
                                Print-Error "Failed to restart nginx"
                            }
                        } else {
                            Print-Error "Docker is not running"
                        }
                    } else {
                        Write-Host ""
                        Print-Error "Certificate generation failed with exit code: $LASTEXITCODE"
                    }
                } else {
                    Print-Error "generate-ssl-cert.ps1 not found"
                }
                Write-Host ""
                Read-Host "Press Enter to continue"
            }
            '0' { return }
            default {
                Print-Error "Invalid option"
                Start-Sleep -Seconds 1
            }
        }
    } finally {
        Pop-Location
    }
}

# Docker status
function Show-DockerStatus {
    Clear-Host
    Print-Header
    Print-Info "Docker Status:"
    Write-Host ""

    Write-Host "=== Docker Information ==="
    if (Test-Docker) {
        docker --version
        docker-compose --version
        Write-Host ""
        Print-Success "Docker is running"
    } else {
        Print-Error "Docker is not running"
    }
    Write-Host ""

    Write-Host "=== Application Containers ==="
    Push-Location $ProjectRoot
    $composeFile = Join-Path $ProjectRoot $DockerComposeFile
    docker-compose -f $composeFile ps
    Pop-Location
    Write-Host ""

    Write-Host "=== Resource Usage ==="
    $containers = docker-compose -f (Join-Path $ProjectRoot $DockerComposeFile) ps -q 2>$null
    if ($containers) {
        docker stats --no-stream $containers
    } else {
        Print-Warning "No running containers"
    }
    Write-Host ""

    Read-Host "Press Enter to continue"
}

# Fix line endings
function Fix-LineEndings {
    Clear-Host
    Print-Header
    Print-Info "Fix Line Endings for Docker Compatibility"
    Write-Host ""
    Print-Warning "This will renormalize all files according to .gitattributes"
    Write-Host ""
    Write-Host "Line ending rules:"
    Write-Host "  • Shell scripts (.sh) -> LF (Unix)"
    Write-Host "  • Docker files -> LF (Unix)"
    Write-Host "  • PowerShell scripts (.ps1) -> CRLF (Windows)"
    Write-Host ""
    $confirm = Read-Host "Continue? (y/N)"

    if ($confirm -notmatch '^[Yy]$') {
        Print-Info "Operation cancelled"
        Write-Host ""
        Read-Host "Press Enter to continue"
        return
    }

    Write-Host ""
    Print-Info "Step 1/3: Removing files from git index..."
    git rm --cached -r . 2>&1 | Out-Null

    Print-Info "Step 2/3: Resetting git index..."
    git reset --hard 2>&1 | Out-Null

    Print-Info "Step 3/3: Renormalizing line endings..."
    git add --renormalize . 2>&1 | Out-Null

    Write-Host ""
    Print-Success "Line endings fixed!"
    Write-Host ""

    # Check if there are any changes
    $status = git status --porcelain
    if ($status) {
        Print-Warning "The following files were normalized:"
        Write-Host ""
        git status --short
        Write-Host ""
        Print-Info "You should commit these changes with:"
        Write-Host "  git commit -m 'chore: normalize line endings'"
    } else {
        Print-Success "No files needed normalization."
    }

    Write-Host ""
    Print-Info "Rebuild Docker containers to apply changes:"
    Write-Host "  docker compose down"
    Write-Host "  docker compose up --build"
    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Initialize environment configuration
function Initialize-EnvironmentConfig {
    Clear-Host
    Print-Header
    Print-Info "Initialize Environment Configuration (.env)"
    Write-Host ""

    $envPath = Join-Path $ProjectRoot $EnvFile
    $existingValues = @{}

    # Helper function to get existing value with default
    function Get-EnvValue($key, $default) {
        if ($existingValues.ContainsKey($key) -and $existingValues[$key]) {
            return $existingValues[$key]
        }
        return $default
    }

    # Read existing .env file if it exists
    if (Test-Path $envPath) {
        Print-Info "Reading existing .env file..."
        Get-Content $envPath | ForEach-Object {
            if ($_ -match '^([A-Z_][A-Z0-9_]*)=(.*)$') {
                $existingValues[$matches[1]] = $matches[2]
            }
        }
        Write-Host ""
        Print-Warning "Existing .env file will be backed up and replaced with normalized version"
        Write-Host ""
        $confirm = Read-Host "Continue? (y/N)"

        if ($confirm -notmatch '^[Yy]$') {
            Print-Info "Operation cancelled"
            Write-Host ""
            Read-Host "Press Enter to continue"
            return
        }

        # Backup existing .env
        $backupPath = "$envPath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item $envPath $backupPath
        Print-Info "Backed up to: $backupPath"
    }

    Print-Info "Generating random secrets..."
    Write-Host ""

    # Generate random values for secrets
    $djangoSecret = if ($existingValues.ContainsKey("DJANGO_SECRET_KEY")) {
        $existingValues["DJANGO_SECRET_KEY"]
    } else {
        -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 50 | ForEach-Object {[char]$_})
    }

    $encryptionSecret = if ($existingValues.ContainsKey("ENCRYPTION_SECRET")) {
        $existingValues["ENCRYPTION_SECRET"]
    } else {
        $bytes = New-Object byte[] 32
        [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($bytes)
        [Convert]::ToBase64String($bytes)
    }

    $minioSuffix = -join ((48..57) + (97..102) | Get-Random -Count 8 | ForEach-Object {[char]$_})
    $minioUser = if ($existingValues.ContainsKey("MINIO_ROOT_USER")) {
        $existingValues["MINIO_ROOT_USER"]
    } else {
        "admin-$minioSuffix"
    }

    $bytes = New-Object byte[] 32
    [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($bytes)
    $minioPassword = if ($existingValues.ContainsKey("MINIO_ROOT_PASSWORD")) {
        $existingValues["MINIO_ROOT_PASSWORD"]
    } else {
        [Convert]::ToBase64String($bytes).Replace('+', 'x').Replace('/', 'y')
    }

    # Get hostname for network access
    $hostname = $env:COMPUTERNAME.ToLower()

    # Build .env content with all sections
    $envContent = @"
# Django Settings
# IMPORTANT: In .env files, escape `$ with `$`$ and % with %%
# Example: "my-key`$123" becomes "my-key`$`$123"
DJANGO_SECRET_KEY="$djangoSecret"
DEBUG=$(Get-EnvValue "DEBUG" "True")

# Allowed Hosts - Add your hostname/domain for network access
# JSON array format - add your machine's hostname.local for mDNS access
# Example: ["127.0.0.1","0.0.0.0","localhost","$hostname.local"]
ALLOWED_HOSTS=$(Get-EnvValue "ALLOWED_HOSTS" '["127.0.0.1","0.0.0.0","localhost"]')

# Database (SQLite)
# Currently using db.sqlite3 in project root (data/db.sqlite3 in Docker)

# LDAP Configuration (if enabled)
SHOULD_USE_LDAP=$(Get-EnvValue "SHOULD_USE_LDAP" "False")
AUTH_LDAP_SERVER_URI="$(Get-EnvValue "AUTH_LDAP_SERVER_URI" "ldap://ldap.example.com")"
AUTH_LDAP_BIND_DN="$(Get-EnvValue "AUTH_LDAP_BIND_DN" "domain\username")"
AUTH_LDAP_BIND_PASSWORD="$(Get-EnvValue "AUTH_LDAP_BIND_PASSWORD" "password")"
AUTH_LDAP_SEARCH_BASE="$(Get-EnvValue "AUTH_LDAP_SEARCH_BASE" "dc=example,dc=com")"
AUTH_LDAP_SEARCH_FILTER="$(Get-EnvValue "AUTH_LDAP_SEARCH_FILTER" "(sAMAccountName=%(user)s)")"
AUTH_LDAP_USER_ATTR_MAP=$(Get-EnvValue "AUTH_LDAP_USER_ATTR_MAP" '{"first_name": "givenName", "last_name": "sn", "email": "mail"}')

# Email Configuration
EMAIL_HOST="$(Get-EnvValue "EMAIL_HOST" "localhost")"
EMAIL_PORT=$(Get-EnvValue "EMAIL_PORT" "25")
EMAIL_USE_TLS=$(Get-EnvValue "EMAIL_USE_TLS" "False")
EMAIL_USE_SSL=$(Get-EnvValue "EMAIL_USE_SSL" "False")
EMAIL_FROM="$(Get-EnvValue "EMAIL_FROM" "noreply@example.com")"

# Encryption
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_SECRET="$encryptionSecret"

# MinIO Object Storage
MINIO_ROOT_USER=$minioUser
MINIO_ROOT_PASSWORD=$minioPassword
MINIO_ENDPOINT=$(Get-EnvValue "MINIO_ENDPOINT" "minio:9000")
MINIO_ACCESS_KEY=$minioUser
MINIO_SECRET_KEY=$minioPassword
MINIO_BUCKET_NAME=$(Get-EnvValue "MINIO_BUCKET_NAME" "enterprise-app-media")
MINIO_USE_SSL=$(Get-EnvValue "MINIO_USE_SSL" "false")
USE_MINIO=$(Get-EnvValue "USE_MINIO" "true")

# Public domain for file URLs (used to generate accessible URLs for MinIO files)
# Set this to your machine's hostname and port for network access
# Auto-detected: $hostname.local:50478
PUBLIC_DOMAIN=$(Get-EnvValue "PUBLIC_DOMAIN" "$hostname.local:50478")

# CSRF Trusted Origins (for HTTPS network access)
# Required when accessing via HTTPS with custom hostname/port
# Comma-separated list of full URLs including protocol, hostname, and port
# Example: https://$hostname.local:50478
CSRF_TRUSTED_ORIGINS_EXTRA=$(Get-EnvValue "CSRF_TRUSTED_ORIGINS_EXTRA" "")

# Poppler (PDF processing) - Only needed on Windows
POPPLER_PATH=$(Get-EnvValue "POPPLER_PATH" "")

# WebAuthn / Passkey Configuration
WEBAUTHN_ENABLED=$(Get-EnvValue "WEBAUTHN_ENABLED" "True")
WEBAUTHN_RP_NAME="$(Get-EnvValue "WEBAUTHN_RP_NAME" "Enterprise Application Manager")"
WEBAUTHN_RP_ID=$(Get-EnvValue "WEBAUTHN_RP_ID" "localhost")
WEBAUTHN_ORIGIN=$(Get-EnvValue "WEBAUTHN_ORIGIN" "http://localhost:8000")
"@

    # Write to .env file
    Set-Content -Path $envPath -Value $envContent -NoNewline

    Print-Success "Environment configuration initialized!"
    Write-Host ""
    Print-Info "Generated new secrets:"
    if (-not $existingValues.ContainsKey("DJANGO_SECRET_KEY")) {
        Write-Host "  Django Secret: $djangoSecret"
    }
    if (-not $existingValues.ContainsKey("ENCRYPTION_SECRET")) {
        Write-Host "  Encryption Secret: $encryptionSecret"
    }
    if (-not $existingValues.ContainsKey("MINIO_ROOT_USER")) {
        Write-Host "  MinIO User: $minioUser"
        Write-Host "  MinIO Password: $minioPassword"
    }
    Write-Host ""
    Print-Info "Existing values were preserved"
    Write-Host ""
    Print-Warning "Review $envPath and update values as needed"
    Write-Host ""
    Print-Info "Restart Docker to apply changes:"
    Write-Host "  docker compose down"
    Write-Host "  docker compose up -d"
    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Open browser
function Show-OpenBrowser {
    Clear-Host
    Print-Header

    # Get network IP and hostname
    $networkIP = Get-NetworkIP
    $hostname = $env:COMPUTERNAME.ToLower()

    Print-Info "Open application in browser:"
    Write-Host ""
    Write-Host "Available URLs:"
    Write-Host "  1) https://localhost:$WebPort"
    Write-Host "  2) https://127.0.0.1:$WebPort"
    Write-Host "  3) https://${networkIP}:$WebPort (network IP)"
    Write-Host "  4) https://${hostname}.local:$WebPort (network .local domain)"
    Write-Host ""
    Write-Host "  0) Back"
    Write-Host ""
    Write-Host -NoNewline "Enter choice: "

    $browserChoice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
    Write-Host ""

    $url = ""

    switch ($browserChoice) {
        '1' { $url = "https://localhost:$WebPort" }
        '2' { $url = "https://127.0.0.1:$WebPort" }
        '3' { $url = "https://${networkIP}:$WebPort" }
        '4' { $url = "https://${hostname}.local:$WebPort" }
        '0' { return }
        default {
            Print-Error "Invalid option"
            Start-Sleep -Seconds 1
            return
        }
    }

    Write-Host ""
    Print-Info "Opening: $url"
    Write-Host ""

    try {
        Start-Process $url
        Print-Success "Browser opened successfully!"
        Write-Host ""
        Print-Info "URL: $url"
        Write-Host ""
        Print-Warning "Note: You may see a security warning about self-signed certificate"
        Write-Host "  - This is normal for local development"
        Write-Host "  - Click 'Advanced' or 'Accept Risk' to continue"
    } catch {
        Print-Error "Failed to open browser"
        Write-Host ""
        Print-Info "Try opening manually: $url"
    }

    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Main loop
function Main {
    while ($true) {
        Show-Menu
        $choice = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
        Write-Host ""

        switch ($choice) {
            '1' { Start-Application }
            '2' { Stop-Application }
            '3' { Restart-Application }
            '4' { Show-Logs }
            '5' { Show-ShellAccess }
            '6' { Show-DatabaseManagement }
            '7' { Show-MinioManagement }
            '8' { Show-DjangoCommands }
            '9' { Show-DevelopmentTools }
            { $_ -in 'a', 'A' } { Show-OpenBrowser }
            '0' {
                Clear-Host
                Print-Success "Goodbye!"
                exit 0
            }
            default {
                Print-Error "Invalid option"
                Start-Sleep -Seconds 1
            }
        }
    }
}

# Run main function
Main
