from pathlib import Path
import math, time
from PIL import Image, UnidentifiedImageError
from django.conf import settings
from django.core.cache import cache
from .models import Slide, ProcessingJob

TILE_SIZE = 256
METRICS = {'tile_requests': 0, 'cache_hits': 0, 'cache_misses': 0, 'tile_latency_total_ms': 0.0}

def pyramid_root(slide): return Path(settings.MEDIA_ROOT) / 'pyramids' / str(slide.id)

def validate_image(upload):
    if upload.size > settings.MAX_UPLOAD_SIZE: raise ValueError('File exceeds configured upload size limit.')
    try:
        image = Image.open(upload); image.verify(); upload.seek(0)
        image = Image.open(upload)
        if image.format not in {'PNG', 'JPEG', 'TIFF', 'WEBP'}: raise ValueError('Unsupported image format. Use PNG, JPEG, TIFF, or WebP.')
        return image.size, image.format
    except (UnidentifiedImageError, OSError): raise ValueError('The uploaded file is corrupted or is not a supported image.')

def build_pyramid(slide):
    started = time.perf_counter(); slide.status = Slide.Status.PROCESSING; slide.save(update_fields=['status'])
    try:
        with Image.open(slide.image.path) as source:
            source = source.convert('RGB'); width, height = source.size; levels=[]
            current = source
            while True:
                levels.append(current.copy())
                if max(current.size) <= TILE_SIZE: break
                current = current.resize((max(1, current.width // 2), max(1, current.height // 2)), Image.Resampling.LANCZOS)
            root = pyramid_root(slide); root.mkdir(parents=True, exist_ok=True)
            for index, image in enumerate(reversed(levels)):
                level_dir = root / str(index); level_dir.mkdir(exist_ok=True)
                for y in range(math.ceil(image.height / TILE_SIZE)):
                    for x in range(math.ceil(image.width / TILE_SIZE)):
                        image.crop((x*TILE_SIZE, y*TILE_SIZE, min((x+1)*TILE_SIZE,image.width), min((y+1)*TILE_SIZE,image.height))).save(level_dir / f'{x}_{y}.jpg', quality=88, optimize=True)
            slide.width, slide.height, slide.pyramid_levels, slide.status = width, height, len(levels), Slide.Status.READY
            slide.save()
    except Exception:
        slide.status = Slide.Status.FAILED; slide.save(update_fields=['status']); raise
    finally:
        ProcessingJob.objects.create(slide=slide, kind='PYRAMID', status=slide.status, duration_ms=(time.perf_counter()-started)*1000)

def tile_path(slide, level, x, y): return pyramid_root(slide) / str(level) / f'{x}_{y}.jpg'

def record_tile(cache_hit, duration):
    METRICS['tile_requests'] += 1; METRICS['cache_hits' if cache_hit else 'cache_misses'] += 1; METRICS['tile_latency_total_ms'] += duration

def metrics():
    n=METRICS['tile_requests']; return {**METRICS, 'cache_hit_ratio': METRICS['cache_hits']/n if n else 0, 'average_tile_latency_ms': METRICS['tile_latency_total_ms']/n if n else 0}
