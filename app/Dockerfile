FROM node:16.16-alpine

EXPOSE 3000

ARG PROJ_DIR=/app

RUN mkdir -p ${PROJ_DIR}

COPY ./app ${PROJ_DIR}

WORKDIR ${PROJ_DIR}

RUN ["chmod", "+x", "./entry.sh"]

ENTRYPOINT [ "sh", "./entry.sh" ]


