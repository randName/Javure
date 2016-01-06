from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from django.apps import apps
from json import dumps
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
        return lambda i: "" 
    else:
        # sm dm dmb
        return lambda i: "http://cc3001.dmm.co.jp/litevideo/freepv/%s/%s/%s/%s_dmb_w.mp4" % (i[0],i[0:3],i,i)

def get_page( object_list, page, per_page=50 ):
    
    paginator = Paginator( object_list, per_page )

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

def get_sort( object_list, sort_keys, sort ):

    if not sort: return False, object_list

    for a in sort_keys:
        if sort.endswith(a):
            return True, object_list.order_by(sort)

    return False, object_list

def show_error(request, errmsg=""):
    return render(request, "404.html", { 'error': errmsg } )

def ajax(request):
    q = request.GET.get('q')
    if not q:
        videos = []
    else:
        vq = Video.objects.values_list('cid','display_id').filter(display_id__icontains=q)[:10]
        videos = list(vq)

    data = dumps(videos) 
    if 'callback' in request.GET:
        data = "%s(%s)" % (request.GET.get('callback'), data)
        return HttpResponse(data, content_type='text/javascript')

    return HttpResponse('', content_type='text/javascript')


def home(request):

    # videos = Video.objects.all()[:10]
    # makers = Maker.objects.annotate(count=Count('video')).order_by('-count')[:10]

    if 'cid' in request.GET: return redirect('video_page', cid=request.GET.get('cid'))

    return render(request, "library/index.html") # , { 'videos': videos, 'makers': makers } )

def video_page(request, cid):

    if cid:
        in_sch = in_school(request)
        get_img_url = img_url_fx(in_sch)
        get_vid_url = vid_url_fx(in_sch)

        try:
            video = Video.objects.get(cid=cid)
        except Video.DoesNotExist:
            return show_error( request, "Video %s does not exist" % cid )

        video.cover = get_img_url( video.pid, 'pl' )
        video.s_vid = get_vid_url( video.cid )

    else:
        videos = Video.objects.all()[:12]
        return render(request, "library/index.html", { 'videos': videos } )

    return render(request, "library/video.html", { 'video': video } )

def article(request, article, a_id):

    for m in apps.get_app_config('library').get_models():
        model = m.__name__.lower()
        if model.startswith(article):
            model_o = m
            break

    sort = request.GET.get('s') 
    page = request.GET.get('p') 

    if a_id:
        hd = ( 'cid', 'title', 'released_date' )

        if model == 'actress' or model == 'keyword':
            q = model_o._meta.verbose_name_plural.lower()
        else:
            q = '%s__pk' % model 

        videos_list = Video.objects.filter(**{ q : a_id })

        if request.GET.get('c'):
            get_img_url = img_url_fx(in_school(request))

            videos = get_page( videos_list, page, per_page=12 )
            for v in videos: v.cover = get_img_url( v.pid, 'pl' )

            videos.title = "%s - %s" % ( model, model_o.objects.get(_id=a_id).name )
            videos.carousel = 1

            return render(request, "library/article_carousel.html", { 'pager': videos } )
        else:
            l_sorted, videos_list = get_sort( videos_list, hd, sort )
            videos = get_page( videos_list, page )

            videos.title = "%s - %s" % ( model, model_o.objects.get(_id=a_id).name )
            videos.thead = hd
            if l_sorted: videos.sort = sort

            return render(request, "library/list.html", { 'pager': videos } )

    else:
        hd = ( '_id', 'name', 'count' )

        models_list = model_o.objects.annotate(count=Count('video')).all()

        l_sorted, models_list = get_sort( models_list, hd, sort )
        models = get_page( models_list, page )

        models.title = model
        models.thead = hd
        if l_sorted: models.sort = sort

        return render(request, "library/article.html", { 'pager': models } )

def keywords(request):
    return home(request)

def actresses(request):
    return home(request)

def articlepage(request, article):
    return home(request)

def stats(request):
    return home(request)
