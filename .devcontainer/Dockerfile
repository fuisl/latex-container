FROM qmcgaw/latexdevcontainer:latest-full

# Install fontconfig for XeLaTeX font support
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fontconfig \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*
