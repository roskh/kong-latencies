FROM python:3.12

COPY ./sleeping-requests.py /sleeping-requests.py

CMD ["python",  "-u", "/sleeping-requests.py"]