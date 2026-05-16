@echo off
echo ==========================================
echo Streamlit Cloud Deployment Preparation
echo ==========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo X Git not initialized
    echo Run: git init
    exit /b 1
)

echo [OK] Git repository found
echo.

REM Check for required files
echo Checking required files...
set all_present=1

if exist app.py (
    echo   [OK] app.py
) else (
    echo   [X] app.py - MISSING!
    set all_present=0
)

if exist requirements.txt (
    echo   [OK] requirements.txt
) else (
    echo   [X] requirements.txt - MISSING!
    set all_present=0
)

if exist .streamlit\config.toml (
    echo   [OK] .streamlit\config.toml
) else (
    echo   [X] .streamlit\config.toml - MISSING!
    set all_present=0
)

if exist README.md (
    echo   [OK] README.md
) else (
    echo   [X] README.md - MISSING!
    set all_present=0
)

echo.

if %all_present%==0 (
    echo [X] Some required files are missing
    exit /b 1
)

REM Check .gitignore
findstr /C:".env" .gitignore >nul
if %errorlevel%==0 (
    echo [OK] .env is in .gitignore
) else (
    echo [!] WARNING: .env not in .gitignore - add it!
)

echo.
echo ==========================================
echo Next Steps:
echo ==========================================
echo.
echo 1. Review your code changes
echo.
echo 2. Commit your code:
echo    git add .
echo    git commit -m "Fixed PDF parser - captures all voucher types"
echo.
echo 3. Create GitHub repository (if not exists):
echo    https://github.com/new
echo.
echo 4. Push to GitHub:
echo    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 5. Deploy to Streamlit Cloud:
echo    https://streamlit.io/cloud
echo.
echo 6. Configure secrets in Streamlit Cloud
echo    (See STREAMLIT_DEPLOYMENT_GUIDE.md for details)
echo.
echo ==========================================
echo.
echo Current git status:
git status --short
echo.
pause

@REM Made with Bob
