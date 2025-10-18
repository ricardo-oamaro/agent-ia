# Etapa 1: Build do React com npm
FROM node:20-bullseye AS build

WORKDIR /app

# Copia apenas os arquivos de configuração de pacotes primeiro
COPY package*.json ./

# Remove o package-lock existente para evitar problemas de dependência
RUN rm -f package-lock.json

# Configura para pular os binários nativos do Rollup
ENV ROLLUP_SKIP_NATIVES=true

# Instala dependências com --no-optional para evitar pacotes específicos de plataforma
RUN npm install --no-optional

# Instala manualmente o pacote necessário para GNU/Linux x64 
# (que parece ser a plataforma que está tentando usar)
RUN ARCH="$(uname -m)" && \
    if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then \
      npm install --no-save @rollup/rollup-linux-x64-gnu || true; \
    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then \
      npm install --no-save @rollup/rollup-linux-arm64-gnu || true; \
    else \
      echo "Unknown arch: $ARCH — skipping native rollup install"; \
    fi

# Copia o restante do código
COPY . .

ARG VITE_API_URL=http://backend:8000
ENV VITE_API_URL=${VITE_API_URL}

# Executa o build com flag adicional para log verboso se necessário
RUN NODE_OPTIONS="--max-old-space-size=4096" npm run build

# Etapa 2: Servir com Nginx
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]