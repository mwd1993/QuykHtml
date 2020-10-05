# QuykHtml
QuykHtml is a python library that allows you to quickly generate websites. The key is to chain together commands to quickly define, combine and modify elements.<br>
Since each method call from a 'QuykHtml.new(type) object' returns itself, allowing you quickly modify the element, chaining together commands.

# Quick Examples
###### Creating Elements

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

```

###### Styling Elements

```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Declare css, the add method allows for a list of lists, with the first value being<br>
# classname and the markup/style string for the second value
css = q.css.add([["div","font-size:32px;"],[".div_custom","color:gray;"]])

# Create a div, inherits from div and .div_custom css values
div = q.new("div").set_class("div_custom").set_text("QuykHtml Rocks!")

# Or use inline styling to style the element
div = q.new("div").style.set("font-size:48px;color:green;").set_text("QuykHtml Rocks!");

```

# Example
Create a Paragraph element, manipulate it in several ways, append it to the display and render the webpage<br>
Note: The render function will attempt to open the resultant webpage. The function also returns the Raw HTML of the website generated.
```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Easily 'import' bootStrap utilities
q.bootStrap.use(True)

# Write direct css - we want to text align all divs for this example
# our final display object we append everything to is a div
q.css.add("div","text-align:center;")

# Inline quick way to define a p element and set several different types of values
# order doesn't matter as each method call returns the object itself
p_element = q.new("p").set_text("chain together commands :D").style.set("font-size:24px;").onClick('alert("You clicked me :D");')

# Doing the same as above, in a more readable way
p_element = q.new("p")
p_element.set_text("Or don't chain them together")
p_element.style.set("font-size:24px;")
p_element.onClick('alert("You clicked me :D");')

# Insert into our display (the main container you should 
# insert everything into) and render using a one liner
q.display.insert(p_element).render()

# Or do the same as above, in a more readable way
q.display.insert(p_element)
q.render()

# The render method can be used on the qhtml object, qhtml.display object or
# on any element created by .new(type), it will render the whole page regardless

```

# See Docs and more examples below:

[QuykHtml Docs](https://mwd1993.github.io/QuykHtml/)
