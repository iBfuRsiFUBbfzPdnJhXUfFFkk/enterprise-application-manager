# Generate self-signed SSL certificate for local development (PowerShell)
# Supports localhost, 127.0.0.1, local IP, and .local domain (mDNS)

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CertsDir = Join-Path $ScriptDir "certs"

Write-Host "================================" -ForegroundColor Green
Write-Host "  SSL Certificate Generator" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Create certs directory if it doesn't exist
if (-not (Test-Path $CertsDir)) {
    New-Item -ItemType Directory -Path $CertsDir | Out-Null
}

# Get hostname and IP address
$Hostname = $env:COMPUTERNAME.ToLower()
$LocalIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet*, Wi-Fi* | Where-Object { $_.IPAddress -notlike "169.254.*" } | Select-Object -First 1).IPAddress

Write-Host "Detected system:"
Write-Host "  Hostname: $Hostname"
if ($LocalIP) {
    Write-Host "  Local IP: $LocalIP"
}
Write-Host ""

# Check if OpenSSL is available
$OpensslPath = (Get-Command openssl -ErrorAction SilentlyContinue).Source
if (-not $OpensslPath) {
    Write-Host "ERROR: OpenSSL not found in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install OpenSSL:" -ForegroundColor Yellow
    Write-Host "  Option 1: Install via Chocolatey:"
    Write-Host "    choco install openssl"
    Write-Host "  Option 2: Install via Git for Windows (includes OpenSSL)"
    Write-Host "  Option 3: Download from: https://slproweb.com/products/Win32OpenSSL.html"
    Write-Host ""
    exit 1
}

# Create OpenSSL configuration file
$OpensslConf = @"
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
DNS.2 = $Hostname
DNS.3 = $Hostname.local
DNS.4 = *.$Hostname.local
IP.1 = 127.0.0.1
IP.2 = ::1
"@

# Add local IP if detected
if ($LocalIP) {
    $OpensslConf += "`nIP.3 = $LocalIP"
}

$OpensslConfPath = Join-Path $CertsDir "openssl.cnf"
$OpensslConf | Out-File -FilePath $OpensslConfPath -Encoding ASCII

# Generate private key
Write-Host "Generating private key..." -ForegroundColor Yellow
$PrivKeyPath = Join-Path $CertsDir "privkey.pem"
& openssl genrsa -out $PrivKeyPath 2048 2>$null

# Generate certificate signing request
Write-Host "Generating certificate signing request..." -ForegroundColor Yellow
$CsrPath = Join-Path $CertsDir "cert.csr"
& openssl req -new -key $PrivKeyPath -out $CsrPath -config $OpensslConfPath

# Generate self-signed certificate (valid for 365 days)
Write-Host "Generating self-signed certificate (valid for 365 days)..." -ForegroundColor Yellow
$CertPath = Join-Path $CertsDir "fullchain.pem"
& openssl x509 -req -days 365 -in $CsrPath -signkey $PrivKeyPath -out $CertPath -extensions v3_req -extfile $OpensslConfPath

# Clean up CSR
Remove-Item $CsrPath

Write-Host ""
Write-Host "✓ SSL certificate generated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Certificate files:"
Write-Host "  Private key: $PrivKeyPath"
Write-Host "  Certificate: $CertPath"
Write-Host ""
Write-Host "Certificate includes:"
Write-Host "  - localhost"
Write-Host "  - 127.0.0.1"
Write-Host "  - $Hostname"
Write-Host "  - $Hostname.local"
if ($LocalIP) {
    Write-Host "  - $LocalIP"
}
Write-Host ""
Write-Host "Note: This is a self-signed certificate for development only." -ForegroundColor Yellow
Write-Host "      Browsers will show a security warning. Click 'Advanced' and 'Proceed'."
Write-Host ""
Write-Host "To trust this certificate on Windows:"
Write-Host "  1. Double-click $CertPath"
Write-Host "  2. Click 'Install Certificate'"
Write-Host "  3. Select 'Local Machine' (requires admin)"
Write-Host "  4. Place in 'Trusted Root Certification Authorities' store"
Write-Host ""
Write-Host "Valid for 365 days. Regenerate before expiration."
