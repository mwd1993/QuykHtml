# QuykHtml
A python library that allows you to quickly and easily generate HTML templates and even create full-on websites.<br><br>

If you are feeling generous or would like to buy me a coffee or donate, below is my cash app:  
```cash app: $elmling```

# pip install QuykHtml

[![Downloads](https://pepy.tech/badge/quykhtml)](https://pepy.tech/project/quykhtml)

 ![](Example3.gif)
 
 New Features:  
 	- [Express](#example-express)<br>

Key Features:<br>
	- [Flask](#example-quykhtml-with-flask)<br>
	- [Chaining together commands](#example-miscellaneous)<br>
	- [Javascript/jQuery support](#example-javascript-code)<br>
	- [Table Creation](#example-tables)<br>
	- [Ajax Creation](#example-ajax-request)<br>
	- [Form Creation](#example-forms)<br>
	- [Boostrap](#example-miscellaneous)<br>
	- [SEO](#example-SEO)<br>
	- [Landing Page Example](#example-simple-landing-page1)
	

# Example: Hello World in 4 lines

```python
# Import the class from the library
from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Insert a modified p element into our main display
q.display.insert(q.new('p').set_text('Hello World').set_id('text-id').style.set('font-size:24px;'))

# Render the page
q.display.render()
```	

# Example: Basic Declaration

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Create a div
div = q.new("div")

#  Create a paragraph
p = q.new("p")

#  Create an input
input = q.new("input")

# Render the results by inserting all objects to display
q.display.insert([div, p, input]).render()

```

# Example: Element Styling

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Declare css, allows for a list of lists, with the first value being
# classname and the markup/style string for the second value
q.css.add([["div","font-size:32px;"],[".div_custom","color:gray;"]])

# You can also do the same by just calling the add method with two arguments
q.css.add("div","font-size:32px;")
q.css.add(".div_custom","color:gray;")

# Create a div with the class .div_custom and set the text in the div
div = q.new("div").set_class("div_custom").set_text("QuykHtml Rocks!")

# You can use inline styling to style the element and set the text in the div
div2 = q.new("div").style.set("font-size:48px;color:green;").set_text("QuykHtml Rocks!")

# Render the results
q.display.insert([div, div2]).render()

```

# Examples: Element Setters

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

p = q.new("p")

# Global Element Setters
p.style.set('color:red;')
p.style.append('background-color:yellow;')
p.add_attribute('title="Qhytml is easy!"')
p.set_text('text')
p.set_text_ipsum()
p.set_text_ipsum_large()
p.set_text_ipsum_small()
p.set_class('class1 class2')
p.set_form_button()
p.set_id('my-id')
p.set_name('some-name')
p.set_value('custom value')
p.set_tool_tip('simple hover text tool tip')
p.on_click("alert('i was clicked!');")
p.on_click_goto('google.com')
p.on_right_click("alert('i was right clicked!');")
p.on_mouse_enter("alert('Mouse entered!');")
p.on_mouse_leave("alert('Mouse left!');")
html = p.html()

# Specific Element setters
q.new("img").set_img_src('src_url')
q.new("img").set_img_placeholder(400)
q.new("img").on_click_showPreview()
q.new("form").set_form_options('file.php','get')
q.new("button").set_form_button()
q.new("iframe").set_iframe('google.com')
q.new("input").set_auto_complete(False)

```

# Example: Tables

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# Create raw table of 1 row and 2 columns
table = q.table(1,2)

# Insert method using 0 based index -> insert_at(row,column,qhtml_object or list of qhtml_objects)
table.insert_at(0,0,q.new("p").set_text("Row 1 column 1"))
table.insert_at(0,1,q.new("p").set_text("Row 1 column 2"))

# Also valid syntax
table = q.table(1,2).insert_at(0,0,q.new("p").set_text("Row 1 column 1")).insert_at(0,1,q.new("p").set_text("Row 1 column 2"))

# Td manipulation examples
for i in range(2): 
	table.style_td_at(0,i,'text-align:center')
	table.set_td_class_at(0,i,'some-class')
	table.set_td_id_at(0,i,'some-id' + str(i))

# Make sure to build the table 
# which returns a div with the table code in it
table = table.build()

# Render the results
q.display.insert(table).render()
	
```

# Example: JavaScript Code

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# Append a script, can even be read from a file
q.scripts.append(
	'function js_function() {'
	'	alert("A JS Function");'
	'}'
)

# Append a script to a qhtml object
p = q.new("p").set_text("Text element").scripts_add(
	'function js_function() {'
	'	alert("A JS Function");'
	'}'
)

# Append code to be executed on page load to a qhtml object
p = q.new("p").set_text("Text element").scripts_add('alert("Js code ran on page load");', on_page_load=True)

q.display.insert(p).render()

```

# Example: Ajax Request

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# Create an ajax request on the p element
# Always specify r in the callback function as that is the response text
p = q.new("p").ajax_build('get','file.php?args=1&args2=2","_some_call_back_func(r)')

# Quickly define the function if need be
p.scripts_add('function _some_call_back_func(r){alert("Response text " + r.responseText);}')

# Append JS Code for when the page loads, call the ajax function using
# element.ajax_get("pointer") <- the 'ajax method built by ajax_build'
p.scripts_add(p.ajax_get("pointer"),on_page_load=True)

q.display.insert(p).render()

```

# Example: Forms

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# Create form element
form = q.new("form").set_form_options('file.php','post')

# Create the input element and set the name to form_name
input = q.new("input").set_name('form_name')

# Create the button and use method .set_form_button() to 
# make it send the form when it is clicked
button = q.new("button").set_text("submit").set_form_button()

# Insert the form elements into the form
form.insert([input,button])

q.display.insert(form).render()

```

# Example: Express
Easily use the official markup language (uses bootstrap)  
to quickly and easily define qhtml objects.  
#### Express Rules:  
	- use attr-'attributename' to declare normal html element attributes  
	- use 'attributename' to attempt to use ANY Qhtml setter methods on an element  
	- you declare columns by element position in the list  
	- each list item is essentially a row  
	- requires bootstrap (instantiate with qhtml method)
	

#### create a 3 columned row
```python
# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# express method returns
# an actual qhtml object
layout = q.express([
	['div','p','div']
]).style.set('background-color:#45afed;')

q.display.insert(layout).render()
```

#### create a 3 columned row and define html values
```python
# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# express method returns
# an actual qhtml object
layout = q.express([
	['div attr-class="myclass"','p attr-id="myid"','div attr-style="background-color:red"']
]).style.set('background-color:#45afed;')

q.display.insert(layout).render()
```
#### create a 3 columned row and call Qhtml setter methods on said element
```python
# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# a Qhtml object has a method called: set_text
# it also a method called: set_img_src
# so we omit the 'set_' prefix. So instead of
# set_text("some text"), we simply use text="some text"
# to call said method
layout = q.express([
	['div','p text="QuykHtml Rocks!"','div'],
	['div','img img_src="myimagesource.com" attr-class="myImgClass"','div']
]).style.set('background-color:#45afed;')

q.display.insert(layout).render()
```

## Express Real World Example

### create a simple form

```python
# Instantiate class
q = qhtml()

# Easily 'import' bootstrap utilities
q.bootstrap.use(True)

# Define some css
q.css.add('.center','text-align:center;')

# Create our form elements
layout = q.express([
	['div', 'p text="Email"', 'div'],
	['div', 'input', 'div'],
	['div', 'p text="Password"', 'div'],
	['div', 'input', 'div'],
	['div', 'p text="Confirm"', 'div'],
	['div', 'input', 'div'],
	['div', 'button text="Complete" attr-value="submit" attr-class="margin-top-med signup"', 'div']
]).set_class("center", True)

# Create the actual form container element
form = q.new('form').set_class('center')

# Insert the form elements and set the form options
form.insert(layout).set_form_options("register.php", "post")

# Render the results
q.display.insert(form)
```

# Example: SEO

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Define some SEO
q.seo.set_page_title('Page Title')
q.seo.set_page_author('Author')
q.seo.set_page_keywords('some key words')
q.seo.set_page_encoding('UTF-8')
q.seo.set_page_auto_refresh(30)  # refresh every 30 seconds

list_of_seo = q.seo.display_all_seo()

```

# Example: Miscellaneous

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Chaining commands
q.new("p").set_text('some text').set_class('text-class').set_id('text-id').on_click("alert('clicked me');").style.set("cursor:pointer;")

# Render arguments examples
# output_file str_path, only_html boolean, set_clip_board boolean
q.display.insert(q.new("p.").set_text("Render Arguments")).render(output_file="file/path/file.html")
q.display.insert(q.new("p.").set_text("Render Arguments")).render(only_html=True)
q.display.insert(q.new("p.").set_text("Render Arguments")).render(output_file="file/path/file.html",set_clip_board=True)
q.display.insert(q.new("p.").set_text("Render Arguments")).render(only_html=True,set_clip_board=True)
q.display.insert(q.new("p.").set_text("Render Arguments")).render()

# ------------------------------
# Bootstrap - Support
# ------------------------------
q.bootstrap.use(True)

div = q.new("div").set_class("row")
div_col1 = q.new("div").set_class("col").set_text("column1")
div_col2 = q.new("div").set_class("col").set_text("column2")
div.insert([div_col1,div_col2])

# Also valid syntax
div = q.new("div").set_class("row").insert([
	q.new("div").set_class("col").set_text("column1"),
	q.new("div").set_class("col").set_text("column2")
])
# ------------------------------

# Append to the head tag
q.head.append('<script type="text/javascript" src="path/to/js_code.js"></script>')
q.head.append('<link rel="stylesheet" href="path/to/css.css">')

# Built in color helpers
c = q.css.colors
colors = [c.LIGHT_GRAY, c.DARK_GRAY,c.LIGHT_GREEN,c.DARK_GREEN] # and more..
for color in colors:
	print(color) # - > #hex_value

# Loop through every created object of a qhtml instance
for element in q.all:
	print('Element type - > ' + element.type)
	element.set_text("Overwrite")
	
# Duplicating element objects
p_main = q.new("p").style.set("font-size:32px;")

p1 = q.dupe(p_main).set_text('p tag number 1').style.append('color:red;')
p2 = q.dupe(p_main).set_text('p tag number 2').style.append('color:green;')

# Exporting css styles added to 'q.css'
q.css.add('p','font-size:32px;')
q.css.add('div','text-align:center;')

q.css.export('path/to/export.css')

```
# Example Simple Landing Page1

``` python
from QuykHtml import qhtml

q = qhtml()

q.bootstrap.use(True)

head = q.new('div')
head_text = q.new('p')
head_text.set_text('Example Landing Header').style.align('center').style.font_size('64px;').style.append('padding-top:200px;padding-bottom:200px;background-color:gray;color:white;')
head.insert(head_text)

body = q.new('div').style.set('width:65%;margin:auto;margin-bottom:100px;').set_class('row')
body_text = q.new('p').set_text_ipsum_large().style.font_size('24px').style.align('left').style.append('margin-top:60px;margin-bottom:60px;').style.font_color('gray')
body_img_1 = q.new('img').set_class('col').set_img_placeholder(400).style.height('400px').style.append('margin-top:20px;')
body_img_2 = q.dupe(body_img_1)
body.insert([body_text,body_img_1,body_img_2])

footer = q.new('div').style.align('center').style.set('margin:0px;position:fixed;bottom:0px;width:100%;background-color:gray;padding-top:5px;padding-bottom:5px;')
footer_text = q.new('p').style.set('font-weight:bold;margin:0px;')
footer_text.set_text('Example Footer Text. All Right Reserved.').style.align('center').style.font_size('15px').style.font_color('white')
footer.insert(footer_text)

q.display.insert([head,body,footer]).render()

```

# Example QuykHtml with Flask

## Using pythonanywhere.com



#### Serving HTML using .html() method

```python
# A very simple Flask Hello World app for you to get started with...
from QuykHtml import qhtml
from flask import Flask

q = qhtml()
q.bootstrap.use(True)
app = Flask(__name__)

# always use " " as the outer string quote and ' ' inside if need
on_click_code = "alert('You clicked the button!');"

# Div containing a p element and a button with an on click event
div = q.new('div').style.set('text-align:center;').insert([
    q.new("p").style.font_size('42px').set_text("This works"),
    q.new('button').style.font_size('24px').set_text('click me').on_click(on_click_code)
])

# Div containing a p element with Greeting text in it
div2 = q.new('div').style.set('background-color:gray;text-align:center;').insert([
    q.new('p').style.set('font-size:32px;color:white;font-weight:bold;').set_text('Hello from QuykHtml and Flask!')
])

@app.route('/')
def hello_world():
	# Use .html method on a qhtml object to get it's HTML and serve it
    return div.html() + div2.html()
```

#### Serving HTML using .render('out_put_file.txt') and .file_read('file.txt')

```python
# A very simple Flask Hello World app for you to get started with...
from QuykHtml import qhtml
from flask import Flask

q = qhtml()
q.bootstrap.use(True)

app = Flask(__name__)

# always use " " as the outer string quote and ' ' inside if need
on_click_code = "alert('You clicked the button!');"

# Div containing a p element and a button with an on click event
div = q.new('div').style.set('text-align:center;').insert([
    q.new("p").style.font_size('42px').set_text("This works"),
    q.new('button').style.font_size('24px').set_text('click me').on_click(on_click_code)
])

# Div containing a p element with Greeting text in it
div2 = q.new('div').style.set('background-color:gray;text-align:center;').insert([
    q.new('p').style.set('font-size:32px;color:white;font-weight:bold;').set_text('Hello from QuykHtml and Flask!')
])

# Place objects in the display and render out the file to test.txt
q.display.insert([div,div2]).render(output_file='test.txt', only_html=True)

@app.route('/')
def hello_world():
	# Use file_read method to get the rendered HTML and serve it
    html = q.file_read('test.txt')
    return html

```
