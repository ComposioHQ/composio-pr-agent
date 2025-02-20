FROM composio/composio:latest

USER root
RUN chmod 755 /root/entrypoint.sh

RUN pip install swekit[langgraph]
RUN pip install -U composio-core --pre
# Create and set ownership of working directory
RUN mkdir -p /composio-pr-agent
WORKDIR /composio-pr-agent

COPY . .

ENTRYPOINT [ "python", "main.py" ]