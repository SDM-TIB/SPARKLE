# Use a Python base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /SPARKLE

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git

# Clone the PyKEEN repository from GitHub
RUN git clone https://github.com/pykeen/pykeen.git


# Install PyKEEN and its dependencies
#RUN pip install -r /SPARKLE/pykeen/requirements.txt
RUN python -m pip install pykeen
RUN python -m pip install pyDatalog
RUN python -m pip install pandas

# Set the entrypoint to the Python interpreter
ENTRYPOINT ["python"]


