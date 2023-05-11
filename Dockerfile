FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV TZ=Asia/Taipei
EXPOSE 8000
CMD [ "python","-u", "app.py" ]
