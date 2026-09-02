from io import BytesIO
from django.test import TestCase
from PIL import Image
from apps.slides.services import validate_image
from apps.analysis.services import quality
class CoreTests(TestCase):
 def test_valid_png(self):
  f=BytesIO();Image.new('RGB',(20,20),'white').save(f,'PNG');f.name='demo.png';f.size=len(f.getvalue());f.seek(0);self.assertEqual(validate_image(f)[1],'PNG')
 def test_quality_reports_heuristics(self): self.assertIn('heuristic',quality(Image.new('RGB',(30,30),'white'))['label'])
