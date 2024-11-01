# run.py
import sys

sys.path.append('.')

from server.app import create_app

if __name__ == "__main__":
    import os

    app = create_app()
    port = int(os.environ.get("PORT", 5555))
    app.run(host="0.0.0.0", port=port, debug=True)
