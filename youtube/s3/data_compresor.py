


def compress_photo(photo):
    from PIL import Image, ImageOps
    import io, os

    base_width = 360
    image = Image.open(photo)
    image = ImageOps.exif_transpose(image)
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    MAX_SIZE = (8000, 8000)
    if image.size[0] > MAX_SIZE[0] or image.size[1] > MAX_SIZE[1]:
        raise ValueError("Photo is too big!")

    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image = image_without_exif

    width_percent = (base_width / float(image.size[0]))
    hsize = int(float(image.size[1] * float(width_percent)))
    image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)

    original_name = getattr(photo, "name", "image.jpg")
    base_name, _ = os.path.splitext(original_name)
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP", quality=80)
    buffer.name = f"{base_name}_compressed.webp"

    buffer.seek(0)
    print(f"Image compressed: {buffer.name}")
    return buffer





ffmpeg_url = r"C:\Users\User\Downloads\ffmpeg-2025-10-12-git-0bc54cddb1-full_build\ffmpeg-2025-10-12-git-0bc54cddb1-full_build\bin\ffmpeg.exe"


def compresor_video_in_memory(file_like):
    import tempfile, os, io, ffmpeg

    resolutions = {
        "240p": ("426x240", "400k"),
        "360p": ("640x360", "800k"),
        "720p": ("1280x720", "2500k"),
        "1080p": ("1920x1080", "5000k"),
    }

    compressed_videos = {}
    ffmpeg_url = r"C:\Users\User\Downloads\ffmpeg-2025-10-12-git-0bc54cddb1-full_build\ffmpeg-2025-10-12-git-0bc54cddb1-full_build\bin\ffmpeg.exe"

    original_name = getattr(file_like, "name", "video.mp4")
    base_name, ext = os.path.splitext(original_name)

    file_like.seek(0)
    video_bytes = file_like.read()
    temp_in_path = tempfile.mktemp(suffix=".mp4")
    with open(temp_in_path, "wb") as f:
        f.write(video_bytes)

    print(f"[DEBUG] temp_in_path = {temp_in_path}, size = {os.path.getsize(temp_in_path)} bytes")

    try:
        probe = ffmpeg.probe(temp_in_path, cmd=ffmpeg_url.replace("ffmpeg.exe", "ffprobe.exe"))
        video_stream = next(s for s in probe["streams"] if s["codec_type"] == "video")
        orig_w = int(video_stream["width"])
        orig_h = int(video_stream["height"])
        print(f"[INFO] Original resolution: {orig_w}x{orig_h}")
    except Exception as e:
        print(f"[WARN] Could not detect resolution: {e}")
        orig_w, orig_h = 1920, 1080

    filtered_res = {}
    for label, (size, bitrate) in resolutions.items():
        w, h = map(int, size.split("x"))
        if w <= orig_w and h <= orig_h:
            filtered_res[label] = (size, bitrate)
        else:
            print(f"[SKIP] Skipping {label} ({size}) — larger than source {orig_w}x{orig_h}")

    if not filtered_res:
        print("[INFO] Source smaller than all predefined resolutions — keeping original")
        with open(temp_in_path, "rb") as f:
            buffer = io.BytesIO(f.read())
        buffer.name = original_name
        buffer.seek(0)
        compressed_videos["original"] = buffer
    else:
        for label, (size, bitrate) in filtered_res.items():
            temp_out_path = tempfile.mktemp(suffix=".mp4")

            cmd = (
                ffmpeg
                .input(temp_in_path)
                .output(
                    temp_out_path,
                    vcodec="libx264",
                    acodec="aac",
                    video_bitrate=bitrate,
                    s=size,
                    preset="ultrafast",
                    movflags="+faststart"
                )
                .overwrite_output()
            )

            print(f"[DEBUG] Starting compression for {label}")
            out, err = cmd.run(capture_stdout=True, capture_stderr=True, cmd=ffmpeg_url)
            print(f"[FFMPEG {label}] {err.decode(errors='ignore')[:200]}...")

            with open(temp_out_path, "rb") as f:
                buffer = io.BytesIO(f.read())


            buffer.name = f"{base_name}_{label}{ext}"

            buffer.seek(0)
            compressed_videos[f"{base_name}_{label}"] = buffer

            os.remove(temp_out_path)

    os.remove(temp_in_path)
    return compressed_videos


def compress_existing_videos(video_dict, ffmpeg_url):
    """
    Приймає словник {"label": BytesIO} і стискає кожне відео за попередньо заданими параметрами.
    Повертає словник {"label": BytesIO} вже стиснутих відео.
    """
    import tempfile, io, os, ffmpeg
    compressed_videos = {}

    for label, buffer in video_dict.items():
        buffer.seek(0)
        temp_in_path = tempfile.mktemp(suffix=".mp4")
        with open(temp_in_path, "wb") as f:
            f.write(buffer.read())

        temp_out_path = tempfile.mktemp(suffix=".mp4")

        cmd = (
            ffmpeg
            .input(temp_in_path)
            .output(
                temp_out_path,
                vcodec="libx264",      # або "libx265" для більшого стискання
                acodec="aac",
                crf=28,                # баланс між якістю і розміром
                preset="fast",         # краще стиснення
                tune="film",           # для звичайного відео
                audio_bitrate="128k",  # економія на звуці
                movflags="+faststart"
            )
            .overwrite_output()
        )

        print(f"[INFO] Compressing {label}...")
        cmd.run(quiet=True, cmd=ffmpeg_url)

        with open(temp_out_path, "rb") as f:
            new_buffer = io.BytesIO(f.read())
        new_buffer.name = label
        new_buffer.seek(0)
        compressed_videos[label] = new_buffer

        os.remove(temp_in_path)
        os.remove(temp_out_path)

    return compressed_videos