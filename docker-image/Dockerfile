#Download base image ubuntu 16.04
FROM ubuntu:18.10

# Update Ubuntu Software repository
RUN apt-get update && \
    apt-get install -y gcc git curl wget make libncurses-dev flex bison gperf python python-pip python-setuptools python-serial python-cryptography python-future

# Download Espressif toolchain
ADD https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz /esp/ 
RUN tar -zxvf /esp/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz -C /esp

# Get esp 32 API/Libraries
RUN git clone --recursive https://github.com/espressif/esp-idf.git /esp/esp-idf

# Set env variables
ENV PATH="/esp/xtensa-esp32-elf/bin:${PATH}" \
    IDF_PATH="/esp/esp-idf"

# Install esp-idf python dependencies
RUN python -m pip install --user -r $IDF_PATH/requirements.txt


