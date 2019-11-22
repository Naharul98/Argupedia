from django.shortcuts import render
import re
from datetime import timedelta
from django.conf import settings
from django.views import View
from .models import Entry
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
class HomeView(View):

    def rebuild_tree(self, request, root_nodes):
        paginator = Paginator(root_nodes, settings.PAGINATE_ENTRIES_BY)
        page = request.GET.get("page")
        queryset = []
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        new_queryset = []
        for node in queryset.object_list:
            new_queryset.append(node)
            for descendant in node.get_descendants():
                if descendant.level >= 9:
                    if descendant.level == 9:
                        new_queryset[-1].has_hidden_children = True
                    continue
                new_queryset.append(descendant)
        queryset.object_list = new_queryset
        return queryset

    def get(self, request):
        root_nodes = Entry.objects.root_nodes()
        root_nodes = root_nodes.annotate(overall_votes=(Count("upvotes") - Count("downvotes"))).order_by("-overall_votes")
        queryset = self.rebuild_tree(request, root_nodes)
        return render(request, "home.html", {"entries": queryset})

class PostsDetailView(View):
    def get(self, request, pk_post):
        subtree = Entry.objects.get(pk=pk_post)
        title = subtree.title
        root_nodes = subtree.get_descendants(include_self=True)
        root_nodes = root_nodes.annotate(overall_votes=(Count("upvotes") - Count("downvotes"))).order_by("-overall_votes")
        return render(request, "post_detail.html", {"entries": root_nodes, "title" : title})
