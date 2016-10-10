from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q, F, Count
from django.apps import apps
from json import dumps, loads
from .models import *
import datetime
import re

from javscraper.websites.DMM import *

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

def get_model( article ):

    for m in apps.get_app_config('library').get_models():
        model = m.__name__.lower()
        if model.startswith(article): return model, m

def show_error(request, errmsg=""):
    return render(request, "404.html", { 'error': errmsg } )

def searchterm( term ):

    data = { 'items': [] }

    if ':' in term:
        m, term = term.split(':')
        model, model_o = get_model(m)
        models_list = model_o.objects.annotate(count=Count('video'))

        nameq = Q(name__icontains=term)
        if model == 'actress':
            nameq = nameq | Q(furi__icontains=term) | Q(alias__icontains=term)

        model_list = models_list.filter( nameq ).order_by('-count')[:50].values()
        for v in model_list: v.update(article=model)

        data['items'] = tuple( model_list )
    else:
        try:
            term = int(term)
            for m in apps.get_app_config('library').get_models():
                if m in (Content, Video): continue
                ar = m.objects.filter(pk=term).values()
                for v in ar: v.update(article=m.__name__.lower())
                data['items'].extend( tuple( ar ) )
        except ValueError:
            pass

    data['count'] = len( data['items'] )

    return data

def searchquery( query ):
    if not query: return {}
    vals = ('pk', 'name', 'title')

    vq = Video.objects.annotate(acts=Count('actresses')).all()
    vq = vq.order_by( '-released_date' )

    m2m_or = {}

    if 'advanced' in query:
        min_a = query['advanced'].get('min_acts', 0)
        max_a = query['advanced'].get('max_acts', 20)
        if min_a != 0: vq = vq.filter(acts__gte=min_a)
        if max_a != 20: vq = vq.filter(acts__lte=max_a)

        min_d = query['advanced'].get('min_date')
        max_d = query['advanced'].get('max_date')
        if min_d: vq = vq.filter(released_date__gte=datetime.date(*min_d))
        if max_d: vq = vq.filter(released_date__lte=datetime.date(*max_d))

        min_t = query['advanced'].get('min_runtime', 0)
        max_t = query['advanced'].get('max_runtime', 960)
        if min_t != 0: vq = vq.filter(runtime__gte=datetime.timedelta(minutes=min_t))
        if max_t != 960: vq = vq.filter(runtime__lte=datetime.timedelta(minutes=max_t))

        m2m_or = query['advanced'].get('m2m_or', {})

    if 'filters' in query:
        print( query )
        for k,v in query['filters'].items():
            if k in ('actress', 'keyword'):
                k += 'es' if k.endswith('s') else 's'
                if m2m_or.get(k):
                    vq = vq.filter(**{ "%s__in" % k: v})
                else:
                    for s in v: vq = vq.filter(**{k:s})
            else:
                vq = vq.filter(**{ "%s__in" % k: v })

    qs = query.get( 'text' )
    if qs:
        nameq = Q()
        terms = re.findall( r'"([^"]+)"|(\S+)', qs )
        for t in terms:
            t = re.sub( r'\s{2,}', ' ', (t[0] or t[1]).strip() )
            print( t )
            if t:
                nameq = nameq | Q(title__icontains=t)
        if len( terms ) == 1:
            nameq = nameq | Q(name__icontains=qs)
        vq = vq.filter( nameq )

    page = int(query.get('page',1))
    per_page = int(query.get('per_page',50))

    try:
        qpage = list( get_page( vq, page, per_page ).object_list.values(*vals) )
    except AttributeError:
        qpage = ()

    return { 'items': qpage, 'count': vq.count() }

def search( request ):

    term = request.GET.get('term')
    if term:
        data = searchterm( term )
    else:
        query = {}
        q = request.GET.get('q')
        if q: query['text'] = q

        a = request.GET.get('a')
        if a:
            query['filters'] = {}
            for k in a.split(','):
                ar, _id = k.split('/')
                query['filters'][ar] = query['filters'].get( ar, [] ) + [_id]

        post_data = request.body.decode()
        if post_data: query = loads( post_data )

        if query:
            data = searchquery( query )
        else:
            return render(request, "library/search.html")

    data = dumps(data)
    if 'callback' in request.GET:
        data = "%s(%s)" % (request.GET.get('callback'), data)
    return HttpResponse(data, content_type='application/json')

