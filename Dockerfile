FROM mi_environment:v7
MAINTAINER MZC <724686158@qq.com>
COPY project.tar.gz /app/project.tar.gz
RUN tar -xzvf /app/project.tar.gz --strip-components 1 \
    && rm /app/project.tar.gz
ENTRYPOINT ["python2"]
CMD ["/app/start.py"]
