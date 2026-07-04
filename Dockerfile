FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Isolate update loops and force-install full font architectures along with core runtime utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    dbus \
    dbus-x11 \
    python3 \
    python3-pip \
    python3-pyqt6 \
    python3-pyqt6.qtwebengine \
    fontconfig \
    fonts-liberation \
    fonts-wine \
    libgl1 \
    libglx-mesa0 \
    libegl1 \
    libgles2 \
    libglib2.0-0 \
    libnss3 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libfontconfig1 \
    libfreetype6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libsm6 \
    libice6 \
    libasound2t64 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libxkbfile1 \
    libgssapi-krb5-2 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Move the Windows structural configuration layout map into position
COPY local.conf /etc/fonts/local.conf
RUN fc-cache -f -v

# Set up clean system locales
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Extract Widevine CDM components using exact internal sub-path mapping
RUN mkdir -p /usr/lib/qt6/plugins/ppapi && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg-deb -x google-chrome-stable_current_amd64.deb /tmp/chrome_unpack && \
    cp /tmp/chrome_unpack/opt/google/chrome/WidevineCdm/_platform_specific/linux_x64/libwidevinecdm.so /usr/lib/qt6/plugins/ppapi/ && \
    rm -rf google-chrome-stable_current_amd64.deb /tmp/chrome_unpack

WORKDIR /app
COPY app/ .

CMD ["python3", "clean_browser.py"]
