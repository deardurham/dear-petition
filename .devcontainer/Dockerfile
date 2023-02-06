FROM mcr.microsoft.com/devcontainers/python:0-3.8-bullseye

ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
RUN set -ex \
    && RUN_DEPS=" \
    postgresql-client-13 \
    " \
    && apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends $RUN_DEPS

# Install poppler pdftotext, based on xpdf3 (for parser mode V1)
RUN set -ex \
    && curl -k https://poppler.freedesktop.org/poppler-0.57.0.tar.xz | tar xJ \
    && chmod -R 755 ./poppler-0.57.0 \
    && cd ./poppler-0.57.0/ \
    && ./configure \
        --prefix=/tmp/poppler \
        --disable-shared \
        --enable-static \
        --enable-build-type=release \
        --enable-libopenjpeg=none \
        --enable-dctdecoder=none \
        --enable-shared=no \
    && make install \
    && cp /tmp/poppler/bin/pdftotext /usr/local/bin/pdftotext

# Install pdftotext
RUN set -ex \
    && wget --no-check-certificate https://dl.xpdfreader.com/xpdf-tools-linux-4.04.tar.gz \
    && tar -xvf xpdf-tools-linux-4.04.tar.gz \
    && cp xpdf-tools-linux-4.04/bin64/pdftotext /usr/local/bin/pdftotext-4
