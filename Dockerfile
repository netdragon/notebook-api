FROM python:3.9-buster
#FROM registry.cn-hangzhou.aliyuncs.com/os-cxb/centos1406-python-base:0.3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 8008

# Define environment variable
ENV NAME my-notebook

# Install any needed packages specified in requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
#RUN pip3 install -r requirements.txt

CMD ["python", "/app/auth-view.py"]
