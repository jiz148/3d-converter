FROM python:3.7

# system update
RUN apt-get update && \
    apt install libgl1-mesa-glx -y

# Create app folder
RUN mkdir -p /var/app
WORKDIR /var/app

# Copy app files into app folder
COPY . /var/app

# Install requirements
RUN pip install --upgrade pip && pip install -r requirements.txt

# ENV
ENV QT_DEBUG_PLUGINS=1

# run app
CMD ["pip", "list"]
CMD ["python", "./3d-converter.py"]
