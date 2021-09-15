## Text sum simple
This project is being made for a very special person that is in Med school: Mainha. It's a simple python code that gets a PDF lecture file, and should help the user by giving them a summary of the subject along with some keywords and links that should explain concepts present in the text. 

> Yet not fully ready for use!!

### **Setup**
> Note: Requiered Python version 3 or higher

*After downloading/cloning the repository...*
Download the following packages using ```pip install```: 
- ```python-dotenv```
- ```summa```
- ```ibm-watson```
- ```uuid```
- ```tkinter```
- ```tika```
- ```askopenfilename```

* ...Then you just need to setup env variables (using your IBM Watson Natural Language API credentials: API Key and API URL)*
* ... And finally run it:*
```bash
python3 text_sum.py
```
> A series of quastions may be asked to the user to input, regarding summariztion size, keywords quantity and etc...

* The results should then be pesent in ```results/``` dir*


### **Technologies**
- summanlp's textrank A.I. model -> https://github.com/summanlp/textrank
- tkinter python interface -> https://docs.python.org/3/library/tkinter.html
- chrismattmann's tika -> https://github.com/chrismattmann/tika-python
- uuid -> https://docs.python.org/3/library/uuid.html
- uuid -> https://docs.python.org/3/library/uuid.html
- IBM Watson Natural Language A.I. SaaS
