from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Relationship,Profile
from .forms import UserRegisterForm,PostForm,ProfileUpdateForm,UserUpdateForm,ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
@login_required
def home(request):
	posts = Post.objects.all()
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('home')
	else:
		form = PostForm()

	context = {'posts':posts, 'form' : form }
	return render(request, 'twitter/newsfeed.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = UserRegisterForm()

	context = {'form' : form}
	return render(request, 'twitter/register.html', context)


def delete(request, post_id):
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('home')
@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all()
    
    # Obtener el perfil del usuario actual
    user_profile = request.user.profile if hasattr(request.user, 'profile') else None
    
    context = {'user': user, 'posts': posts, 'user_profile': user_profile}
    return render(request, 'twitter/profile.html', context)

@login_required
def editar(request):
    try:
        # Intenta obtener el perfil del usuario actual
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        # Si el perfil no existe, crea uno
        user_profile = Profile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'twitter/editar.html', context)

@login_required
def follow(request, username):
    current_user = request.user
    viewed_user = User.objects.get(username=username)
    to_user_id = viewed_user.id  # Obtener el ID del usuario objetivo
    rel = Relationship(from_user=current_user, to_user_id=to_user_id)  # Usar el ID del usuario objetivo
    rel.save()
    return redirect('home')

@login_required
def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    # Filtra las relaciones entre el usuario actual y el usuario objetivo
    relationships = Relationship.objects.filter(from_user=current_user, to_user=to_user)
    
    # Verifica si hay relaciones para eliminar
    if relationships.exists():
        # Elimina todas las relaciones encontradas
        relationships.delete() 
    return redirect('home')
