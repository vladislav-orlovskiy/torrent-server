import libtorrent as lt
import shelve
import yaml
import os

class LibtorrentSession:
    def __init__(self):
        self.session = lt.session()

    def start_session(self):
        # Restore previous torrents and resume their downloads
        self.restore_previous_torrents()

        # Additional session configuration can be added here
        pass

    def get_session(self):
        return self.session

    def restore_previous_torrents(self):
        with get_torrents_db() as db:
            for torrent_id, torrent_data in db.items():
                magnet_link = torrent_data.get('magnet_link')
                download_dir = torrent_data.get('download_dir')
                upload_speed = torrent_data.get('upload_speed')
                download_speed = torrent_data.get('download_speed')
                user_paused = torrent_data.get('user_paused')

                # Create Torrent object and resume download only if not paused by the user
                if magnet_link and not user_paused:
                    torrent = Torrent(magnet_link, download_dir, upload_speed, download_speed)
                    torrent.start_download()
                    self.session.add_torrent(torrent.handle)

class Torrent:
    def __init__(self, magnet_link, libtorrent_session, download_dir, upload_speed, download_speed):
        self.magnet_link = magnet_link
        self.session = libtorrent_session.get_session()
        self.download_dir = download_dir
        self.handle = self.session.add_torrent(
            dict(save_path=download_dir, url=magnet_link)
        )
        self.paused = False
        self.upload_speed = upload_speed
        self.download_speed = download_speed

        # Set custom upload and download speeds
        self.set_custom_speeds()

    def __getstate__(self):
        # Exclude the 'session' attribute from the serialized state
        exclude_dict = ["session", "handle"]
        return {k: v for k, v in self.__dict__.items() if k not in exclude_dict}

    def get(self, key):
        print(self)
        # Check if the key exists as an attribute and return its value
        return getattr(self, key, None)

    def set_session(self, session):
        self.session = session.get_session()
    def set_handle(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
        self.handle = self.session.add_torrent(
            dict(save_path=self.download_dir, url=self.magnet_link)
        )
    def set_custom_speeds(self):
        settings = self.session.get_settings()
        print(settings)
        if self.upload_speed:
            settings["upload_rate_limit"] = self.upload_speed * 1024  # Convert to bytes
        if self.download_speed:
            settings["download_rate_limit"] = self.download_speed * 1024  # Convert to bytes
        self.session.apply_settings(settings)

    def start_download(self):
        self.handle.resume()
        self.paused = False

    def pause_download(self):
        self.handle.pause()
        self.paused = True

    def play_download(self):
        if self.paused:
            self.start_download()

    def stop_download(self):
        self.session.remove_torrent(self.handle)

    def get_progress(self):
        status = self.handle.status()
        return status.progress * 100 if status.progress >= 0 else 0

    def get_status(self):
        status = self.handle.status()
        return {
            'progress': status.progress * 100 if status.progress >= 0 else 0,
            'state': str(status.state),
            'download_rate': status.download_rate,
            'upload_rate': status.upload_rate,
            'num_peers': status.num_peers,
        }

def get_torrents_db():
    config = load_config()
    return shelve.open(config["shell_file"])

def save_torrent(torrent_id, torrent):
    with get_torrents_db() as db:
        db[torrent_id] = torrent

def delete_torrent(torrent_id):
    with get_torrents_db() as db:
        if torrent_id in db:
            del db[torrent_id]

def get_torrent(torrent_id, session):
    with get_torrents_db() as db:
        if torrent_id in db:
            torrent = db.get(torrent_id)
            torrent.set_session(session)
            torrent.set_handle()
            return torrent
        else: return None

def load_config():
    config_path = os.environ.get('TORRENT_SERVER_CONFIG', 'config.yaml')
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)