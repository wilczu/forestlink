# ForestLink

### What is ForestLink?

ForestLink app allows you to create your personalised desktop with pages. By creating your own desktop you can save some time and have all of the pages which you’re using daily in one place. The application allows you to add and customize your pages.

### Features:

* <b>Authentication</b> - This web application is using the build-in Django authentication system to authenticate users. This process includes filling Register form and then logging in to your account by providing your user name and password.
* <b>Customization</b> - When adding a new website to your desktop you’re able to choose the background colour of the text and background of the tile. 
* <b>Pagination</b> - The content of your desktop is depending only from how many pages you’re going to add to it. Some users might have a lot of pages and that’s why the pagination system is displaying 20 sites per page.  
* <b>Reporting sites</b> - User can report any site which may be insecure and cause harm. Then this report is inspected by the administrator and can be either rejected or blocked. When the website is blocked users are not able to add this website to their desktop anymore. 
* <b>Responsive Web Design</b> - This application is fully responsive and because of that it can work on all platforms and devices.

### What each file is containing

* <i>forest/</i>
  * <b>urls.py</b> - contains paths for all routes of the application.
* <i>templates/forest/</i>
  * <b>layout.html</b> - contains HTML template which is used across all sub-pages. It is also including all the js and CSS files required.
  * <b>index.html</b> - Html for the main website which presents the whole application to the new user.
  * <b>login.html</b> - contains login form with user name and password fields and login button.
  * <b>register.html</b> - contains register form with the user name, email, password and confirm password fields and register button.
  * <b>report.html</b> - contains two sections. First one is a simple form with button to submit your report and the second one is displaying the table of your reports, pagination and menu.
  * <b>user.html</b> - displaying content of user desktop, pagination, modals to edit, remove and add page and menu. 
* <i>static/forest/</i>
  * styles.css - main styles file to define new styles and overwrite or add, edit bootstrap classes.
* <i>static/forest/js/</i>
  * <b>scrolling.js</b> - simple scrolling script for the main menu on the index page. Allows scrolling to the 	appropriate section when clicking on a link.
  * <b>managePage.js</b> - contain functions to enable or disable edit mode on the desktop and showing 	modals. Talking to the API to get data and putting it to the input fields of edit modal.
  
### I believe my project satisfies the distinctiveness and complexity requirements because:

<b>Use of external library.</b> My application is using an external open source library called ‘django-fontawesome-5’ which is supplying the application with icons from well-known site called fontawesome.com. I’m also using it to generate the icon drop-down input field.

<b>Talking to the API when editing page.</b> Inputs from modal which is displaying form when editing the website are pre-filled with this websites’ data. This is achieved because of the API talking to the server and getting data to put it to the inputs of this modal.

User desktop is displaying all of your pages from the newest one and it is limiting the number of sites per page because of the pagination. When hovering on one of your pages the animation made in CSS is going to be executed. Also when edit mode is launched then this hover effect will be disabled and two buttons (edit and delete) will be displayed for every site. This is achieved using JavaScript and a framework called jQuery.

All of the user data is stored inside of the database which contains following rows:
  * User - store all information about the user. (default table from Django authentication system)
  * Page - contains all information about user pages. This table has relationship with User and Color table. This table also contains IconField added by django-fontawesome-5   library.
  * Color - contains colour of the text and background of user’s pages.
  * Report - store all reports made by users. This table also contain the drop-down menu which allows the administrator to accept or deny reports.
