# QuykHtml
Use Python to quickly create, style, and manipulate web elements to create websites very quyckly :D.

# Example
```python

from QuykHtml import qhtml
q = qhtml()

# inline quick way
p_element = q.new("p").set_text("chain together commands :D").style.set("font-size:24px;").onClick('alert("You clicked me :D");')
q.display.style.set("text-align:center").insert(p_element).render()

# readable way

p_element = q.new("p").
p_element.set_text("Or don't chain them together")
p_element.style.set("font-size:24px;")
p_element.onClick('alert("You clicked me :D");')

# insert into our display and render one liner
q.display.style.set("text-align:center;").insert(p_element).render()

# or do the same as above, in a more readable way
q.display.style.set("text-align:center;")
q.display.insert(p_element)
q.render()

```

# See:

[QuykHtml Docs](https://mwd1993.github.io/QuykHtml/)
