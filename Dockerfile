FROM python:3.8.5-buster

# DIRECTORY FOR OUR APP
WORKDIR .
# INSTALL DEPENDENCIERS
COPY requirements.txt .
RUN pip install -r requirements.txt
#COPy source CODE

COPY . .

#   RUN APPLICATION

CMD ["python","main.py"]
