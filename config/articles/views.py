from django.views.generic import ListView
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentForm
from .models import Article, Category, Tag, Comment


class ArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"
    paginate_by = 12

    def get_queryset(self):
        qs = Article.objects.filter(status=Article.PUBLISHED).select_related("category", "author")
        category_slug = self.request.GET.get("category")

        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        return qs.order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category"] = self.request.GET.get("category")
        # context["seo_title"] = self.get_seo_title()
        # context["seo_description"] = self.get_seo_description()
        return context
    


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('category', 'author').prefetch_related('tags'),
        slug=slug,
        status=Article.PUBLISHED
    )

    comments = article.comments.filter(parent__isnull=True, is_approved=True).select_related('user')

    comment_form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent = None

            if parent_id:
                parent = Comment.objects.get(id=parent_id)

            Comment.objects.create(
                article=article,
                user=request.user,
                text=comment_form.cleaned_data['text'],
                parent=parent
            )
            return redirect('articles:article_detail', slug=article.slug)

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'seo_title': article.get_seo_title(),
        'seo_description': article.get_seo_description()
    })
