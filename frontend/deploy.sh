#!/bin/bash

# Microsoft Agent Framework Frontend Deployment Script

echo "🚀 Building Microsoft Agent Framework Frontend..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the project
echo "🔨 Building production bundle..."
npm run build

echo "✅ Frontend build complete!"
echo ""
echo "📁 Build files are in the 'build' directory"
echo "🌐 You can now deploy the 'build' folder to any static hosting service:"
echo ""
echo "   • Netlify: Drag and drop the 'build' folder"
echo "   • Vercel: Run 'vercel --prod' in this directory"
echo "   • GitHub Pages: Push 'build' contents to gh-pages branch"
echo "   • AWS S3: Upload 'build' contents to S3 bucket"
echo ""
echo "🔧 Make sure to set REACT_APP_API_URL to your backend URL!"
echo "   Current API URL: ${REACT_APP_API_URL:-'https://web--microsoft-agent-framework--4h7vh8ddvxpx.code.run'}"
