# Use the official NGINX Alpine image
FROM nginx:alpine

# Install gettext for envsubst
RUN apk add --no-cache gettext

# Optionally, remove the default NGINX config if you don't need it
RUN rm /etc/nginx/conf.d/default.conf

# Copy the NGINX configuration template into the container
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint to our script
ENTRYPOINT ["/entrypoint.sh"]
