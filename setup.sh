#!/bin/bash

# Setup script for Personal Dashboard

echo "🏠 Personal Dashboard Setup"
echo "============================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    
    echo ""
    echo "⚠️  IMPORTANT: You need to configure your .env file"
    echo ""
    echo "1. Generate a password hash:"
    echo "   python -c \"from passlib.hash import pbkdf2_sha256; print(pbkdf2_sha256.hash('your_password'))\""
    echo ""
    echo "2. Edit .env and paste the hash as PASSWORD_HASH"
    echo ""
    echo "3. Add your OpenAI API key to .env"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Create data directory
mkdir -p data
echo "✅ Data directory created"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your .env file (see instructions above)"
echo "2. (Optional) Run: python seed_data.py"
echo "3. Run the app: streamlit run app.py"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
