# Create your views here.
from models import *

def test(request):
    f = Foo.objects.get(pk=1)
    f2 = Foo1(f)
    f2.save()
    return