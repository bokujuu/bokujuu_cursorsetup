@echo off
echo probe: intentional pause for watchdog test
echo Press any key to continue . . .
ping 127.0.0.1 -n 120 >nul
