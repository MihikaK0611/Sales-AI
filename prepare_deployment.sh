#!/bin/bash

echo "=========================================="
echo "Streamlit Cloud Deployment Preparation"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized"
    echo "Run: git init"
    exit 1
fi

echo "✅ Git repository found"
echo ""

# Check for required files
echo "Checking required files..."
files=("app.py" "requirements.txt" ".streamlit/config.toml" "README.md")
all_present=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - MISSING!"
        all_present=false
    fi
done

echo ""

if [ "$all_present" = false ]; then
    echo "❌ Some required files are missing"
    exit 1
fi

# Check .gitignore
if grep -q ".env" .gitignore; then
    echo "✅ .env is in .gitignore"
else
    echo "⚠️  WARNING: .env not in .gitignore - add it!"
fi

echo ""

# Remove debug files (optional)
echo "Cleaning up debug files..."
debug_files=("test_pdf.py" "debug_pdf_structure.py" "debug_pdf_detailed.py" "debug_customer_detection.py" "validate_parser.py" "clear_database.py" "clear_sales_data.py")

for file in "${debug_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  Found: $file"
        read -p "  Remove $file? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm "$file"
            echo "  ✅ Removed $file"
        fi
    fi
done

echo ""

# Check git status
echo "Git status:"
git status --short

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Review changes above"
echo "2. Commit your code:"
echo "   git add ."
echo "   git commit -m 'Fixed PDF parser - captures all voucher types'"
echo ""
echo "3. Create GitHub repository (if not exists):"
echo "   https://github.com/new"
echo ""
echo "4. Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Deploy to Streamlit Cloud:"
echo "   https://streamlit.io/cloud"
echo ""
echo "6. Configure secrets in Streamlit Cloud"
echo "   (See STREAMLIT_DEPLOYMENT_GUIDE.md for details)"
echo ""
echo "=========================================="

# Made with Bob
