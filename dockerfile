FROM python:3.7.4 AS base
WORKDIR /luyuntongimagclassify
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install MarkupSafe==1.1.1 -i https://pypi.tuna.tsinghua.edu.cn/simple 
EXPOSE 10539
COPY ./ .
ENTRYPOINT  python img_interface_job.py 
