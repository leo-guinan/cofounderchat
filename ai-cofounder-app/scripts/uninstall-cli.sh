#!/bin/bash
# Uninstall AI Cofounder CLI

set -e

echo "Uninstalling AI Cofounder CLI..."

# Stop agent if running
if systemctl is-active --quiet ai-cofounder-agent; then
  systemctl stop ai-cofounder-agent
  systemctl disable ai-cofounder-agent
  echo "✓ Agent stopped"
fi

# Remove systemd service
if [ -f /etc/systemd/system/ai-cofounder-agent.service ]; then
  rm /etc/systemd/system/ai-cofounder-agent.service
  systemctl daemon-reload
  echo "✓ Service removed"
fi

# Uninstall CLI
npm uninstall -g @ai-cofounder/cli || true
echo "✓ CLI uninstalled"

# Ask about config removal
read -p "Remove configuration files? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  rm -rf /etc/ai-cofounder
  echo "✓ Configuration removed"
fi

echo ""
echo "✅ Uninstall complete"