def media( request ):

    try:
        vid = Video.objects.get(pk=request.GET.get('v'))
    except Video.DoesNotExist:
        return HttpResponse('')

    domain = get_domain( request )
    c = vid.content_set.first()

    if request.GET.get( 'r' ):
        location = domain[1] + get_sample_path( c.cid, request.GET.get('s','sm') )
    else:
        location = domain[0] + get_image_path( c.pid, request.GET.get('s','pt'), c.realm )

    resp = HttpResponse( location, status=303 )
    resp['Location'] = location

    return resp

def export_videos():
    with open('fskv', 'w') as f:
        for vid in Video.objects.filter(maker_id=46283):
            v = vid.__dict__
            v['actresses'] = tuple(vid.actresses.values_list('pk',flat=True))
            v['keywords'] = tuple(vid.keywords.values_list('pk',flat=True))
            v['cid'] = vid.content_set.filter(realm=1).values_list()[0][0]
            del v['_state']
            del v['_id']
            v['runtime'] = int(v['runtime'].seconds/60)
            v['released_date'] = str(v['released_date'])
            print(dumps(v), file=f)

def find_same_video():
    fields = ('title','maker','label','series','director')
    #'runtime','released_date',
    for v in Video.objects.filter(pk__endswith='-RE'):
        #if v.content_set.first().realm == 0:
    #    print(v)
        kk = Video.objects.filter(pk=v.pk[:-3])
        if not kk: continue
        kk = kk.first()

        diffs = {}

        for f in fields:
            fs = tuple(getattr(i,f) for i in (kk, v))
            if fs[0] != fs[1]: diffs[f] = fs

        for f in ('actresses', 'keywords'):
            fs = tuple(set(getattr(i,f).all()) for i in (kk, v))
            dfs = fs[0] ^ fs[1]
            if dfs: diffs[f] = dfs

        #for k in diffs['keywords']:
        #    if k.pk == 6102: continue
        if not diffs: continue    
        print( kk, diffs )

    #for title in vs.values_list('title',flat=True):
    #    sames = vs.filter(title__startswith=title)
    #    if len(sames) == 3:
    #        sm = sames.values_list('title',flat=True) 
    #        if any( 'pecial' in t for t in sm ):
    #            #print( sames )
    #            for t in sm: print( t )

    #for v in Video.objects.filter(pk__regex=r'-[A-Z]{2}$'):
    #    print(v)
        #print( v, v.content_set.first(), kk, kk.content_set.first() )

def get_filled(request=None):
    data = []
    for m in Maker.objects.annotate(count=Count('video')).exclude(count=0):
        vs = Video.objects.filter(maker=m)
        hv2 = vs.annotate(c_count=Count('content')).filter(c_count=2).count()
        havs = tuple(vs.filter(content__realm=i).count() for i in (0, 1))
        #avls = tuple(get_article('maker',m.pk,realm=i)['count'] for i in (0, 1))
        data.append((m.pk, m.name, vs.count(), havs[0]-hv2, hv2, havs[1]-hv2, havs[0], havs[1]))
        #data.append((vs.count(), 0, havs[0]-hv2, hv2, havs[1]-hv2, 0, m.name))
    data.sort(reverse=True,key=lambda x: x[2])
    data.insert(0, ('id', 'name', '0∪1', '0\\1', '0∩1', '1\\0', '0', '1'))
    return data

    data = dumps(data)
    if 'callback' in request.GET:
        data = "%s(%s)" % (request.GET.get('callback'), data)
    return HttpResponse(data, content_type='application/json')

