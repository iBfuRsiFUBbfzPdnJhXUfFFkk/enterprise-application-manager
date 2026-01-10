#!/bin/bash

# Generate self-signed SSL certificate for local development
# Supports localhost, 127.0.0.1, local IP, and .local domain (mDNS)

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CERTS_DIR="${SCRIPT_DIR}/certs"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  SSL Certificate Generator${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Create certs directory if it doesn't exist
mkdir -p "$CERTS_DIR"

# Get hostname and IP address
HOSTNAME=$(hostname -s | tr '[:upper:]' '[:lower:]')
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "")

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
echo -e "${YELLOW}Generating private key...${NC}"
openssl genrsa -out "${CERTS_DIR}/privkey.pem" 2048

# Generate certificate signing request
echo -e "${YELLOW}Generating certificate signing request...${NC}"
openssl req -new -key "${CERTS_DIR}/privkey.pem" \
    -out "${CERTS_DIR}/cert.csr" \
    -config "${CERTS_DIR}/openssl.cnf"

# Generate self-signed certificate (valid for 365 days)
echo -e "${YELLOW}Generating self-signed certificate (valid for 365 days)...${NC}"
openssl x509 -req -days 365 \
    -in "${CERTS_DIR}/cert.csr" \
    -signkey "${CERTS_DIR}/privkey.pem" \
    -out "${CERTS_DIR}/fullchain.pem" \
    -extensions v3_req \
    -extfile "${CERTS_DIR}/openssl.cnf"

# Clean up CSR
rm "${CERTS_DIR}/cert.csr"

# Set permissions
chmod 600 "${CERTS_DIR}/privkey.pem"
chmod 644 "${CERTS_DIR}/fullchain.pem"

echo ""
echo -e "${GREEN}✓ SSL certificate generated successfully!${NC}"
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
echo -e "${YELLOW}Note:${NC} This is a self-signed certificate for development only."
echo "      Browsers will show a security warning. Click 'Advanced' and 'Proceed'."
echo ""
echo "To trust this certificate on macOS:"
echo "  sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ${CERTS_DIR}/fullchain.pem"
echo ""
echo "Valid for 365 days. Regenerate before expiration."
