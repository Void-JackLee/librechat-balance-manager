FROM node:20-alpine

RUN apk upgrade --no-cache
RUN apk add --no-cache python3 py3-pip uv

WORKDIR /app

# init backend

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

COPY api ./api
COPY config ./config
COPY .python-version ./
COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync

# init frontend
COPY public ./public
COPY src ./src
COPY *.html ./
COPY *.json ./
COPY *.ts ./

RUN npm install

EXPOSE 3010

COPY entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]