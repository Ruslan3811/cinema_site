# cinema_site
Making site of films

# Added ckeditor and appended Youtube plugin in the redactor.
Ckeditor allows to use text redactor in admin panel.
Youtube plugin allows to add videos to the site using admin panel.

# Added actions of publishing and unpublishing movies to admin panel for Movie Page
It allows administrators to edit Movie Page for user's interface.

# Using simple and inclusion tags
Simple tag allows to call function, that returns objects.
Inclusion tag allows to call function, thar returns objects to template in queryset.

# Year and genre filtering of films
Instead tags, I used classes for filtering and returnin objects. For filtering I made Queries using class Q.

# User's values to films
Now every user can rate the film and change his choice. Every user can do it for every film.

# Added pagination for main page
It works if user looks page with full list of films or uses filter

# Added searching movies with search bar
Users can find a movie by title

# Added ReCaptcha in Reviews
It protects against spam

# Added page /about/ using flatpage
Flatpages allows to create static pages, save info in database and manage it using admin panel

# Added forms:
## 1) Review form
## 2) Comment form
## 3) Mailing form

# Added sign in, sign out, registration

# Added sign in using social app vk