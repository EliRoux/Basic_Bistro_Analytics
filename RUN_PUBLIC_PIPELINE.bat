@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "System\python\run_public_pipeline.py" %*
) else (
    py "System\python\run_public_pipeline.py" %*
)
if errorlevel 1 (
    echo Pipeline failed. Review the error above.
    pause
    exit /b 1
)
echo Public synthetic pipeline finished.
pause
