from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from django.apps import apps
from json import dumps
from .models import *

from DMM import DMM

def get_domain( req ):

    pxy = "http://dmm-proxy.herokuapp.com/"
    dmm = "http://%s.dmm.co.jp/"

    school_ips = ( '202.94.70.51', '103.24.77.25', '202.94.70.25' )

    for f in ( 'REMOTE_ADDR', 'HTTP_X_FORWARDED_FOR' ):
        if f in req.META: addr = req.META[f]

    if addr in school_ips:
        return ( pxy, pxy )
    else:
        return [ dmm % s for s in ( 'pics', 'cc3001' ) ]

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

def get_video( vid ):

        try:
            video = Video.objects.get(_id=vid)
        except Video.DoesNotExist:
            return None

        dmm = DMM()
        c = video.content_set.first()
        video.cover = dmm.get_image_path( dmm.REALM[c.realm], c.pid, 'pl' )
        video.s_vid = dmm.get_sample_vid_path( c.cid )

        return video

def show_error(request, errmsg=""):
    return render(request, "404.html", { 'error': errmsg } )

def search(request):
    q = request.GET.get('q')
    if not q:
        videos = []
    else:
        vq = Video.objects.values_list('pk',flat=True).filter(pk__icontains=q)[:10]
        videos = list(vq)

    data = dumps(videos) 
    if 'callback' in request.GET:
        data = "%s(%s)" % (request.GET.get('callback'), data)
        return HttpResponse(data, content_type='text/javascript')

    return HttpResponse('', content_type='text/javascript')

def home(request):

    if 'vid' in request.GET: return redirect('video_page', vid=request.GET.get('vid'))

    return render(request, "library/index.html")

def video_page(request, vid):

    if not vid:
        videos = Video.objects.all()[:12]
        return render(request, "library/index.html", { 'videos': videos } )

    video = get_video( vid )
    if not video: return show_error( request, "Video %s does not exist" % vid )

    return render(request, "library/video.html", { 'video': video, 'domain': get_domain(request) })

def article(request, article, a_id):

    for m in apps.get_app_config('library').get_models():
        model = m.__name__.lower()
        if model.startswith(article):
            model_o = m
            break

    sort = request.GET.get('s') 
    page = request.GET.get('p') 

    if a_id:
        hd = ( '_id', 'title', 'released_date' )

        if model == 'actress' or model == 'keyword':
            q = model_o._meta.verbose_name_plural.lower()
        else:
            q = '%s__pk' % model 

        videos_list = Video.objects.filter(**{ q : a_id })

        if request.GET.get('c'):
            dmm = DMM()
            domain = get_domain( request )[0]

            videos = get_page( videos_list, page, per_page=12 )
            for v in videos:
                c = v.content_set.first()
                v.cover = domain + dmm.get_image_path( dmm.REALM[c.realm], c.pid, 'pl' )

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
