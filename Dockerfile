FROM python:3.9

RUN apt-get update && apt-get install -y unzip

WORKDIR /app

COPY requirements.txt .

RUN apt-get install -y  gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libgbm1 libu2f-udev

RUN apt-get install -y tzdata
RUN apt-get install -yqq unzip

# #download and install chrome
# # RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN wget -q "https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && unzip /tmp/chromedriver.zip -d /usr/bin/ && rm /tmp/chromedriver.zip
# # RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
# RUN apt-get -fy install

# # Set display port as an environment variable
# ENV DISPLAY=:99

# RUN chmod +x /usr/bin/chromedriver 

# # Install chrome driver
# RUN apt-get update && apt-get install -yq unzip libgconf-2-4 chromium && \
#     wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip" && \
#     unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
#     chmod +x /usr/local/bin/chromedriver

RUN apt-get -y install chromium
RUN apt-get update && apt-get install -y

# Create the 'drivers' folder and move the ChromeDriver
# RUN mkdir -p drivers
# RUN mv /usr/local/bin/chromedriver drivers


COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5005"]