def uniq_names():
    dg = re.compile(r'\d')
    nms = []
    #with open('labels.txt','w') as f:
    if True:
        for l in Label.objects.annotate(ct=Count('video')).filter(ct__gt=1):
            vs = Video.objects.filter(label=l).values_list('pk',flat=True)
            if len(vs) < 100: continue
            idtt = set(dg.subn('0',v) for v in vs)
            if len(idtt) > 4: continue
            regs = tuple(re.sub(r'0+', r'\d{%d}'%subs[1], subs[0]) for subs in idtt)
            difft = []
            for r in regs:
            #    if r.endswith('-RE'): print(r)
                rc = re.compile(r)
                difft.append((sum(rc.fullmatch(s) is not None for s in vs), r))
            difft.sort(reverse=True)
            #if difft[0][0] > 5:
            #    nms.append((l.pk,difft))
            print('{:>7}'.format(l.pk), difft)
            # if difft[0][0] != 1: continue
            # if len(difft) == 2: print('{:>7}'.format(l.pk), difft)
        #nms.sort(reverse=True,key=lambda x: x[1])
        #for n in nms:
        #    print('{:>7}  {}'.format(n[0], n[1]))

def maker_urls():
    return tuple((m.pk, m.name, m.url) for m in Maker.objects.exclude(url=''))

def home( request ):
    console = None
    # uniq_names()
    #find_same_video()
    #print( max(len(k.name) for k in Maker.objects.only('name').all()) )
    console = get_filled()
    # console = maker_urls()
    return render(request, "library/index.html", {'console': console})

def video_page(request, vid):

    if not vid: return redirect('home')

    try:
        video = Video.objects.get(name=vid)
    except Video.DoesNotExist:
        return show_error( request, "Video %s does not exist" % vid )
    except Video.MultipleObjectsReturned:
        return show_error( request, "Multiple videos called %s" % vid )

    c = video.content_set.first()
    sample_images = get_video(c.cid, realm=c.realm).get( "sample_images", 0 )
    video.samples = range( 1, sample_images ) if sample_images else ()

    if request.GET.get('f') == 'json':
        v = video.__dict__
        del v['_state']
        v['runtime'] = v['runtime'].seconds/60
        v['released_date'] = str(v['released_date'])
        v['samples'] = len(v['samples'])
        data = dumps(v)
        return HttpResponse(data, content_type='application/json')

    return render(request, "library/video.html", { 'video': video })

def article(request, article, a_id):

    sort = request.GET.get('s')
    page = request.GET.get('p')
    query = request.GET.get('q')

    model, model_o = get_model( article )

    if a_id:
        hd = ( 'name', 'title', 'released_date' )

        if model in ('actress', 'keyword'):
            q = model_o._meta.verbose_name_plural.lower()
        else:
            q = '%s__pk' % model

        videos_list = Video.objects.filter(**{ q : a_id })

        if request.GET.get('c'):

            videos = get_page( videos_list, page, per_page=12 )

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
        models_list = model_o.objects.annotate(count=Count('video'))

        hd = ( '_id', 'name', 'count' )

        if not sort: sort = '-count'

        l_sorted, models_list = get_sort( models_list, hd, sort )
        models = get_page( models_list, page )

        models.title = model
        models.thead = hd
        if l_sorted: models.sort = sort

        return render(request, "library/article.html", { 'pager': models } )

def filtered_article(request, filter_article, a_id, article):

    sort = request.GET.get('s')
    page = request.GET.get('p')
    query = request.GET.get('q')

    if not sort: sort = '-count'

    model, model_o = get_model( filter_article )
    article, a_o = get_model( article )

    hd = ( article, 'name', 'count' )

    if model in ('actress', 'keyword'):
        q = model_o._meta.verbose_name_plural.lower()
    else:
        q = '%s__pk' % model

    if article in ('actress', 'keyword'):
        article = a_o._meta.verbose_name_plural.lower()

    vs = Video.objects.filter(**{q: a_id}).values(article)
    m_list = vs.annotate(count=Count(article)).exclude(count=0)

    l_sorted, models_list = get_sort( m_list, hd, sort )

    for item in models_list:
        item['pk'] = item[article]
        item['name'] = a_o.objects.get(pk=item[article]).name

    models = get_page( models_list, page )
    models.title = "%s (%s)" % (article, model_o.objects.get(pk=a_id).name)
    models.thead = hd
    if l_sorted:
        models.sort = sort

    return render(request, "library/article.html", { 'pager': models } )
