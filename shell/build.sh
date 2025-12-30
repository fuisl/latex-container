#!/bin/bash
# LaTeX Build Script - Fast compilation with latexmk

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting LaTeX compilation...${NC}"

# Navigate to source directory
cd /workspace/src

# Run latexmk - it handles everything (biber, makeglossaries, multiple passes)
echo -e "${YELLOW}Running latexmk with XeLaTeX...${NC}"
latexmk -xelatex -synctex=1 -interaction=nonstopmode -file-line-error -outdir=../out main.tex

# Check if PDF was created
if [ -f "../out/main.pdf" ]; then
    echo -e "${GREEN}✓ Compilation successful!${NC}"
    echo -e "${GREEN}PDF generated at: /workspace/out/main.pdf${NC}"
    
    # Show file size
    SIZE=$(du -h ../out/main.pdf | cut -f1)
    echo -e "${GREEN}File size: ${SIZE}${NC}"
else
    echo -e "${RED}✗ Compilation failed - PDF not generated${NC}"
    exit 1
fi
