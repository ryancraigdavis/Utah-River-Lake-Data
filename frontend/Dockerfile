FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy source code explicitly
COPY src/ ./src/
COPY index.html ./
COPY vite.config.js ./

# Debug: List files to verify copy
RUN ls -la && ls -la src/ && ls -la src/lib/

# Accept build arg for API URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the app
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install serve for production
RUN npm install -g serve

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Expose port
EXPOSE 3000

# Serve the built app
CMD ["serve", "-s", "dist", "-l", "3000", "-n"]