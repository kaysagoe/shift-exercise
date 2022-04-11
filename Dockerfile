FROM python:3.9

WORKDIR /project

COPY ./requirements.txt /project/requirements.txt

RUN pip install -r /project/requirements.txt
RUN curl https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words -o /usr/share/dict/words

ENV word_list_path=/usr/share/dict/words

COPY . /project/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]