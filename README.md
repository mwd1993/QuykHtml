# QuykHtml
A python library that allows you to quickly and easily generate HTML templates and even create full-on websites.<br><br>
Key Features:<br>
	- [Chaining together commands](#example-miscellaneous)<br>
	- [Write Javascript/jquery in your IDE or include from a file](#example-javascript-code)<br>
	- [Easy Table system](#example-tables)<br>
	- [Easy Ajax Setup and Calls](#example-ajax-request)<br>
	- [Easy Form Submissions](#example-forms)<br>
	- [Bootstrap Support](#example-miscellaneous)
	

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

# Specific Element setters
q.new("img").set_img_src('src_url')
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

# Easily 'import' bootStrap utilities
q.bootStrap.use(True)

# Create the container for the table to be built into
table = q.new("div").style.set("width:80%;margin:auto;")

# Create raw table of 1 row and 2 columns
table_raw = q.table(1,2)

# Insert method using 0 based index -> insert_at(row,column,qhtml_object)
table_raw.insert_at(0,0,q.new("p").set_text("Row 1 column 1"))
table_raw.insert_at(0,1,q.new("p").set_text("Row 1 column 2"))

# Also valid syntax
table_raw = q.table(1,2).insert_at(0,0,q.new("p").set_text("Row 1 column 1")).insert_at(0,1,q.new("p").set_text("Row 1 column 2"))

# Td manipulation examples
for i in range(2): 
	table_raw.style_td_at(0,i,'text-align:center')
	table_raw.set_td_class_at(0,i,'some-class')
	table_raw.set_td_id_at(0,i,'some-id' + str(i))

# Build raw table into table container
table_raw.build_into(table)

# Render the results
q.display.insert(table).render()
	
```

# Example: JavaScript Code

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Easily 'import' bootStrap utilities
q.bootStrap.use(True)

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

# Easily 'import' bootStrap utilities
q.bootStrap.use(True)

# Create an ajax request on the p element
# Always specify r in the callback function as that is the response text
p = q.new("p").ajax_build('get','file.php?args=1&args2=2","_some_call_back_func(r)')

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

# Easily 'import' bootStrap utilities
q.bootStrap.use(True)

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

# Example: Miscellaneous

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Chaining commands
q.new("p").set_text('some text').set_class('text-class').set_id('text-id').on_click("alert('clicked me');").style.set("cursor:pointer;")

# Bootstrap - Support
q.bootstrap.use(True)

div = q.new("div").set_class("row")
div_col1 = q.new("div").set_class("col").set_text("column1")
div_col2 = q.new("div").set_class("col").set_text("column2")
div.insert([div_col1,div_col2])

# Bootstrap - Also valid syntax
div = q.new("div").set_class("row").insert([
	q.new("div").set_class("col").set_text("column1"),
	q.new("div").set_class("col").set_text("column2")
])

# Append to the head tag
q.head.append('<script type="text/javascript" src="path/to/js_code.js"></script>')
q.head.append('<link rel="stylesheet" href="path/to/css.css">')

# Built in color helpers
q.css.colors.LIGHT_GRAY
q.css.colors.DARK_GRAY
q.css.colors.LIGHT_GREEN
q.css.colors.DARK_GREEN
# and more..

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
