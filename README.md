# MyTravelog - Social Networking Travel Website 
A social networking travel website developed using Django Web Framework, where users can share and log their beautiful moments to help others plan their trips. The website also incorporates a ranking system, where each user gets ranked based on their travel and social statistics, motivating them to be more active in order to compete with other users. 

## Developer Documentation

[TOC]


Geting Started 
--------------------
All you need to get started: 

**Tools:**

1. Python 2.7.x or Python 3.4.x

2. Pip (Python package management tool)

3. virtualenv (tool to create isolated Python environments)

**Dependencies:**

 1. Django Web Framework
 2. Pillow Imaging Library
 3. beatifulsoup4 - HTML Scraping Library
 4. coverage - Test Coverage Analyser 

The provided bash script called `installation_script`, sets up a virtual environment, activates it, installs the required dependencies, and starts the local development server. You just need to go to `s1265676_selp/` directory and execute the following command: 
```
$ . ./installation_script
```
(Notice the 2 `.` before `/`) 

Now that the web server has started, you can start exploring the website by visiting the following URL in **Google Chrome** or **Internet Explorer**: 

    127.0.0.1:8000/mytravelog/

> **Note**: 
You must use `Google Chrome` or `Internet Explorer` to view the website, since it uses some `HTML5` features not yet supported by `FireFox`. 


----------


Project and Code Structure
-----------------

When you first clone the repository, the directory structure would look like this: 

    selp/
        mytravelog/
        selp/
        .coverage
        .gitignore
        db.sqlite3
        manage.py
        populate_cities.py
        update_log_scores.py
        update_user_ranks.py
        
These files are: 

 - The outer **`selp/`** root directory is just a container for the project. It's name doesn't matter, so it can be simply renamed to anything you like.

 - The inner **`mytravelog/`** directory is the main Django application package that houses all the logic required to run the website. (*See the note below to know the difference between a project and an application*).

 - The inner **`selp/`** directory  is the actual Python package for the project. It's name is the Python package name that you'll need to use to import anything inside it (eg. `selp.urls`).
 
 - **`.coverage`**: File containing the coverage analysis report. It gets generated whenever the coverage analyser is run. 
 
 - **`.gitignore`**: Consists a lists of files and directories that you do not want to track using version control.
 
 -  **`db.sqlite3`**: Default database file that comes installed when you first start a Django project. No need to change any configuration files to start using it.
 
 - **`manage.py`**: A command-line utility that lets you interact with this Django project in various ways (such as creating a new Django application or starting a local web server).
  
 - **`populate_cities.py`**: A script to populate the database with 101 cities from a serialized file included in `mytravelog/utils/city_parser/`. One of the cities: Edinburgh, is added manually since it is not included in the Euromonitor's report on 'Top 100 City Destinations Ranking'. 
  
 -  **`update_log_scores.py`**: A script to update the scores of user logs in the database. The live feed page displays all user logs sorted by descending order of this score. **Note**: This script should be scheduled to run every few hours using a cron job in `Linux` or task scheduler in `Windows`. 
 
 - **`update_user_ranks.py`**:  A script to update ranks for all users in the database. These ranks show up leaderboard page and each user page.  **Note**: This script should be scheduled to run every few hours using a cron job in `Linux` or task scheduler in `Windows`. 

> **Note: Project vs app**
> An app is a web application that does something. Whereas, a project is a collection configuration and apps for a particular website. A project can contain multiple apps. In our case, *mytravelog* is the only app. 

Moving onto the inner `selp/` directory: 

    selp/
	    media/
		     mytravelog/
					   cover_pictures/
					   log_pictures/
					   profile_pictures/
		static/
		     mytravelog/
					   css/
					   fonts/
					   imgs/
					   js/
		templates/
			 mytravelog/
        __init__.py
        settings.py
        urls.py
        wsgi.py

