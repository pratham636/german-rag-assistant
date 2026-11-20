import logging

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("rag")
log.setLevel(logging.INFO)                     # your own logs: INFO