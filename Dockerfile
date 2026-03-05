FROM ghcr.io/cmlccie/agentic/python:latest

LABEL org.opencontainers.image.title="Pit Bot Agent"
LABEL org.opencontainers.image.description="Pit Bot Agent."
LABEL org.opencontainers.image.documentation="README.md"
LABEL org.opencontainers.image.source="https://github.com/gryphoncommand/pit-bot"

COPY main.py system_prompt.md fact_file.md README.md ./
RUN chmod +x main.py
RUN chown -R appuser:appuser /app
USER appuser

# Expose port 8000 for HTTP agent endpoints
EXPOSE 8000

ENTRYPOINT ["/app/main.py"]
CMD ["serve"]