These files are: 

 - **`media/`**: User-uploaded files are served from this directory. Whenever you add a new `FileField` or `ImageField` to any of your models, you need to set the `upload_to` attribute to this directory.
 
 - **`media/mytravelog/cover_pictures/`**: Serves all user-uploaded cover pictures. This includes all `Album` and `UserProfile` cover pictures. 
 - **`media/mytravelog/log_pictures/`**: Serves all user-uploaded `Log` pictures. 
 - `media/mytravelog/profile_pictures`: Serves all user-uploaded `UserProfile` profile pictures. 
 
 - **`static/`**: Serves all static files such ash images, Javascript or CSS.
  
 - **`static/mytravelog/css`**: Serves stylesheets for your various HTML templates included in `selp/templates/`.
 
 - **`static/mytravelog/fonts`**: Serves all custom fonts used in the website.
  
 - **`static/mytravelog/imgs`**: Serves all default images (not uploaded by the user) used in the website, such as country flags, default city cover picture and default profile picture.
     
 - **`static/mytravelog/js`**: Serves Javascript files.
 
 - **`templates/`**: Serves all HTML templates for the various pages on the website.
  
 - **`__init__.py`**: An empty file that tells Python that this directory should be considered a Python package.
 
 - **`settings.py`**: Settings/configuration for this Django project.
  
 - **`urls.py`**: The URL declarations for this Django project.
 
 - **`wsgi.py`**: a Python script used to help run a development server and deploy thus project to a production environment.

> **Note: Why do most directories contain the inner mytravelog/ directory?**
> Since our Django app's name is *mytravelog*, each file serving directory contains a directory named after the app, to separate its files from other apps. 

And now finally, our main app `mytravelog/` directory: 

    mytravelog/
	        migrations/
	        models/
	        tests/
	        utils/
		         city_parser/
	        views/
	        __init__.py
	        admin.py
	        urls.py

These files are: 

 - The inner **`migrations/`** directory includes migration files, where each file stores the changes to your database models (and thus your database schema).

 - The inner **`models/`** directory  includes all database models that essentially represent the tables inside your database and the relations between them. 

 - The inner **`tests/`** directory includes all functional and unit tests.

 - The inner **`utils/`** directory includes any helper/utility packages. In our case, we have a utility package called `city_parser`, which parses all information related to cities from external websites (Wikipedia and/or Wikitravel). 

 - The inner **`views/`** directory includes all the views for our website. A view is essentially a type of a web page in a Django application that generally serves a specific function and has a specific template.

 - **`__init__.py`**: An empty file that tells Python that this directory should be considered a Python package.

 - **`admin.py`**: A command-line utility for administrative tasks, such as clearing the entire database or checking if there are any problems with the installed database models.

 - **`urls.py`**:  The URL declarations for this app only. (*See the note below to know why there are 2 urls.py files*)

> **Note: Why are there 2 urls.py files?**
> Technically, we can put all URL mappings/declarations inside the project level `urls.py` (`selp/urls.py`), however, this is considered bad practice as it creates coupling between our individual applications. Therefore, all URL mappings related to our main app *mytravelog*, go in `selp/mytreavelog/urls.py`, and then they are simply joined to the project level `urls.py` by adding the following line to it: 
>     
>     `url(r'^mytravelog/', include('mytravelog.urls'))`


----------

**Views Overview**

Now that we're done understanding the overall structure of the project, I'll describe what each of the files in  `mytravelog/views/` directory contains and which urls are mapped to the views in each file 

    views/
	    __init__.py
	    album.py
		city.py
		comments.py
		follower.py
		home.py
		leaderboard.py
		like.py
		live_feed.py
		log.py
		search.py
		user.py

