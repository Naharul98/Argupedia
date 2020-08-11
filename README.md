# Argupedia
 
An online debate platform which alllows visualization of debates in the form of directed graph and automatically labels arguments as Winning/Losing/Undecided in a given state of the debate

### Features

- Implements [Grounded Extension Algorithm](https://nms.kcl.ac.uk/sanjay.modgil/inf/ProofTheories_and_Algorithms.pdf) to label arguments according to their current position (Winning/Losing/Undecidable)
- Visualizes debates in the form of an interactive directed graph
    - Nodes represent individual arguments in the debate
    - Edges in the graph reflect their attack relation (Which argument is challenging which)
    - Nodes are highlighted according to their labelling by the algorithm (Winning: Green, Losing: Red, Undecidable: Grey)
    - Hover over nodes to view the argument
    - Hover over edges to view the argument structure used
- A range of [Argumentation Schemes](https://www.reasoninglab.com/patterns-of-argument/argumentation-schemes/waltons-argumentation-schemes/) to choose from to allow people engaging in debates to make their arguments more clear and concise.

### Instructions for Running the Project
```
• Activate virtual environment
• Run the following command:
	> python manage.py runserver
• This will start the web-server. A URL will be displayed in the command prompt. Copy the URL into a browser to access the website.

If website runs into issues, reinstall the dependencies after activating virtual environment, by executing the following command:

> pip install -r requirements.txt
```

### Libraries Used
- [Django - 2.2.7](https://www.djangoproject.com)
- [Django-Mptt - 0.9.1](https://django-mptt.readthedocs.io/en/latest/)
- [Bootstrap – 4.3.1](https://getbootstrap.com)
- [JQuery – 3.3.1](https://jquery.com)
- [D3.JS – 4.0](https://d3js.org)
- [Markdown – 3.0.1](https://pypi.org/project/django-markdown/)
- [Bleach – 3.0.2](https://pypi.org/project/django-bleach/)
