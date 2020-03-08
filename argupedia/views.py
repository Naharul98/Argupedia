from django.http import Http404
from django.shortcuts import render
import re
from datetime import timedelta
from django.conf import settings
from django.views import View
from .models import Entry
from .models import Scheme
from .models import SchemeStructure
from .models import CriticalQuestion
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

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
        return render(request, "post_detail.html", {"entries": root_nodes, "title" : title, "root_post_id" : pk_post, "is_parent": (subtree.parent == None)})

class MyDiscussionsView(DetailView):
    model = User
    template_name = 'home.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        username = self.kwargs.get("username")
        if not username:
            return super().get_object(queryset)
        else:
            username = username.lower()
        queryset = queryset.filter(username=username)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("something went wrong")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_entries = Entry.objects.filter(user=self.get_object().pk)
        last_discussions = []

        for entry in user_entries:
            if any([entry.pk == discussion.pk for discussion in last_discussions]):
                continue
            for node in list(entry.get_family()):
                last_discussions.append(node)
        context["entries"] = last_discussions
        return context

class ChooseSchemeView(View):
    def get(self, request, pk_post):
        all_schemes = Scheme.objects.all()
        entry = ''
        if(pk_post != 0):
            entry = Entry.objects.get(pk=pk_post)

        return render(request, "choose_scheme.html", {"schemes": all_schemes, "pk_post": pk_post, "entry": entry})


class CreatePost(View):
    def get(self, request, pk_scheme):
        argumentation_scheme = SchemeStructure.objects.filter(scheme=pk_scheme).order_by('ordering')
        return render(request, "create_post.html", {"scheme_structure": argumentation_scheme, "scheme_id": pk_scheme})

    def post(self, request, pk_scheme):
        argumentation_scheme = SchemeStructure.objects.filter(scheme=pk_scheme).order_by('ordering')
        stringBuilder = []
        for tup in argumentation_scheme:
            stringBuilder.append('**')
            stringBuilder.append(tup.section_title)
            stringBuilder.append(':')
            stringBuilder.append('**')
            stringBuilder.append('<br>')
            stringBuilder.append(request.POST.get(tup.section_title, ""))
            stringBuilder.append('<br>')
        baldur = ''.join(stringBuilder)
        entry = Entry(user=request.user, content=baldur, title=request.POST.get('post_title', ""), scheme_used=Scheme.objects.get(pk=pk_scheme))
        entry.save()
        entry.upvotes.add(request.user)
        return redirect('posts-detail-view', pk_post=entry.id)


class DeletePost(View):
    def get(self, request, pk_post):
        Entry.objects.get(id=pk_post).delete()
        Entry.objects.rebuild()
        return redirect('home')


class CounterPost(View):
    def get(self, request, pk_scheme, pk_post):
        argumentation_scheme = SchemeStructure.objects.filter(scheme=pk_scheme).order_by('ordering')
        attacking = Entry.objects.get(pk=pk_post)
        criticalQuestions = CriticalQuestion.objects.filter(related_scheme=attacking.scheme_used.id)
        return render(request, "counter_post.html", {"scheme_structure": argumentation_scheme, "scheme_id": pk_scheme, "entry": Entry.objects.get(pk=pk_post), "critiques": criticalQuestions})

    def post(self, request, pk_scheme, pk_post):
        argumentation_scheme = SchemeStructure.objects.filter(scheme=pk_scheme).order_by('ordering')
        stringBuilder = []
        critique = CriticalQuestion.objects.get(pk=request.POST.get('critique'))
        stringBuilder.append('Critique Position: *')
        stringBuilder.append(critique.question)
        stringBuilder.append('*')
        stringBuilder.append('<br>')
        for tup in argumentation_scheme:
            stringBuilder.append('**')
            stringBuilder.append(tup.section_title)
            stringBuilder.append(':')
            stringBuilder.append('**')
            stringBuilder.append('<br>')
            stringBuilder.append(request.POST.get(tup.section_title, ""))
            stringBuilder.append('<br>')
        baldur = ''.join(stringBuilder)
        attacking = Entry.objects.get(pk=pk_post)

        entry = Entry(user=request.user, content=baldur, title=request.POST.get('post_title', ""), scheme_used=Scheme.objects.get(pk=pk_scheme), critical_question=critique, parent=attacking)
        entry.save()
        entry.upvotes.add(request.user)
        return redirect('posts-detail-view', pk_post=pk_post)


class VisualizeView(View):
    def get(self, request, pk_post):
        subtree = Entry.objects.get(pk=pk_post)
        root_nodes = subtree.get_descendants(include_self=True)
        set_in = set()
        set_out = set()
        set_undec = set()

        for entry in root_nodes:
            if (entry.has_children == False and entry.is_root_node() == False):
                if (entry.critical_question.is_attack_on_conclusion == False):
                    set_in.add(entry.pk)
        while(True):
            prev_set_in = set_in.copy()
            prev_set_out = set_out.copy()
            for entry in root_nodes:
                if entry.pk not in set_in and entry.pk not in set_out:
                    okay = True
                    for y in entry.get_attackers():
                        if y.pk not in set_out:
                            okay = False
                            break
                    if okay == True:
                        set_in.add(entry.pk)
            for entry in root_nodes:
                if entry.pk not in set_out and entry.pk not in set_in:
                    okay = False
                    for y in entry.get_attackers():
                        if y.pk in set_in:
                            okay = True
                            break
                    if okay == True:
                        set_out.add(entry.pk)
            if(prev_set_in == set_in and prev_set_out == set_out):
                break
        for entry in root_nodes:
            if entry.pk not in set_in and entry.pk not in set_out:
                set_undec.add(entry.pk)
        print(set_in)
        print(set_out)
        print(set_undec)
        return render(request, "visualize.html", {"post_id": pk_post,"entries": root_nodes,"in": set_in,"out": set_out, "undec" : set_undec})




