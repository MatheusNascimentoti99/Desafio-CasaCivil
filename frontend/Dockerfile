# Build stage
FROM node:20-alpine AS builder

ARG APP_DIR
WORKDIR /workspace

ARG VITE_ORDERS_MFE_URL
ENV VITE_ORDERS_MFE_URL=${VITE_ORDERS_MFE_URL}

COPY shared-ui ./shared-ui
WORKDIR /workspace/app
COPY ${APP_DIR}/package*.json ./

RUN npm install

COPY ${APP_DIR}/ ./

RUN npm run build

# Production stage
FROM nginx:1.25-alpine

COPY --from=builder /workspace/app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
