FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json ./
COPY apps/web/package.json ./apps/web/package.json
RUN npm install
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/web/node_modules ./apps/web/node_modules
COPY . .
RUN npm run build --workspace @solarrecover/web
EXPOSE 3000
CMD ["npm", "run", "start", "--workspace", "@solarrecover/web"]
