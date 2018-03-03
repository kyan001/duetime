from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _

from main.models import ShortUrl


def shorturlJump(request, id):
    """su/<int:id>"""
    shorturl = ShortUrl.objects.get_or_404(id=id)
    shorturl.add_pv()
    return redirect(shorturl.url)


@login_required
def shorturlAdd(request):
    """shorturl/add"""
    name = request.POST.get('name') or ""
    url = request.POST.get('url') or None
    user = request.user
    if request.POST:
        if not url:
            messages.error(request, _("Argument URL cannot be empty"))
        else:
            with transaction.atomic():
                shorturl = ShortUrl(name=name, url=url, userid=user.id)
                shorturl.save()
                return redirect("/shorturl/detail?id={}".format(shorturl.id))
    return render(request, "shorturl/add.html")


@login_required
def shorturlDetail(request):
    """shorturl/detail"""
    shorturlid = request.GET.get('id')
    user = request.user
    if not shorturlid:
        raise Http404(_("ShortURL ID cannot be empty"))
    shorturl = ShortUrl.objects.get_or_404(id=int(shorturlid))
    if shorturl.userid != user.id:
        raise Http404(_("You are not the owner of this shorturl"))
    context = {
        'shorturl': shorturl,
    }
    return render(request, 'shorturl/detail.html', context)


@login_required
def shorturlList(request):
    """shorturl/list"""
    user = request.user
    shorturls = ShortUrl.objects.filter(userid=user.id).order_by('created')
    context = {
        "shorturls": shorturls,
    }
    return render(request, 'shorturl/list.html', context)


@login_required
def shorturlDelete(request):
    """shorturl/delete"""
    shorturlid = request.GET.get('id')
    user = request.user
    if not shorturlid:
        raise Http404(_("ShortURL ID cannot be empty"))
    shorturl = ShortUrl.objects.get_or_404(id=int(shorturlid))
    if shorturl.userid != user.id:
        raise Http404(_("You are not the owner of this shorturl"))
    with transaction.atomic():
        shorturl.delete()
        messages.success(request, _("Shorturl removed!"))
        return redirect("/shorturl/list")
    raise Http404(_("Delete failed"))