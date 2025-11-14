FROM ubuntu:latest

ENV PORT=3001
ENV CONFIG_PATH="/home/backend/config/config.yml"
ENV TEMPLATE_PATH="/home/backend/template/template.txt"
ENV DATA_PATH="/home/data/cpp"

EXPOSE 3001

RUN apt-get update --fix-missing && apt-get upgrade -y

RUN apt-get install -y sudo nodejs npm python3-pip python3-venv


RUN mkdir -p $DATA_PATH
RUN mkdir /home/backend

WORKDIR $DATA_PATH
COPY cpp .

WORKDIR /home/backend
COPY backend .

RUN python3 -m venv env
ENV PATH="env/bin:$PATH"

RUN pip install -r requirements.txt

RUN npm install

RUN python3 ./scripts/collect_data.py

ENTRYPOINT ["npm", "start"]