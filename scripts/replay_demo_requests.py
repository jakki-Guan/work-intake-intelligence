from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_URL = "http://127.0.0.1:8000/predict"


def post_json(url: str, payload: dict) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url=url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=10) as response:
        body = response.read().decode("utf-8")
        return response.status, body


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("scripts/demo_requests.json")
    requests_list = json.loads(input_path.read_text(encoding="utf-8"))

    success = 0
    for i, payload in enumerate(requests_list, start=1):
        try:
            status_code, body = post_json(API_URL, payload)
            print(f"[{i}] status={status_code}")
            if 200 <= status_code < 300:
                success += 1
        except HTTPError as e:
            print(f"[{i}] status={e.code}")
            print(e.read().decode("utf-8"))
        except URLError as e:
            print(f"[{i}] request failed: {e}")

    print(f"\nFinished. Successful calls: {success}/{len(requests_list)}")


if __name__ == "__main__":
    main()