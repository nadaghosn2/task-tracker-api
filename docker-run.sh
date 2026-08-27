#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="task-tracker:dev"
CONTAINER_NAME="task-tracker-dev"
HOST_PORT="8000"

echo "==> Building image ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" .

if docker ps -a --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "==> Removing existing container ${CONTAINER_NAME}"
  docker rm -f "${CONTAINER_NAME}" >/dev/null
fi

echo "==> Starting container ${CONTAINER_NAME} on port ${HOST_PORT}"
docker run -d --name "${CONTAINER_NAME}" -p "${HOST_PORT}:8000" "${IMAGE_NAME}"

echo "==> Waiting for /health"
for i in $(seq 1 10); do
  if curl -sf "http://localhost:${HOST_PORT}/health" >/dev/null; then
    echo "==> Healthy:"
    curl -s "http://localhost:${HOST_PORT}/health"
    echo
    exit 0
  fi
  sleep 1
done

echo "==> Container did not become healthy in time. Logs:"
docker logs "${CONTAINER_NAME}"
exit 1
