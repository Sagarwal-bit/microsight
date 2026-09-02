import cv2, numpy as np
from PIL import Image
from .models import AnalysisRegion, DetectedObject
from apps.slides.models import Slide

def quality(image):
    rgb=np.asarray(image.convert('RGB')); gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
    brightness=float(gray.mean()); contrast=float(gray.std()); focus=float(cv2.Laplacian(gray,cv2.CV_64F).var()); saturation=float(cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)[:,:,1].mean())
    blur=float(1/(1+focus)); artifact=float(np.mean((gray<8)|(gray>247)))
    overall=float(np.mean([min(brightness/255,1),min(contrast/64,1),min(focus/500,1),1-artifact]))
    return {'focus_score':focus,'brightness_score':brightness,'contrast_score':contrast,'saturation_score':saturation,'artifact_score':artifact,'overall_score':overall,'label':'heuristic metrics; not clinical quality scores'}
def analyze(slide):
    with Image.open(slide.image.path) as img:
        rgb=np.asarray(img.convert('RGB')); h,w=rgb.shape[:2]; gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
        AnalysisRegion.objects.filter(slide=slide).delete(); DetectedObject.objects.filter(slide=slide).delete()
        step=max(128,min(w,h)//8)
        regions=[]
        for y in range(0,h,step):
            for x in range(0,w,step):
                crop=gray[y:y+step,x:x+step]; texture=cv2.Laplacian(crop,cv2.CV_64F).var(); darkness=1-crop.mean()/255
                regions.append(AnalysisRegion(slide=slide,x=x,y=y,width=crop.shape[1],height=crop.shape[0],score=float(min(1,0.55*darkness+0.45*min(texture/700,1)))))
        AnalysisRegion.objects.bulk_create(regions)
        _,mask=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU); count,_,stats,_=cv2.connectedComponentsWithStats(mask)
        objects=[DetectedObject(slide=slide,x=int(a[0]),y=int(a[1]),width=int(a[2]),height=int(a[3]),area=float(a[4]),score=float(min(1,a[4]/2000))) for a in stats[1:] if 25<=a[4]<=10000]
        DetectedObject.objects.bulk_create(objects[:1000])
    slide.status=Slide.Status.ANALYZED; slide.save(update_fields=['status'])
