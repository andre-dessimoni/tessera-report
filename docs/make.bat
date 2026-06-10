@ECHO OFF
SETLOCAL

SET SPHINXBUILD=python -m sphinx
SET SOURCEDIR=.
SET BUILDDIR=_build

IF "%1"==""      GOTO help
IF "%1"=="help"  GOTO help
IF "%1"=="html"  GOTO html
IF "%1"=="clean" GOTO clean
IF "%1"=="live"  GOTO live
IF "%1"=="install" GOTO install
GOTO help

:help
ECHO Usage: make.bat [html^|clean^|live^|install]
ECHO.
ECHO   html     Build HTML documentation in _build/html
ECHO   clean    Remove the _build directory
ECHO   live     Local server with auto-rebuild (requires sphinx-autobuild)
ECHO   install  Install documentation dependencies
GOTO end

:html
%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%\html %SPHINXOPTS%
IF ERRORLEVEL 1 EXIT /B 1
ECHO.
ECHO Documentation built at %BUILDDIR%\html\index.html
GOTO end

:clean
IF EXIST %BUILDDIR% (
    RMDIR /S /Q %BUILDDIR%
    ECHO _build directory removed.
) ELSE (
    ECHO Nothing to clean.
)
GOTO end

:live
python -m sphinx_autobuild %SOURCEDIR% %BUILDDIR%\html %SPHINXOPTS% --open-browser
GOTO end

:install
pip install -r requirements.txt
GOTO end

:end
ENDLOCAL
