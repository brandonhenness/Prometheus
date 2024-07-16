# Use the latest Node.js image
FROM node:latest

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to the work directory
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install

# Copy the app code to the container
COPY . .

# Verify that next is installed correctly
RUN npx next --version

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define the command to run the app
CMD ["npm", "run", "dev"]
