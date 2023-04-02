FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pyqt5 python3-pyqt5.qtwebengine xauth openssh-server python3-pip python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the display environment variable
ENV DISPLAY=:0

# Create the sshd_config file and add X11 forwarding settings
RUN touch /etc/ssh/sshd_config && \
    echo "X11UseLocalhost no" >> /etc/ssh/sshd_config && \
    echo "X11Forwarding yes" >> /etc/ssh/sshd_config

# Start the ssh service
CMD ["service", "ssh", "start"]

# Copy the PyQt5 Python GUI application to the container
COPY ./ /app

# Install the libraries listed in requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Set the working directory to /app
WORKDIR /app

CMD ["python3", "pyqt5.py"]