FROM postgres:17-bookworm

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y locales locales-all wget && \
    localedef -i cs_CZ -c -f UTF-8 -A /usr/share/locale/locale.alias cs_CZ.UTF-8 && \
    wget -qO- "https://postgres.cz/files/czech.tar.gz" | tar xzf - -C /usr/share/postgresql/17/tsearch_data --strip 1
ENV POSTGRES_INITDB_ARGS="--locale=cs_CZ.UTF-8 --locale-provider=icu --icu-locale=cs_CZ.UTF-8 --lc-messages=en_US.UTF-8"
COPY ./init-user-db.sh /docker-entrypoint-initdb.d/.
