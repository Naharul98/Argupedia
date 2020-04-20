Running Instructions:
• Extract the project.
• Navigate to the path of the project using command prompt:
	> cd <project location>
• Navigate to the scripts folder using command prompt:
	> cd Scripts
• Activate virtual environment:
	> activate.bat (for windows)
	> activate (for linux)
• Back out of the folder into the root folder:
	> cd ..
• Run the following command:
	> python manage.py runserver
• This will start the web-server. A URL will be displayed in the command prompt. Copy the URL into a browser to access the website.

Note: 
If website runs into issues, reinstall the dependencies after activating virtual environment, by executing the following command:

> pip install -r requirements.txt

and then running the website by executing the following command while being in the root folder in command prompt:

> python manage.py runserver

