#!/bin/bash
# Setup script for UV-based Multi-Agent Workflow System

set -e

echo "🚀 Setting up Multi-Agent Workflow System with UV..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Initialize UV project if not already done
if [ ! -f "uv.lock" ]; then
    echo "🔧 Initializing UV project..."
    uv sync
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << 'ENVEOF'
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Tavily Search API Configuration  
TAVILY_API_KEY=your_tavily_api_key_here

# LangSmith Configuration (Optional)
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=multiagent_workflow
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# LangFuse Configuration (Optional)
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
ENVEOF
    echo "⚠️  Please update .env file with your actual API keys"
fi

echo "✅ Setup complete! Use the following commands:"
echo "   uv run main.py                 # Run the main application"
echo "   uv run workflow-demo           # Run workflow demo"
echo "   uv run pytest                 # Run tests (when available)"
echo "   uv add <package>               # Add new dependencies"
