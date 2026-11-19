# Copyright (c) 2026 Khalid Salman. SPDX-License-Identifier: Apache-2.0
"""Local media analysis; no silent model downloads or image generation."""
from __future__ import annotations
import wave
from pathlib import Path
from .core import Result, ValidationError, ConsentRequired, input_file, require, fingerprint


def image_analyze(*, image, config, detect_faces=True, **kwargs):
    cv2 = require('cv2', 'vision')
    p = input_file(image, config)
    import numpy as np
    encoded = np.fromfile(str(p), dtype=np.uint8)
    img = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if img is None:
        raise ValidationError('Cannot decode this image')
    h, w = img.shape[:2]
    if h*w > 40_000_000:
        raise ValidationError('Decoded image exceeds 40 megapixels')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = []
    if detect_faces:
        classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if classifier.empty():
            raise ValidationError('OpenCV face cascade unavailable')
        faces = [{'x': int(x), 'y': int(y), 'width': int(fw), 'height': int(fh)} for x, y, fw, fh in classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))]
    return Result('image.analyze', {'width': w, 'height': h, 'channels': 3, 'mean_rgb': cv2.mean(img)[:3][::-1], 'faces': faces, 'face_count': len(faces)}, 'opencv.HaarCascade', ['Face detection only, not identity recognition or general object detection. Detections can be wrong.'], {'input_sha256': fingerprint(p)})


def video_motion(*, video, config, min_area=300, max_frames=None, **kwargs):
    cv2 = require('cv2', 'vision')
    p = input_file(video, config)
    limit = config.max_video_frames if max_frames is None else int(max_frames)
    if limit <= 0 or limit > config.max_video_frames or float(min_area) <= 0:
        raise ValidationError('Invalid frame/area budget')
    cap = cv2.VideoCapture(str(p))
    if not cap.isOpened():
        raise ValidationError('Video cannot be opened; check codec support')
    rows = []
    previous = None
    fps = cap.get(cv2.CAP_PROP_FPS)
    try:
        while len(rows) < limit:
            ok, frame = cap.read()
            if not ok:
                break
            if frame.shape[0]*frame.shape[1] > 40_000_000:
                raise ValidationError('Decoded frame too large')
            gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (5, 5), 0)
            boxes = []
            changed = 0.0
            if previous is not None:
                mask = cv2.threshold(cv2.absdiff(previous, gray), 25, 255, cv2.THRESH_BINARY)[1]
                mask = cv2.dilate(mask, None, iterations=2)
                changed = float(cv2.countNonZero(mask) / mask.size)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                boxes = [dict(zip(('x', 'y', 'width', 'height'), map(int, cv2.boundingRect(c)))) for c in contours if cv2.contourArea(c) >= float(min_area)]
            i = len(rows)
            rows.append({'frame': i, 'time_seconds': i/fps if fps > 0 else None, 'changed_fraction': changed, 'boxes': boxes})
            previous = gray
        if not rows:
            raise ValidationError('Video contains no readable frames')
        has_more = cap.read()[0] if len(rows) == limit else False
    finally:
        cap.release()
    return Result('video.motion', {'fps': fps, 'processed_frames': len(rows), 'truncated': bool(has_more), 'rows': rows}, 'opencv.frame-difference', ['Motion regions only, not action understanding, person identification or persistent tracking. Camera movement can trigger detections.'], {'input_sha256': fingerprint(p)})


def audio_info(*, audio, config, **kwargs):
    p = input_file(audio, config)
    try:
        with wave.open(str(p), 'rb') as wav:
            rate, count = wav.getframerate(), wav.getnframes()
            data = {'channels': wav.getnchannels(), 'sample_rate': rate, 'sample_width_bytes': wav.getsampwidth(), 'frames': count, 'duration_seconds': count/rate, 'compression': wav.getcomptype()}
    except (wave.Error, EOFError) as exc:
        raise ValidationError('audio.info accepts PCM WAV, not arbitrary audio codecs') from exc
    return Result('audio.info', data, 'stdlib.wave', provenance={'input_sha256': fingerprint(p)})


def transcribe(*, audio, config, model_path=None, language=None, **kwargs):
    fw = require('faster_whisper', 'speech')
    p = input_file(audio, config)
    model = model_path or config.model
    if not model:
        raise ValidationError('Provide model_path= to a local CTranslate2 Whisper directory')
    if not Path(model).is_dir() and not config.allow_model_download:
        raise ConsentRequired('Model downloads disabled. Supply a local model directory or explicitly set allow_model_download=True after license review.')
    engine = fw.WhisperModel(str(model), device='cpu', compute_type='int8', local_files_only=not config.allow_model_download)
    segments, info = engine.transcribe(str(p), language=language)
    rows = [{'start': s.start, 'end': s.end, 'text': s.text} for s in segments]
    return Result('speech.transcribe', {'language': info.language, 'text': ''.join(r['text'] for r in rows).strip(), 'rows': rows}, 'faster-whisper.cpu-int8', provenance={'input_sha256': fingerprint(p), 'model': str(model)})


def objects_detect(*, image, model_path, config, **kwargs):
    """User-provided local Transformers model; remote custom code is always disabled."""
    transformers = require('transformers', 'objects')
    input_file(image, config)
    if not Path(model_path).is_dir():
        raise ValidationError('Provide a reviewed local Transformers object-detection model directory. Automatic downloads are not implemented for this adapter.')
    processor = transformers.AutoImageProcessor.from_pretrained(str(model_path), local_files_only=True, trust_remote_code=False)
    model = transformers.AutoModelForObjectDetection.from_pretrained(str(model_path), local_files_only=True, trust_remote_code=False, use_safetensors=True)
    torch = require('torch', 'objects')
    PIL = require('PIL.Image', 'objects')
    with PIL.open(image) as im:
        if im.width*im.height > 40_000_000:
            raise ValidationError('Image exceeds pixel budget')
        im = im.convert('RGB')
        inputs = processor(images=im, return_tensors='pt')
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
        processed = processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=torch.tensor([[im.height, im.width]]))[0]
    rows = [{'label': model.config.id2label.get(int(l), str(int(l))), 'score': float(s), 'box_xyxy': b.tolist()} for l, s, b in zip(processed['labels'], processed['scores'], processed['boxes'])]
    return Result('image.objects', {'rows': rows}, 'transformers.local-object-detection', ['Model license and accuracy depend on your chosen weights.'], {'model_path': str(model_path)})
