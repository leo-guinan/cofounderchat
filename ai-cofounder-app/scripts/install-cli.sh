#!/bin/bash
# Install AI Cofounder CLI on a server

set -e

echo "================================"
echo "AI Cofounder CLI Installation"
echo "================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root"
  exit 1
fi

# Check OS
if [ ! -f /etc/os-release ]; then
  echo "❌ Cannot detect OS"
  exit 1
fi

source /etc/os-release

echo "OS: $PRETTY_NAME"
echo ""

# Install Node.js if not present
if ! command -v node &> /dev/null; then
  echo "Installing Node.js..."
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs
  echo "✓ Node.js installed"
else
  echo "✓ Node.js already installed ($(node --version))"
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
  echo "Installing Docker..."
  curl -fsSL https://get.docker.com | sh
  systemctl enable docker
  systemctl start docker
  echo "✓ Docker installed"
else
  echo "✓ Docker already installed"
fi

# Install AI Cofounder CLI
echo ""
echo "Installing AI Cofounder CLI..."

# Build from source or install from npm
if [ -d "./cli" ]; then
  cd cli
  npm install
  npm run build
  npm link
  echo "✓ CLI installed from source"
else
  npm install -g @ai-cofounder/cli
  echo "✓ CLI installed from npm"
fi

# Verify installation
echo ""
echo "Verifying installation..."
cofounder --version

echo ""
echo "================================"
echo "✅ Installation Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "  1. Initialize node: cofounder init"
echo "  2. Set up SSL: cofounder ssl setup -d yourdomain.com -e you@email.com"
echo "  3. Deploy app: cofounder deploy"
echo "  4. Start agent: cofounder agent start --daemon"
echo ""
