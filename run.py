#!/usr/bin/env python3
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", os.environ.get("PORT", "5001")))
    use_reloader = os.environ.get("FLASK_RELOADER", "").lower() in ("1", "true", "yes")
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        use_reloader=use_reloader,
    )
