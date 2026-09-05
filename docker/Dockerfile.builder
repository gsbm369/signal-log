# Builds the Astro site and runs the Claude curator.
# Runs as uid 1000 so files written into bind-mounted host dirs stay owned by the host user.
FROM node:22-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    npm_config_cache=/tmp/.npm \
    NODE_ENV=production

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip \
      ca-certificates tzdata rsync \
 && rm -rf /var/lib/apt/lists/*

# --- Python deps (own layer: rarely changes) ---
COPY curator/requirements.txt /app/curator/requirements.txt
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir -r /app/curator/requirements.txt
ENV PATH="/opt/venv/bin:${PATH}"

# --- Node deps (own layer: changes only with package-lock.json) ---
COPY site/package.json site/package-lock.json /app/site/
RUN cd /app/site && npm ci --include=dev

# --- Application source ---
COPY site /app/site
COPY curator /app/curator
COPY scripts/run-cycle.sh /app/run-cycle.sh

RUN chmod +x /app/run-cycle.sh \
 && mkdir -p /out /data/state /app/site/src/content/posts \
 && chown -R node:node /app /out /data

ENV CONTENT_DIR=/app/site/src/content/posts \
    STATE_DIR=/data/state \
    FEEDS_FILE=/app/curator/feeds.yml \
    OUT_DIR=/out

USER node
WORKDIR /app
CMD ["/app/run-cycle.sh"]
