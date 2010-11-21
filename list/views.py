from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from models import GroceryList, GroceryItem
from forms import GroceryListForm, GroceryItemFormSet

@login_required
def index(request):
    '''returns a list of grocery list for a user'''
    glist = GroceryList.objects.filter(author=request.user)
    return render_to_response('list/grocery_index.html', {'glists' : glist}, context_instance=RequestContext(request))

@login_required
def groceryDelete(request, id):
    ''' takes the id of a list andremoves a users grocery list'''
    list = get_object_or_404(GroceryList, author=request.user, id=id)
    list.delete()
    messages.success(request, 'Your grocery list has been removed.')
    return HttpResponseRedirect(reverse('list.views.index'))

@login_required
def groceryCreate(request):
    ItemFormSet = inlineformset_factory(GroceryList, GroceryItem, extra=15, formset=GroceryItemFormSet)
    if request.method=='POST':
        form = GroceryListForm(request.POST)
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            new_list = form.save()
            instances = formset.save(commit=False)#save the items seperatly
            for instance in instances:
                instance.list_id = new_list.id #set the grocery id foregin key to the this grocery id
                instance.save()
            return redirect('/list/grocery/')
    else:
        form = GroceryListForm()
        formset = ItemFormSet(queryset=GroceryItem.objects.none())

    return render_to_response('list/grocerylist_form.html', {'form': form, 'formset' : formset,}, context_instance=RequestContext(request))