These files are: 

 - **`__init__.py`**: An empty file that tells Python that this directory should be considered a Python package.
 
 - **`album.py`**: Consists of views related to the `Album` model.  These views are used to perform *CRUD* operations on the `Album` model. The following URLs are mapped to the views in this file:   
	 -  `/mytravelog/album/create/`
	 -  `/mytravelog/album/update/<album_id>/`
	 -  `/mytravelog/album/delete/<album_id>/`
	 -  `/mytravelog/album/<album_id>/`
 - **`city.py`**: Consists of views that show the requested city page to the user and to fetch auto-complete city name suggestions based on a search tern provided by the user. The following URLs are mapped to the views in this file: 
	 - `/mytravelog/city/<city_name>/`
	 - `/mytravelog/city/autocomplete/` 
 - **`comments.py`**: Consists of views that perform *CREATE* and *DELETE* operations on `Comment` model. The URLs mapped to the views in this file are: 
	- `/mytravelog/comment/create/<log_id>`
	- `/mytravelog/comment/delete/<comment_id>`
 - **`follower.py`**: Consists of views that perform *CREATE* and *DELETE* operations on `Follower` model. The URLs mapped to the views in this file are: 
	- `/mytravelog/follower/create/<following_user_profile_id>`
	- `/mytravelog/follower/delete/<following_user_profile_id>`
 - **`home.py`**: Consists of a single which which is used to show the home page to the user. This view is mapped to the following URL: 
	 - `/mytravelog/`
 - **`leaderboard.py`**: Consists of a single view which is used to show the leaderboard page to the user, with paginated results based on the requested model: `cities` or `users`. The results are filtered using a helper functions included in this file.  The only view is mapped to the following URL: 
 	 - `/mytravelog/leaderboard/<model>/`
 - **`like.py`**: Consists of views that perform *CREATE* and *DELETE* operations on `Like` model. The URLs mapped to the views in this file are: 
 	- `/mytravelog/like/create/<log_id>`
	- `/mytravelog/like/delete/<log_id>`
 - **`live_feed.py`**: Consists of a single view which is used to show the live feed page to the user, with paginated results based on the requested filter: `all` or `following`. If the requested filter is `all`, then logs from all posts are displayed, whereas the `following` filter only displays logs from users followed by current user. The returned logs are also sorted in descending order of their log scores. This view is mapped to the following URL: 
 	 - `/mytravelog/live_feed/<feed_filter>/`
 - **`log.py`**:  Consists of views that perform *CRUD* operations on the `Log` model. There's also another view named `get_log_info_for_map`, which returns the requested user's log locations and related info (in `json` format), which is then used to show all log locations on a world map. The URLs mapped to the views in this file are: 
	 - `/mytravelog/log/create/`
	 - `/mytravelog/log/edit/<log_id>/`
	 - `/mytravelog/log/delete/<log_id>/`
	 -  `/mytravelog/log/<log_id>/`
	 - `/mytravelog/log/get_info_for_map/<username>/`
 - **`search.py`**: Consists of a single view which is used to search for cities and users from the home page. If a search matches a city name exactly, the user is navigated directly to its city page. Else, the search page is displayed with all the filtered results. This view is mapped to the following URL: 
	 - `/mytravelog/search/` 
 - **`user.py`**: Consists of views that handle user registration and authentication. There's also a view to display the requested user page. The following URLs mapped to the views in this file: 
	 -  `/mytravelog/sign_up/`
	 - `/mytravelog/sign_in/`
	 - `/mytravelog/sign_out/`
	 - `/mytravelog/user/<username>`


----------
**Models Overview**

Moving onto `mytravelog/models` directory: 

    models/
	    __init__.py
	    album.py
		city.py
		comments.py
		follower.py
		like.py
		live_feed.py
		log.py
		log_picture.py
		user_profile.py
Each of these files consists of the corresponding model, where each model is represented by a class that subclasses `django.db.models.Model` Each model has a number of class variables, each of which represents a database field in the model. Relations are also defined using these variables. For example: `UserProfile` model has a variable `user` defined as follows: 
```
user = models.OneToOneField(User)
```
Even though `user` is just a class variable, it defines a one-to-one relationship between `UserProfile` and `User` models. 

Some of the above models also make use of a custom `Manager` to provide the ability to perform complex queries to the corresponding models.  For example, the `Log` model has a custom manager called `LogManager` which provides it the ability to attach all comments, likes and log pictures to each log in the provided list of logs, using a static method: `attach_additional_info_to_logs`.  

> **Note: What is a Manager?**
A `Manager` is the interface through which database query operations are provided to Django models. At least one Manager exists for every model in a Django application.

Another important thing to note is the location of the scoring functions. `Log` model has a function: `get_log_score` which computes the score of a log based on the following factor: 

 - time difference between epoch time and log creation time
 - number of comments received 
 - number of likes received

