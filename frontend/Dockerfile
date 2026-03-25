# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

ARG VITE_ORDERS_MFE_URL
ENV VITE_ORDERS_MFE_URL=${VITE_ORDERS_MFE_URL}

COPY package*.json yarn.lock* ./

RUN yarn install --frozen-lockfile

COPY . .

RUN yarn build

# Production stage
FROM nginx:1.25-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
