from flask import Flask, jsonify, request, Blueprint, render_template
from torrent_manager import Torrent, get_torrents_db, save_torrent, delete_torrent, get_torrent
api_blueprint = Blueprint('api',__name__)
from main import libtorrent_session, config
@api_blueprint.route('/api/v1/torrent', methods=['GET'])
def get_all_torrents():
    all_torrent_ids = list(get_torrents_db().keys())
    return jsonify({'torrent_ids': all_torrent_ids}), 200

@api_blueprint.route('/api/v1/torrent', methods=['POST'])
def add_torrent():
    data = request.get_json()
    magnet_link = data.get('magnet_link')

    if not magnet_link:
        return jsonify({'error': 'Magnet link is required'}), 400

    torrent = Torrent(
        magnet_link, libtorrent_session, config['download_dir'],
        config['default_upload_speed'], config['default_download_speed']
    )
    torrent_id = str(len(get_torrents_db()) + 1)
    save_torrent(torrent_id, torrent)
    torrent.play_download()  # Start download by default

    return jsonify({'message': 'Torrent added successfully', 'torrent_id': torrent_id}), 201

@api_blueprint.route('/api/v1/torrent/<torrent_id>', methods=['DELETE'])
def delete_torrent_route(torrent_id):
    torrent = get_torrent(torrent_id, libtorrent_session)
    if torrent:
        torrent.stop_download()
        delete_torrent(torrent_id)
        return jsonify({'message': 'Torrent deleted successfully'}), 200
    else:
        return jsonify({'error': 'Torrent not found'}), 404

@api_blueprint.route('/api/v1/torrent/<torrent_id>', methods=['GET'])
def get_torrent_status(torrent_id):
    torrent = get_torrent(torrent_id, libtorrent_session)
    if torrent:
        status = torrent.get_status()
        return jsonify(status), 200
    else:
        return jsonify({'error': 'Torrent not found'}), 404

@api_blueprint.route('/api/v1/torrent/<torrent_id>/pause', methods=['POST'])
def pause_torrent(torrent_id):
    torrent = get_torrent(torrent_id, libtorrent_session)
    if torrent:
        torrent.pause_download()
        save_torrent(torrent_id, torrent)
        return jsonify({'message': 'Torrent download paused'}), 200
    else:
        return jsonify({'error': 'Torrent not found'}), 404

@api_blueprint.route('/api/v1/torrent/<torrent_id>/play', methods=['POST'])
def play_torrent(torrent_id):
    torrent = get_torrent(torrent_id, libtorrent_session)
    if torrent:
        torrent.play_download()
        save_torrent(torrent_id, torrent)
        return jsonify({'message': 'Torrent download resumed'}), 200
    else:
        return jsonify({'error': 'Torrent not found'}), 404

@api_blueprint.route('/api/v1/torrent/<torrent_id>/progress', methods=['GET'])
def get_torrent_progress(torrent_id):
    torrent = get_torrent(torrent_id, libtorrent_session)
    if torrent:
        progress = torrent.get_progress()
        return jsonify({'progress': progress}), 200
    else:
        return jsonify({'error': 'Torrent not found'}), 404
