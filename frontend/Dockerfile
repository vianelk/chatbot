# Utiliser une image de Node.js
FROM node:18 AS build-stage

WORKDIR /app

# Copier les fichiers et installer les dépendances
COPY package.json package-lock.json ./
RUN npm install

# Copier le reste du projet
COPY . .

# Construire l'application
RUN npm run build

# Utiliser Nginx pour servir l'application
FROM nginx:alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
