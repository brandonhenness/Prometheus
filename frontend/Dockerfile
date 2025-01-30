FROM node:18-alpine

WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json* ./
RUN npm install --force

# Copy source files
COPY . .

# Configure Next.js for Docker development
ENV NEXT_TELEMETRY_DISABLED=1 \
    WATCHPACK_POLLING=true \
    NODE_ENV=development

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]