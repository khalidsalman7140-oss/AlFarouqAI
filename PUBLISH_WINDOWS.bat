@echo off
set /p REPO=Your authorized GitHub OWNER/REPOSITORY:
echo This creates a PUBLIC repository only after your explicit confirmation.
choice /M "Approve public source publication"
if errorlevel 2 exit /b 0
python scripts\publish.py --repo "%REPO%" --public --approve-publication
pause
