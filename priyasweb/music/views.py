#from django.http import Http404
#from django.http import HttpResponse
#from .models import Album, Song
#from django.template import loader
#from django.shortcuts import render , get_object_or_404
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
#to create model views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album
from django.urls import reverse_lazy
from .forms import UserForm

class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(CreateView):
    #what are we trying to create
    model = Album
    fields = ['artist', 'album_logo', 'album_title', 'genre']

class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_logo', 'album_title', 'genre']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {form:'form'})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #clean and normalised data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # returns user objects if credentials are correct
            user= authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {form: 'form'})



#check out the previous code below and there import files above
"""
def index(request):

    all_albums = Album.objects.all()
    #template = loader.get_template('music/index.html')
    context = {'all_albums': all_albums}
    #return HttpResponse(template.render(context, request))
    return render(request, 'music/index.html', context )


    #html=''
    #for album in all_albums:
    #    url = '/music/'+ str(album.id) + '/'
    #    html += '<a href="'+url+'">' + album.album_title + '</a><br>'
    #return HttpResponse(html)
def detail(request, album_id):
    #return HttpResponse("<h2>This is detail for album id" + str(album_id) + "</h2>")
    #try:
    #    album = Album.objects.get(pk=album_id)
    #except Album.DoesNotExist:
    #    raise Http404("Album does not exist")
    album = get_object_or_404(Album, pk= album_id)
    return render(request, 'music/detail.html', {'album': album})


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {'album': album,
                                                     'error_message': "You did not select a valid song"})
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/detail.html', {'album': album})
"""