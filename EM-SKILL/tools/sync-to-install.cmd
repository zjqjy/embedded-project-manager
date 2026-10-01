@echo off
REM sync-to-install.cmd — EM-SKILL dev → install 同步脚本（只补不删，不执行 rm）
REM 约定见项目 CLAUDE.md「EM-SKILL dev / install 路径约定」
REM
REM 默认：SRC=脚本父目录, DST=%USERPROFILE%\.claude\skills\EM-SKILL
REM 覆盖：set EM_INSTALL_PATH=D:\other
REM 用法：sync-to-install.cmd [/y]

setlocal enabledelayedexpansion
set "SRC=%~dp0.."
set "DST=%USERPROFILE%\.claude\skills\EM-SKILL"
if not "%EM_INSTALL_PATH%"=="" set "DST=%EM_INSTALL_PATH%"

echo 📦 EM-SKILL dev → install 同步（只补不删，不执行 rm）
echo   SRC: %SRC%
echo   DST: %DST%
echo.

if /i not "%~1"=="/y" (
    set "C="
    set /p "C=确认执行？[y/N] "
    if /i not "!C!"=="y" (
        echo ❌ 取消
        exit /b 1
    )
)

REM 单行 robocopy：/E 只补不删；排除 __pycache__ .git build dist *.egg-info 和 .pyc/.pyo/.pyd
robocopy "%SRC%" "%DST%" /E /R:0 /W:0 /NFL /NDL /NJH /NJS /XD __pycache__ .git build dist *.egg-info /XF *.pyc *.pyo *.pyd
echo ✅ 完成（install 中 dev 没有的旧文件不会被删除，请手动清理）
endlocal
