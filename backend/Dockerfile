#Contents of Dockerfile
#Dockerfile to build an image which supports webscraping that uses selenium and others
FROM python:alpine3.17

#set working directory
WORKDIR /app

#copy requirements over
COPY requirements.txt .

#install all python dependencies
RUN pip3 install -Ur requirements.txt

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# environment variable to tell the backend whether its developement or production
ENV FLASK_ENV developement
#ENV FLASK_ENV production

# Expose port 5000 to the outside world for flask to use
EXPOSE 5000


# Run the main executable to start flask
CMD ["python", "main.py"]
#CMD ["./wait-for-it.sh", "bolt://cmpt370-db:7687","-t", "40", "--", "python", "main.py"]