`UserProfile` model has a function: `compute_and_get_score` which computes the user score based on the following factors: 

 - Ranks of all unique cities visited
 - Number of logs posted
 - Total number of comments received on all logs 
 - Total number of likes received on all logs 
 - Number of followers 

To combine all of these factors together, a weight sum is computed. 
 

 **Tip: Models with File attributes**: 
 If you add a model with a `FileField` or `ImageFIeld` attribute in it, then don't forget to delete the linked image if the corresponding model instance gets deleted. This can be done by receiving a `post_delete` signal for that specific model, and deleting the linked image manually. For example, when a `LogPicture` instance is being deleted, the following code would also delete the image file linked it:    

```
    # auto delete file when imagefield is deleted
    from django.db.models.signals import post_delete
    from django.dispatch.dispatcher import receiver
    
    @receiver(post_delete, sender=LogPicture)
    def auto_delete_file(sender, instance, **kwargs):
        # Pass false so ImageField doesn't save the model.
        instance.picture.delete(False)
```


----------
**JavaScript Overview**

Finally, I'm going to describe how the `JavaScript` code is structured in `selp/static/mytravelog/js/main.js`. Since it is recommended to have all JavaScript code in one file, in order to reduce the number of HTTP requests, I decided to use *revealing module design pattern*. It allows me to reduce clutter in the global namespace by the localization of functions and variables through closures. 

Basically, an immediately invoked function which returns all the public functions, is namespaced by the name of the module, so that the returned functions can be accessed. The common structure I follow for all my modules is shown below: 

