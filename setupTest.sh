
docker kill zest

ZEST_IMAGE_VERSION="databoxsystems/zestdb-amd64:latest"

echo "start the store with the key from above"
docker run -p 5555:5555 -p 5556:5556 -d --name zest --rm ${ZEST_IMAGE_VERSION} /app/zest/server.exe --secret-key-file example-server-key --identity '127.0.0.1' --enable-logging
