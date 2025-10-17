# Etapa 1: Build do React com npm
FROM node:20-slim AS build

WORKDIR /app

# Copia dependências
COPY package*.json ./
RUN npm install

# Copia o restante do código
COPY . .

# Executa o build (gera /dist)
RUN npm run build

# Etapa 2: Servir com Nginx
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