```

// Namespacing an immediately invoked function that returns all public functions 
var Module = (function() {

	// an object defined using object literal notation, 
	// consisting of all commonly used values/selectors 
	var _config = {
		selectorOne: $('.class')
	}

	// initializes the module 
	function init() {
		_bindUIActions();
	}

	// binds any selectors with the appropriate listeners and calls appropriate 
	// private function 
	function _bindUIActions() {
		selectorOne.click(function() {
			_somePrivateFunction();
		});
	}

	function _somePrivateFunction() {

	}

	return {
		init: init 
	}

}());

// now, Module can simply be initialized by calling its only public function: init 
$(document).ready(function () {
	Module.init()
});
```
To make it easier to understand how each module works, here are some brief descriptions 
for each of them along with the URL mappings they use to contact the server:  

 - **`UserTabNavigationHandler`**:  Handles tab navigation on user page by extracting the hash part of the URL and using it to generate a class name for the active tab. The appropriate tab is selected using this class name, and active tab class is added to it. To deselect all the other tabs, active tab class is removed from all the sibling tabs of the active tab. The hash is also used to show the contents of the right div under the tabs.
 
 - **`WorldMapModal`**:  Handles a modal containing a map as its body content. Once the modal is visible, info about all user logs is retrieved from the server using the username of the current user. This info is used to mark all log locations on the map with their corresponding timestamps. The following URL mapping is used:
	 -  `/mytravelog/log/get_info_for_map/<username>/`
 
 -  **`AddOrEditAlbumModal`**:  Handles a modal which allows a user to add or edit an album. Every time a new album is created, all input fields are reset. If an album is being edited, then all the data about a specific album is retrieved from the custom attributes defined on a 'delete album' button and set on the input fields. When the user clicks on Add or Save, the form is submitted to the server as a `POST` request. On success, the page is reloaded, else, an error message is displayed. The following URL mappings are used: 
	 - `/mytravelog/album/create/`
	 - `/mytravelog/album/update/<album_id>/`
 
 - **`DeleteAlbumModal`**:   Handles a modal which allows a user to delete an existing album. When the modal is shown, info about the album being deleted is retrieved from the custom attributes defined on the delete album button. When the user clicks on Delete, a `POST` request is sent to the server. On success, the page is reloaded, else, an error message is displayed. The following URL mapping is used: 
	 - `/mytravelog/album/delete/<album_id>/`
 
 - **`AddLogModal`**: Handles a modal which allows the user to add a new log. Every time this modal is shown, all input fields are reset and a new file input field is added. A map at the top of the modal showing the current position of the user, is also reset. If user clicks on 'add another image' button, a new file field with an incremented name (For example: if log_picture_1 already exists, then log_picture_2 is added) is added. When the user clicks on Add, the form is submitted to the server as a `POST` request. On success, the page is reloaded, else, an error message is displayed. The following URL mapping is used: 
	 - `/mytravelog/log/create/`
 
 - **`DeleteLogModal`**:  Handles a modal which allows a user to delete an existing log. When the modal is shown, info about the log being deleted is retrieved from the custom attributes defined on the log div. When the user clicks on Delete, a `POST` request is sent to the server. On success, the page is reloaded, else, an error message is displayed. The following URL mapping is used: 
	 - `/mytravelog/log/delete/<log_id>/`
 
 - **`EditLogModal`**: Handles a modal which allows the user to edit an existing log. Every time this modal is shown, all input fields are reset and a new file input field is added. A map at the top of the modal showing the position of the user when the where the log was create, is also reset. If user clicks on 'Add another image' button, a new file field with an incremented name (For example: if log_picture_1 already exists, then log_picture_2 is added) is added. Previously saved log images are also displayed. Whenever the user clicks on any of these images, their id is appended to a hidden input field. When the user clicks on Save, the form is submitted to the server as a `POST` request. On success, the page is reloaded, else, an error message is displayed. The following URL mapping is used: 
	 - `/mytravelog/log/edit/<log_id>/`
 
 - **`LogPicturesViewer`**:  Handles a modal which allows the user to view an enlarged version of the log picture they click on. Every time this modal is shown, a list of all URLs of the neighbouring pictures is obtained, and the index of the selected picture is calculated. This index is used to navigate between the list of images.

 - **`LikeHandler`**:  Handles clicks on like button that are present on every log. Whenever a log is liked, a POST request is sent the server along with the id of the log in the URL. On success, the profile picture of the liker is added to a liker-profile-pictures container, and the like count is incremented. At most 14 pictures of the most recent likers are allowed in this container. Since each picture gets appended to this container, any picture after the first 14, gets removed. If a post is disliked, a `POST` request is sent again, and the disliker's profile picture is removed on getting a successful response from the server. The like count is decremented as well. The following URL mappings are used: 
	 - `/mytravelog/like/create/<log_id>`
	 - `/mytravelog/like/delete/<log_id>`
 
 - **`CommentHandler`**:  Handles ENTER key presses on the comment input field which is present on each log. When the user presses enter, a `POST` request is sent to the server along with the comment body and id of the log on which the comment is posted. On success, the comment is added to the body of the log along with a time stamp and user details, and the comment count is incremented. A DELETE button is also added under the comment, allowing the user to delete their comments. If the delete button is clicked, the comment is removed from the log body and comment count is decremented. The following URL mappings are used: 
	 - `/mytravelog/comment/create/<log_id>`
	 - `/mytravelog/comment/delete/<comment_id>`
 
 - **`ShareLogModal`**:  Handles a modal which allows the user to share the selected log on other social networking websites: `Facebook`, `Twitter` and `Google Plus`. When the modal is shown, the selected log's location and creation time are retrieved using the custom attributes defined on the log itself. This info is just used to let the user know what they are about to share. When the user clicks on any of the icons representing each website, they are navigated to the sharing page of that particular website along with the URL they were trying to share. This final URL is generated by appending the URL of the selected log to the base URL of each of the websites.

 - **`FollowerHandler`**:  Handles clicks on follow buttons that are present on search and user pages. Whenever such a button is clicked, the id of the person who the user wants to follow, is retrieved from a custom attribute on the button itself. This id is appended to the URL and sent to the server as a `POST` request. On success, active class is added to the button, indicating the the operation was successful. If the use tries to un-follow another user, a similar `POST` request is sent again, but this time the active class is removed from the button. The following URL mappings are used: 
	 - `/mytravelog/follower/create/<following_user_profile_id>`
	 - `/mytravelog/follower/delete/<following_user_profile_id>`
 
 - **`CityTabNavigationHandler`**:  Handles tab navigation on city page by extracting the hash part of the URL and using it to generate a class name for the active tab. The appropriate tab is selected using this class name, and active tab class is added to it. To deselect all the other tabs, active tab class is removed from all the sibling tabs of the active tab. The hash is also used to show the contents of the right div under the tabs.
 
 - **`CityWeatherForecastHandler`**:  Handles the fetching, parsing and displaying the weekly weather forecast for a particular city on city page. First, the city name is retrieved and then it is appended to the base URL of the Weather API. The `JSON` response is parsed, and then the parsed data is used to generate `HTML` for each of the 7 days in the week. This `HTML` is then added to the weather container and presented to the user. Also, while the data is being fetched and parsed, a progress bar is displayed, which is then hidden once the process is complete.
 
 - **`CityAutocompleteSuggestionsHandler`**:  Handles the the display of autocomplete suggestions under the search input field on the home page. Whenever the user presses a key, the search term is retrieved from the input field and a `GET` request is sent to the server. The `JSON` response is then used to generate html for the suggestions, which is then appended to the suggestions container. This module also handles clicks on suggestions. Whenever a user clicks on a suggestion, a search term is formed using the full city name this time, and sent to the server again (as a `GET` request to the search URL instead of auto-complete URL). But this time, since the search matches exactly one city, the user is directly navigated to it. The following URL mapping is used: 
	 - `/mytravelog/city/autocomplete/`
	 - `/mytravelog/search/` 

 - **`LeaderBoardHandler`**:  Handles the sorting of fields in the leaderboard table on the leaderboard page. Whenever a field heading is clicked, the order in which the fields should be sorted is retrieved by checking if a down or up caret exists in the heading. If it's a down caret, order is ascending, else, the order is descending. Then all the other parameters (query, orderBy and page) are retrieved from the current URL and a new URL is generated using them. The user is eventually redirected to this new URL. This module also handles clicks on pagination buttons, by going through the same process. The following URL mapping is used: 
	 - `/mytravelog/leaderboard/<model>/`

