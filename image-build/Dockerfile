FROM jupyter/pyspark-notebook:latest

# Install additional dependencies if needed
# For example, if you need more libraries for your Spark jobs

# RUN pip install your_additional_libraries

# Copy any additional files or configurations if necessary
# COPY your_additional_files /path/in/container

# Expose the Jupyter port
EXPOSE 8888

# Set environment variables for Spark
ENV SPARK_HOME /usr/local/spark
ENV PATH $PATH:$SPARK_HOME/bin

# Any additional Spark configurations can be set here
# For example, if you have custom spark-defaults.conf
COPY spark-defaults.conf /usr/local/spark/conf/spark-defaults.conf

USER root

RUN sed -i 's/333JUPYTERUSER/jupyter/g' /usr/local/spark/conf/spark-defaults.conf
RUN echo 'jovyan:password' | chpasswd

# Start Jupyter Notebook upon container launch
CMD ["start-notebook.sh"]
