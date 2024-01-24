from flask import Flask
from api import api_blueprint
from torrent_manager import LibtorrentSession, load_config
import os
# Load configuration
config = load_config()

# Initialize libtorrent session
libtorrent_session = LibtorrentSession()

# Start the Flask app
if __name__ == "__main__":
    libtorrent_session.start_session()
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    port = int(os.environ.get('TORRENT_SERVER_API', 5000))
    debug_mode = os.environ.get('TORRENT_SERVER_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
