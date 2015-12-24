from django.shortcuts import render
from socket import gethostname
from .models import *

def in_school(req):
    school_ips = ( '202.94.70.25', '103.24.77.25' )

    for f in ( 'REMOTE_ADDR', 'HTTP_X_FORWARDED_FOR' ):
        if f in req.META: addr = req.META[f]

    return ( addr in school_ips )

def img_url_fx(in_sch):

    if in_sch:
        return lambda i, s: "http://pxy.randna.me:3000/%s?%s" % (i,s)
    else:
        return lambda i, s: "http://pics.dmm.co.jp/digital/video/%s/%s%s.jpg" % (i,i,s)

def vid_url_fx(in_sch):

    if in_sch:
        return lambda i: "http://pxy.randna.me:3000/%s" % i
    else:
        return lambda i: "http://cc3001.dmm.co.jp/litevideo/freepv/%s/%s/%s/%s_sm_w.mp4" % (i[0],i[0:3],i,i)

def home(request):
    get_img_url = img_url_fx(in_school(request))

    videos = Video.objects.all()[:12]

    for v in videos: v.thumb = get_img_url( v.cid, 'pt' )

    return render(request, "library/index.html", { 'videos': videos } )

def video_page(request, cid):

    in_sch = in_school(request)
    get_img_url = img_url_fx(in_sch)
    get_vid_url = vid_url_fx(in_sch)

    try:
        video = Video.objects.get(cid=cid)
    except Video.DoesNotExist:
        error = "Video %s does not exist" % cid
        return render(request, "library/error.html", { 'error': error } )

    video.cover = get_img_url( video.cid, 'pl' )
    video.s_vid = get_vid_url( video.cid )

    return render(request, "library/video.html", { 'video': video } )

def article(request, article, a_id):

    prop = { 'maker': Maker, 'label': Label, 'series': Series, 'director': Director, 'actresses': Actress, 'tags': Tag }

    for k,v in prop.items():
        if k.startswith(article):
            a_model = (k,v)
            break

    try:
        a_object = a_model[1].objects.get(_id=a_id)
    except a_model[1].DoesNotExist:
        error = "%s %s does not exist" % ( article, a_id )
        return render(request, "library/error.html", { 'error': error } )

    a_object.t = article

    kwa = { a_model[0]: a_id }

    get_img_url = img_url_fx(in_school(request))

    videos = Video.objects.filter(**kwa)[:12]

    for v in videos: v.thumb = get_img_url( v.cid, 'ps' )

    return render(request, "library/article.html", { 'article': a_object, 'videos': videos } )
