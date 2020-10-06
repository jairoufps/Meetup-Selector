from django.http import HttpResponse
from django.shortcuts import render

from .forms import TopicProposalForm


def topic_proposal(request):
    topic_form = TopicProposalForm()

    if request.method == 'POST':
        topic_form = TopicProposalForm(request.POST)
        if topic_form.is_valid():
            topic_form.save()
            topic_form = TopicProposalForm()

    context = {
        'topic_form': topic_form
    }
    html = render(request=request, template_name='topic_proposal.html', context=context)

    return HttpResponse(html)
