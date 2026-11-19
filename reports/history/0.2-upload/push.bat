
@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title Khaled Salman - One Click GitHub

echo ==========================================
echo       KHALED SALMAN - AUTO PUBLISH
echo ==========================================

where git >nul 2>&1 || (
 echo Git is not available in PATH.
 pause
 exit /b 1
)

where gh >nul 2>&1 || (
 echo GitHub CLI is not available in PATH.
 pause
 exit /b 1
)

gh auth status >nul 2>&1 || (
 echo Run gh auth login first.
 pause
 exit /b 1
)

for %%I in ("%CD%") do set "PROJECT=%%~nxI"
for /f "delims=" %%U in ('gh api user --jq .login') do set "OWNER=%%U"

if not defined OWNER (
 echo Could not detect GitHub account.
 pause
 exit /b 1
)

if not exist "README.md" (
 >README.md echo # %PROJECT%
 >>README.md echo.
 >>README.md echo **Developer:** Khaled Salman
 >>README.md echo.
 >>README.md echo ## Project purpose
 >>README.md echo Describe the actual purpose and features of this project here.
 >>README.md echo.
 >>README.md echo ## Technologies
 >>README.md echo Document the languages and tools used.
 >>README.md echo.
 >>README.md echo ## Installation and usage
 >>README.md echo Add verified setup and run instructions here.
)

if not exist ".gitignore" (
 >.gitignore echo .env
 >>.gitignore echo .env.*
 >>.gitignore echo !.env.example
 >>.gitignore echo venv/
 >>.gitignore echo .venv/
 >>.gitignore echo __pycache__/
 >>.gitignore echo *.pyc
 >>.gitignore echo node_modules/
 >>.gitignore echo *.pem
 >>.gitignore echo *.key
)

if not exist ".git" git init
if errorlevel 1 goto failed

git branch -M main
if errorlevel 1 goto failed

git remote get-url origin >nul 2>&1
if errorlevel 1 (
 gh repo view "%OWNER%/%PROJECT%" >nul 2>&1
 if errorlevel 1 (
  gh repo create "%OWNER%/%PROJECT%" --private
  if errorlevel 1 goto failed
 )
 git remote add origin "https://github.com/%OWNER%/%PROJECT%.git"
 if errorlevel 1 goto failed
)

echo.
echo Review README.md and .gitignore before upload.
choice /M "Continue and publish project"
if errorlevel 2 exit /b 0

git add -A
if errorlevel 1 goto failed

git diff --cached --quiet
if errorlevel 1 (
 git commit -m "Update %PROJECT%"
 if errorlevel 1 goto failed
) else (
 echo No new changes to commit.
)

git push -u origin main
if errorlevel 1 goto failed

echo.
echo SUCCESS: https://github.com/%OWNER%/%PROJECT%
pause
exit /b 0

:failed
echo.
echo Upload failed. Read the error above.
pause
exit /b 1
