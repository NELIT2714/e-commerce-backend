import os

import uvicorn
from project import app

if __name__ == "__main__":
    log_level = "debug" if os.getenv("MODE") else "info"
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=log_level)
