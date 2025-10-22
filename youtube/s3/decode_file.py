from urllib.parse import urlparse
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from youtube.models import Video
import boto3


CHUNK_SIZE = 8192

def parse_s3_url(s3_url: str):

    parsed = urlparse(s3_url)
    host_parts = parsed.netloc.split(".")
    bucket = host_parts[0]
    key = parsed.path.lstrip("/")
    return bucket, key


def stream_from_s3(bucket, key, range_header=None):

    s3 = boto3.client('s3')

    range_str = None
    if range_header:
        byte_range = range_header.replace('bytes=', '').split('-')
        start = int(byte_range[0])
        end = int(byte_range[1]) if byte_range[1] else ''
        range_str = f"bytes={start}-{end}"

    params = {'Bucket': bucket, 'Key': key}
    if range_str:
        params['Range'] = range_str
    response = s3.get_object(**params)

    body = response['Body']

    for chunk in iter(lambda: body.read(CHUNK_SIZE), b''):
        yield chunk
    body.close(),
    return response


def stream_video(request, video_slug):

    video = get_object_or_404(Video, slug=video_slug)
    print(f"DEBUG Video {video}")
    video_url = video.url_video
    s3_bucket, s3_key = parse_s3_url(video_url)

    range_header = request.headers.get('Range', None)

    s3 = boto3.client('s3')
    params = {'Bucket': s3_bucket, 'Key': s3_key}
    if range_header:
        byte_range = range_header.replace('bytes=', '').split('-')
        start = int(byte_range[0])
        end = int(byte_range[1]) if byte_range[1] else ''
        params['Range'] = f"bytes={start}-{end}"

    s3_response = s3.get_object(**params)
    body = s3_response['Body']

    def stream():
        for chunk in iter(lambda: body.read(CHUNK_SIZE), b''):
            yield chunk
        body.close()

    status_code = 206 if range_header else 200

    response = StreamingHttpResponse(stream(), status=status_code, content_type='video/mp4')
    response["Accept-Ranges"] = "bytes"

    if "ContentRange" in s3_response:
        response["Content-Range"] = s3_response["ContentRange"]
    if "ContentLength" in s3_response:
        response["Content-Length"] = s3_response["ContentLength"]

    return response















