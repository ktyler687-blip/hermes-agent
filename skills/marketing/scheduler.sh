#!/usr/bin/env bash
# ============================================================
#  AUTONOMOUS MARKETING AGENT — SCHEDULER SETUP
#  Installs cron jobs for daily automated execution
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PYTHON="$(which python3)"
LOG_DIR="$SCRIPT_DIR/logs"
CRON_MARKER="# hermes-marketing-agent"

mkdir -p "$LOG_DIR"

echo ""
echo "  AUTONOMOUS MARKETING AGENT — SCHEDULER SETUP"
echo "  =============================================="
echo "  Agent dir:  $SCRIPT_DIR"
echo "  Python:     $PYTHON"
echo "  Logs:       $LOG_DIR"
echo ""

# Validate ANTHROPIC_API_KEY is set
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "  ⚠  WARNING: ANTHROPIC_API_KEY is not set in this shell."
  echo "     Add it to your ~/.bashrc or ~/.zshrc:"
  echo "     export ANTHROPIC_API_KEY=sk-ant-..."
  echo ""
fi

# Build cron jobs
CRON_DAILY="0 6 * * * cd $HERMES_ROOT && ANTHROPIC_API_KEY=\${ANTHROPIC_API_KEY} $PYTHON $SCRIPT_DIR/daily_agent.py --all --pick-top 2 >> $LOG_DIR/daily.log 2>&1 $CRON_MARKER"
CRON_WEEKEND="0 8 * * 0 cd $HERMES_ROOT && ANTHROPIC_API_KEY=\${ANTHROPIC_API_KEY} $PYTHON $SCRIPT_DIR/daily_agent.py --all >> $LOG_DIR/weekly.log 2>&1 $CRON_MARKER"
CRON_REPORT="0 20 * * * $PYTHON $SCRIPT_DIR/revenue_tracker.py --status >> $LOG_DIR/revenue.log 2>&1 $CRON_MARKER"

echo "  Cron jobs to install:"
echo ""
echo "  1. Daily (6am) — auto-pick top 2 brands, run full loop"
echo "     $CRON_DAILY"
echo ""
echo "  2. Sunday (8am) — full loop for ALL 7 brands"
echo "     $CRON_WEEKEND"
echo ""
echo "  3. Daily (8pm) — revenue status log"
echo "     $CRON_REPORT"
echo ""

read -r -p "  Install these cron jobs? [y/N] " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  # Remove old entries
  (crontab -l 2>/dev/null | grep -v "$CRON_MARKER") | crontab -
  # Add new entries
  (
    crontab -l 2>/dev/null
    echo "$CRON_DAILY"
    echo "$CRON_WEEKEND"
    echo "$CRON_REPORT"
  ) | crontab -
  echo ""
  echo "  ✓ Cron jobs installed. Verify with: crontab -l"
else
  echo "  Skipped. To install manually, run: crontab -e"
fi

echo ""
echo "  MANUAL RUN COMMANDS:"
echo "  ────────────────────────────────────────────────"
echo "  # Run daily loop now (picks top 2 brands):"
echo "  python $SCRIPT_DIR/daily_agent.py"
echo ""
echo "  # Dry run (no API cost, see the plan):"
echo "  python $SCRIPT_DIR/daily_agent.py --dry-run"
echo ""
echo "  # Full loop for all 7 brands:"
echo "  python $SCRIPT_DIR/daily_agent.py --all"
echo ""
echo "  # Single brand:"
echo "  python $SCRIPT_DIR/daily_agent.py --brand TheFlavorCrave"
echo ""
echo "  # View dashboard:"
echo "  python $SCRIPT_DIR/daily_agent.py --dashboard"
echo ""
echo "  # Revenue status:"
echo "  python $SCRIPT_DIR/revenue_tracker.py --status"
echo ""
echo "  # Log revenue:"
echo "  python $SCRIPT_DIR/revenue_tracker.py --log TheFlavorCrave 450.00 affiliate"
echo ""
echo "  # Campaign runner (fine-grained mode control):"
echo "  python $SCRIPT_DIR/campaign_runner.py --brand HealthIsWealth --mode content"
echo "  ────────────────────────────────────────────────"
echo ""
