# Use an official node runtime as a parent image
FROM node:22.1.0

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and yarn.lock (or package-lock.json) into the container
COPY package.json ./
COPY package-lock.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Set the NODE_OPTIONS environment variable to use the legacy OpenSSL provider
ENV NODE_OPTIONS=--openssl-legacy-provider

# Build the React application
RUN npm run build

# Use a lightweight web server to serve the React application
RUN npm install -g serve
CMD ["serve", "-s", "build"]

# Expose port 3000
EXPOSE 3000
