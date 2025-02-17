import os
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.http import Http404
from django.conf import settings
from django.utils import timezone

# PostForm with a title and an optional image field.
class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
    image = forms.ImageField(required=False)

def home(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT bp.id, bp.title, bp.image, bp.date_posted, 
                   au.id, au.username, COALESCE(up.image, 'profile_pics/default.jpg')
            FROM blog_post bp
            JOIN auth_user au ON bp.author_id = au.id
            LEFT JOIN users_profile up ON au.id = up.user_id
            ORDER BY bp.date_posted DESC
        """)
        posts = cursor.fetchall()

    context = {
        'posts': [
            {
                'id': row[0],
                'title': row[1],
                'image': row[2],  # This should be a relative path like "blog_images/..."
                'date_posted': row[3],
                'author': {
                    'id': row[4],
                    'username': row[5],
                    'image': row[6],
                }
            } for row in posts
        ]
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, "blog/about.html")

def user_posts(request, username):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT bp.id, bp.title, bp.image, bp.date_posted, 
                   au.username, COALESCE(up.image, 'profile_pics/default.jpg')
            FROM blog_post bp
            JOIN auth_user au ON bp.author_id = au.id
            LEFT JOIN users_profile up ON au.id = up.user_id
            WHERE au.username = %s
            ORDER BY bp.date_posted DESC
        """, [username])
        rows = cursor.fetchall()

    posts = [{
        'id': row[0],
        'title': row[1],
        'image': row[2],
        'date_posted': row[3],
        'author': {
            'username': row[4],
            'image': row[5],
        }
    } for row in rows]

    return render(request, 'blog/user_posts.html', {'posts': posts, 'username': username})

def post_detail(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, image, date_posted, author_id FROM blog_post WHERE id = %s", [post_id])
        post = cursor.fetchone()
        if not post:
            raise Http404("Post does not exist")
        cursor.execute("SELECT username FROM auth_user WHERE id = %s", [post[4]])
        author = cursor.fetchone()
        if not author:
            raise Http404("Author does not exist")
    context = {
        'post': {
            'id': post[0],
            'title': post[1],
            'image': post[2],
            'date_posted': post[3],
            'author': {
                'id': post[4],
                'username': author[0],
            }
        }
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            uploaded_image = request.FILES.get('image')
            relative_path = None  # Will store the relative file path if an image is uploaded

            if uploaded_image:
                # Generate a unique filename (like your profile update code)
                file_ext = os.path.splitext(uploaded_image.name)[1].lower()
                timestamp = int(timezone.now().timestamp())
                new_filename = f"blog_{request.user.id}_{timestamp}{file_ext}"
                relative_path = os.path.join('blog_images', new_filename)
                absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

                # Save the image file in chunks
                with open(absolute_path, 'wb+') as f:
                    for chunk in uploaded_image.chunks():
                        f.write(chunk)

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO blog_post (title, image, author_id) VALUES (%s, %s, %s) RETURNING id",
                    [title, relative_path, request.user.id]
                )
                post_id = cursor.fetchone()[0]
            messages.success(request, "Post created successfully!")
            return redirect('post-detail', post_id=post_id)
        else:
            messages.error(request, "Form is invalid. Please try again.")
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def update_post(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT title, image FROM blog_post WHERE id = %s AND author_id = %s", [post_id, request.user.id])
        post = cursor.fetchone()
    if not post:
        raise Http404("Post not found or you are not authorized to edit it.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            uploaded_image = request.FILES.get('image')
            relative_path = post[1]  # Use current image path by default

            if uploaded_image:
                # Generate a new unique filename
                file_ext = os.path.splitext(uploaded_image.name)[1].lower()
                timestamp = int(timezone.now().timestamp())
                new_filename = f"blog_{request.user.id}_{timestamp}{file_ext}"
                relative_path = os.path.join('blog_images', new_filename)
                absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

                os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

                with open(absolute_path, 'wb+') as f:
                    for chunk in uploaded_image.chunks():
                        f.write(chunk)

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE blog_post SET title = %s, image = %s WHERE id = %s AND author_id = %s",
                    [title, relative_path, post_id, request.user.id]
                )
            messages.success(request, "Post updated successfully!")
            return redirect('post-detail', post_id=post_id)
        else:
            messages.error(request, "Form is invalid. Please try again.")
    else:
        form = PostForm(initial={'title': post[0]})
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def delete_post(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM blog_post WHERE id = %s AND author_id = %s", [post_id, request.user.id])
    messages.success(request, "Post deleted successfully!")
    return redirect('home')