> **Note**: 
> Not all modules are initialized on every page load. Only the relevant modules are initialized, based on the current page URL. 


----------
## Testing ##
 The test directory  `selp/mytravelog/tests` has the following structure: 

    tests/
	    test_images/
			   large_image.jpg
			   small_image.jpg
	    __init__.py
	    tests.py
		util.py

These files are: 

 - The inner **`test_images/`** directory consists of two images: a large image (size > 2 mb) and a small image. These images are used for testing file uploads.
 - **`__init__.py`**:  An empty file that tells Python that this directory should be considered a Python package.
 - **`tests.py`**: Main test file consisting of all unit and functional tests, divided into multiple classes. 
 - **`util.py`**: Consists of utility functions such as functions for populating test database with sample data. 

To run the entire test suite, all you need to do is execute the following command from the project root directory `selp/`: 
```
$ python manage.py test
```   
If you want to check the coverage of these tests, run the tests using the following command:
```
$ coverage run --source='.' manage.py test
```
Now, to view the detailed report showing which parts of the code are being exercised by the tests:
```
$ coverage report
```
For a nicer presentation detailing missed lines: 
```
$ coverage html
```
Then visit `htmlcov/index.html` in your browser. 

> **Note: Deleting test image files** 
> When testing file uploads, do not forgot to delete the test image files that get uploaded to your `media` directory by your views. Even if you have set to delete files on the deletion of modal instances, test images are not deleted automatically.  Use the provided `delete_all_test_image_files` function found in `tests/uitl.py` in an overridden `tearDown` method for your specific file upload test. 

----------


## Debugging ##
To enable debugging in Django, you simply have to set `DEBUG` attribute's value to TRUE. This can be done in the project settings file: `selp/settings.py`. Once this has been done, the debug mode would be turned on, and a detailed error message would be displayed in the browser every time an exception is raised. Each message would consist of a detailed traceback, including a lot of metadata about your environment, such as all the currently defined Django settings. 

> **Note**: 
> Do not deploy the site into production with `DEBUG` turned on! When `DEBUG`=TRUE, Django will remember every `SQL` query it executes, rapidly consuming memory on a production server. 

If such an exception is raised during an `AJAX` request, then you can view it in the `JavaScript` console of the browser.

## Developed by 

*  Manas Bajaj - <manas.bajaj94@gmail.com>