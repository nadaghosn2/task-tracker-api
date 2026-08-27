# ---- builder stage ----
# Builder stage: install dependencies into an isolated virtualenv;
# none of this stage's layers are carried into the final image.
FROM python:3.11-slim AS builder

# Set the working directory for the build steps below.
WORKDIR /app

# Create a virtualenv at /opt/venv, kept separate from system site-packages.
RUN python -m venv /opt/venv
# Put the virtualenv's bin directory first on PATH so pip/python resolve to it.
ENV PATH="/opt/venv/bin:$PATH"

# Copy only the dependency manifest first, so this layer is cached
# independently of application source code changes.
COPY requirements.txt .
# Install dependencies into the virtualenv without caching pip's download/build artifacts.
RUN pip install --no-cache-dir -r requirements.txt

# ---- runtime stage ----
# Runtime stage: start fresh from a slim base with none of the builder's
# compilers, caches, or build-only files.
FROM python:3.11-slim AS runtime

# Create a dedicated non-root user with no home directory and no login shell.
RUN useradd --uid 1000 --no-create-home --shell /usr/sbin/nologin app

# Set the working directory for the application.
WORKDIR /app

# Copy only the populated virtualenv from the builder stage.
COPY --from=builder /opt/venv /opt/venv
# Copy the application source code.
COPY app ./app

# Ensure the non-root user owns the application files before switching to it.
RUN chown -R app:app /app

# Put the virtualenv's bin directory first on PATH so `uvicorn` resolves to it.
ENV PATH="/opt/venv/bin:$PATH"

# Drop root privileges for all subsequent instructions and the running container.
USER app

# Document that the application listens on port 8000.
EXPOSE 8000

# Poll /health every 30s using stdlib urllib, so no extra HTTP client
# needs to be installed in the image.
HEALTHCHECK --interval=30s --timeout=5s CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)"]

# Start the API server; no --reload, since this is the production/runtime image.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
