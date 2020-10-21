FROM trestletech/plumber

# install the randomForest package
RUN R -e 'install.packages(c("jsonlite"))'

# copy model and scoring script
RUN mkdir /data
COPY combine_data.rds /data
COPY plumber.R /data
WORKDIR /data

# plumb and run server
EXPOSE 8000
ENTRYPOINT ["R", "-e", \
    "pr <- plumber::plumb('/data/plumber.R'); pr$run(host='0.0.0.0', port=8000)"]