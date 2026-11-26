import json
import logging
import sys

from config.log import JsonFormatter


def test_json_formatter_emits_one_parseable_line_with_exception() -> None:
    try:
        raise ValueError("boom")
    except ValueError:
        record = logging.LogRecord(
            "app", logging.ERROR, __file__, 1, "failed %s", ("job",), sys.exc_info()
        )

    line = JsonFormatter().format(record)

    assert "\n" not in line
    payload = json.loads(line)
    assert payload["level"] == "ERROR"
    assert payload["logger"] == "app"
    assert payload["message"] == "failed job"
    assert "ValueError: boom" in payload["exception"]
    assert payload["time"].endswith("+00:00")
