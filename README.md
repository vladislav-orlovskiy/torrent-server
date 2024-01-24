# Torrent Server

This is a simple Flask api server for managing torrent downloads using the libtorrent library.

## Configuration

### Environment Variables

- `TORRENT_SERVER_API`: Set the port for the Flask API. Default is `5000`.
- `TORRENT_SERVER_DEBUG`: Set to `True` for Flask debug mode, or `False` (default) otherwise.
- `TORRENT_SERVER_CONFIG`: Path to the configuration file. Default is `config.yaml`.

### Configuration File (config.yaml)

```yaml
download_dir: "./downloads"
default_upload_speed: 1000
default_download_speed: 1000

`download_dir`: The directory where downloaded torrents will be saved.
`default_upload_speed`: Default upload speed for new torrents in KB/s.
`default_download_speed`: Default download speed for new torrents in KB/s.

## API Documentation

### Add a Torrent

**Endpoint:**
```
POST /api/v1/torrent
```

**Request Body:**
```json
{
  "magnet_link": "magnet:?xt=urn:btih:..."
}
```

**Response:**
```json
{
  "message": "Torrent added successfully",
  "torrent_id": "1"
}
```

### Get All Torrents

**Endpoint:**
```
GET /api/v1/torrent
```

**Response:**
```json
{
  "torrent_ids": ["1", "2"]
}
```

### Delete a Torrent

**Endpoint:**
```
DELETE /api/v1/torrent/<torrent_id>
```

**Response:**
```json
{
  "message": "Torrent deleted successfully"
}
```

### Get Torrent Status

**Endpoint:**
```
GET /api/v1/torrent/<torrent_id>
```

**Response:**
```json
{
  "progress": 50,
  "state": "Downloading",
  "download_rate": 1024,
  "upload_rate": 512,
  "num_peers": 5
}
```

### Pause Torrent Download

**Endpoint:**
```
POST /api/v1/torrent/<torrent_id>/pause
```

**Response:**
```json
{
  "message": "Torrent download paused"
}
```

### Resume Torrent Download

**Endpoint:**
```
POST /api/v1/torrent/<torrent_id>/play
```

**Response:**
```json
{
  "message": "Torrent download resumed"
}
```

### Get Torrent Download Progress

**Endpoint:**
```
GET /api/v1/torrent/<torrent_id>/progress
```

**Response:**
```json
{
  "progress": 75
}
```

## MacOS development

Just use docker and Vagrant
