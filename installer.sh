#!/bin/bash
echo "👻 GHOST PHISHER - COMPLETE INSTALLATION"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root user"
fi

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install dependencies
print_status "Installing dependencies..."
apt install -y python3 php curl wget git

# Install Cloudflared
print_status "Installing Cloudflared..."
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
mv cloudflared /usr/local/bin/

# Verify installations
print_status "Verifying installations..."

# Check Python
if command -v python3 &> /dev/null; then
    print_status "Python3 is installed"
else
    print_error "Python3 installation failed"
    exit 1
fi

# Check PHP
if command -v php &> /dev/null; then
    print_status "PHP is installed"
else
    print_error "PHP installation failed"
    exit 1
fi

# Check Cloudflared
if command -v cloudflared &> /dev/null; then
    print_status "Cloudflared is installed"
else
    print_error "Cloudflared installation failed"
    exit 1
fi

# Create Ghost Phisher directory
print_status "Setting up Ghost Phisher..."
mkdir -p ~/ghostphisher
cd ~/ghostphisher

# Download main script (you'll need to add this manually or via git)
print_status "Setup complete!"
echo ""
echo -e "${GREEN}✅ Installation Successful!${NC}"
echo ""
echo "Next steps:"
echo "1. Copy ghost-phisher.py to ~/ghost-phisher/"
echo "2. Run: cd ~/ghost-phisher"
echo "3. Run: python3 ghost-phisher.py"
echo ""
echo "📖 For updates: https://github.com/yourusername/ghost-phisher"