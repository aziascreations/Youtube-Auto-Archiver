FROM python:alpine

# Installing dependencies
# * 'g++', 'make' -> Compiling some dependencies.
# * 'py3-lxml' -> Pre-compiled module, allows you to ignore compilation errors.

# Used to compile lxml for streamlink  (Not used for the moment)
# RUN apk add --no-cache libxslt-dev libxml2-dev

# Used for compiling streamlink and its dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache g++ make py3-lxml ffmpeg

# Installing required Python packages
RUN pip install --upgrade streamlink==2.3.0 yt-dlp==2021.12.01

# Removing packages that are no longer needed and were used for compiling streamlink and its dependencies
# * Some are left however: libgcc, libstdc++, libgomp and gmp
# * Reduces the HDD usage from 198 MiB to 127 MiB for these packages
RUN apk del g++ make

# Reading the build arguments
# * BUID -> Build UID
# * BGID -> Build GID
ARG BUID=1000
ARG BGID=1000

# Copying the app's files to the container
ADD --chown=BUID:BGID . /app

# Running the application
# * Thanks to jdpus for the "-u" flag, it fixes the output (https://stackoverflow.com/a/29745541/4135541)
WORKDIR /app
USER $BUID:$BGID
CMD ["python", "-u", "/app/app.py"]

# Used for debugging
#CMD ["tail", "-f", "/dev/null"]
