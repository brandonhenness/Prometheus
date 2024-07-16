# Use the official lightweight Node.js image.
# https://hub.docker.com/_/node
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to the work directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the app code to the container
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define the command to run the app
CMD ["npm", "run", "dev"]
