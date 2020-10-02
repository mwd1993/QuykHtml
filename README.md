# QuykHtml
Use Python to quickly create, style, and manipulate web elements to create websites very quyckly :D.

# Example
```python

from QuykHtml import qhtml
q = qhtml()
p_element = q.new("p").set_text("chain together commands :D").style.set("font-size:24px;")
q.display.style.set("text-align:center").insert(p_element).render()

```

# See:

[QuykHtml Docs](https://mwd1993.github.io/QuykHtml/)
