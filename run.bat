@echo off
REM Activate the virtual environment
call odoo-venv\Scripts\activate.bat

REM Run Odoo with the config file
python odoo-bin -c odoo.conf -u sale_summary_report

REM Keep the window open after Odoo stops (optional)
pause