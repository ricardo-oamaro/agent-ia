# =========================
# Etapa 1: Build com Node
# =========================
# FROM node:20 AS build
# WORKDIR /app

# # Copia arquivos de dependência
# COPY package*.json ./

# # Instala dependências (sem pacotes opcionais)
# RUN npm install --no-optional

# # Instala manualmente rollup correto por arquitetura (evita erro no ARM)
# RUN ARCH="$(uname -m)" && \
#     if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then \
#       npm install --no-save @rollup/rollup-linux-x64-gnu || true; \
#     elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then \
#       npm install --no-save @rollup/rollup-linux-arm64-gnu || true; \
#     else \
#       echo "Unknown arch: $ARCH — skipping native rollup install"; \
#     fi

# # Copia o restante do código
# COPY . .

# # 🔹 Declara e injeta variável VITE_API_URL durante o build
# ARG VITE_API_URL
# ENV VITE_API_URL=${VITE_API_URL}
# RUN echo "Building frontend with API URL: $VITE_API_URL"
# RUN npm run build

# # =========================
# # Etapa 2: Servir com Nginx
# # =========================
# FROM nginx:1.27-alpine

# # Copia build do frontend para o nginx
# COPY --from=build /app/dist /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]


FROM node:20 AS build
WORKDIR /app

COPY package*.json ./
RUN npm install --no-optional

COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

RUN echo "🚀 Building frontend with API URL: $VITE_API_URL"
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
