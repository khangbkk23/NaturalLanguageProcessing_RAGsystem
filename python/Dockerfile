# Written by: Hung Vo (thanhhungqb@gmail.com)
# 
# can be used by wide project of DL (demo)
#

# =====================================================================
# base-image maybe share for quicker build and save storage
# thanhhungqb/python-builder:ver
# =====================================================================
FROM python:3.8-slim-bullseye as builder

LABEL author="Hung Vo"
LABEL description="NLP Assignment Docker Image - Builder Stage"

ENV TZ=Asia/Ho_Chi_Minh
ENV DEBIAN_FRONTEND=noninteractive

# 1. Cài đặt các gói build cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    locales \
    && rm -rf /var/lib/apt/lists/*

# 2. Thiết lập Locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# 3. Tạo venv và cài đặt dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /src/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --upgrade pip && \
    pip install -r /src/requirements.txt

FROM python:3.8-slim-bullseye as runtime

LABEL author="Student"
LABEL description="NLP Assignment Docker Image - Runtime Stage"

ENV TZ=Asia/Ho_Chi_Minh
ENV DEBIAN_FRONTEND=noninteractive

# 1. Cài đặt Runtime dependencies
RUN apt-get update && apt-get -y --no-install-recommends install \
    locales \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# 2. Thiết lập Locale
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# 3. Copy môi trường ảo Python đã build xong
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 4. Copy mã nguồn
COPY . /src/
WORKDIR /src/

ENV PYTHONPATH="/src"
RUN mkdir -p /src/output

# 5. Lệnh chạy mặc định
CMD ["python3", "-m", "hcmut.iaslab.nlp.app.main"]