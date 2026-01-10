# Enterprise Application Manager - Configuration Example (PowerShell)
# Copy this file to manage.config.ps1 and customize for your environment

# Application Settings
$AppName = "Enterprise Application Manager"
$WebPort = 50478
$MinioConsolePort = 9005
$MinioApiPort = 9004

# Docker Settings
$DockerComposeFile = "docker-compose.yml"
$WebContainer = "enterprise-app-web"
$MinioContainer = "enterprise-app-minio"
$NginxContainer = "enterprise-app-nginx"

# Database Settings
$DbFile = "data\db.sqlite3"
$DbBackupDir = "backups\database"

# MinIO Settings
$MinioBucket = "enterprise-app-media"
$MinioDataDir = "data\minio"
$MinioConsoleUrl = "http://localhost:9005"

# File Paths
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$StaticDir = "static"
$StaticfilesDir = "staticfiles"
$MediaDir = "media"
$LogDir = "logs"
$CertsDir = "certs"

# Environment File
$EnvFile = ".env"

# Development Settings
$DefaultBrowser = "start"  # Windows default browser
$AutoOpenBrowser = $false
$LogTailLines = 100

# Backup Settings
$BackupRoot = "backups"
$BackupRetention = 7
$BackupIncludeMedia = $true
$BackupIncludeMinio = $true

# Migration Settings
$MigrationBatchSize = 100
$MigrationVerifyChecksum = $true

# SSL/OpenSSL Settings
# Path to OpenSSL executable (leave as "openssl" to use PATH, or specify full path)
# Common locations:
#   - C:\Program Files\OpenSSL-Win64\bin\openssl.exe
#   - C:\Program Files\Git\usr\bin\openssl.exe (if using Git for Windows)
#   - C:\ProgramData\chocolatey\bin\openssl.exe (if installed via Chocolatey)
$OpensslPath = "openssl"  # Uses PATH by default
