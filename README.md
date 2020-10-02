# QuykHtml
Use Python to create, style, and manipulate web elements to build websites and elements very quyckly :D.

# Example
```python

from QuykHtml import qhtml

# Instantiate class
q = qhtml()

# Easily 'import' bootStrap utilities
q.bootStrap.use(True)

# Write direct css - we want to text align all divs for this example
# our final display object we append everything to is a div
q.styleSheet.add("div","text-align:center;")

# Inline quick way to define a p element and set several different types of values
# order doesn't matter as each method call returns the object itself
p_element = q.new("p").set_text("chain together commands :D").style.set("font-size:24px;").onClick('alert("You clicked me :D");')

# Doing the same as above, in a more readable way
p_element = q.new("p")
p_element.set_text("Or don't chain them together")
p_element.style.set("font-size:24px;")
p_element.onClick('alert("You clicked me :D");')

# Insert into our display and render using one liner
q.display.insert(p_element).render()

# Or do the same as above, in a more readable way
q.display.insert(p_element)
q.render()

# The render method can be used on the qhtml object itself or
# on any element created by .new(type), it will render the whole page

```

# See Docs and a lot more examples:

[QuykHtml Docs](https://mwd1993.github.io/QuykHtml/)
