#!/bin/sh
# Substitute environment variables in the nginx config template and write the output to nginx.conf
envsubst '$FRONTEND_HOST_NAME $BACKEND_HOST_NAME $PGADMIN_HOST_NAME' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Optionally, print the generated config for debugging
# cat /etc/nginx/nginx.conf

# Start NGINX in the foreground
exec nginx -g 'daemon off;'
