from QuykHtml import qhtml

q = qhtml()
q.styleSheet.add("td","text-align:center;width:25%;")
q.styleSheet.add(".title",
                 'color:white;font-size:42px;background-color:#085d82;padding-top:50px;padding-bottom:50px;padding-left:60px;')
q.styleSheet.add(".title_desc", 'font-size:38px;font-weight:bold;font-weight:bold;')
q.styleSheet.add(".method-name", "font-size:20px;font-weight:bold;")
q.styleSheet.add(".method-return", "font-size:14px;padding-bottom:20px;")
q.styleSheet.add(".faq-q", "font-size:28px;font-weight:bold;")
q.styleSheet.add(".faq-a", "font-size:18px;color:gray;width:50%;margin:auto;")
q.styleSheet.add(".body-desc", "font-weight:bold;font-size:18px;width:40%;margin:auto;margin-bottom:20px;color:gray;")
q.styleSheet.add(".button",
                 "border:solid 2px #183623;text-align:center;font-size:32px;color:white;background-color:#25633d;padding:6px;width:80%;cursor:pointer;border-radius:4px;margin:auto;")
q.styleSheet.add(".button-left",
                 "border:solid 2px #183623;text-align:center;font-size:32px;color:white;background-color:#25633d;padding:6px;width:80%;cursor:pointer;border-radius:4px;margin:auto;")
q.styleSheet.add(".body-methods", "text-align:center;clear:both;margin-bottom:60px;display:none;padding-top:80px;")
q.styleSheet.add(".example-p", "font-size:32px;font-weight:bold;color:gray;")
q.styleSheet.add(".foot",
                 "height:40px;text-align:center;clear: both;position:fixed;bottom:0px;width:100%;background-color:#085d82;width:99%;")
q.styleSheet.add("img", "border-radius:4px;")

q.scripts.append('var _image_cycle_count = 0;')
q.scripts.append('function _show(self){'
                 'if(self.innerText == "Methods"){'
                 'document.getElementById("b_f").style.display = "none";'
                 'document.getElementById("b_m").style.display = "block";'
                 'document.getElementById("b_e").style.display = "none";'
                 'document.getElementById("b_m").scrollIntoView();'
                 '}else if(self.innerText =="FAQS"){'
                 'document.getElementById("b_m").style.display = "none";'
                 'document.getElementById("b_f").style.display = "block";'
                 'document.getElementById("b_e").style.display = "none";'
                 'document.getElementById("b_f").scrollIntoView();'
                 '}else if(self.innerText =="Examples"){'
                 'document.getElementById("b_m").style.display = "none";'
                 'document.getElementById("b_f").style.display = "none";'
                 'document.getElementById("b_e").style.display = "block";'
                 'document.getElementById("b_e").scrollIntoView();'
                 '}'
                 '}'
                 'function _hover(self){'
                 'self.style.width="40%";'
                 '}'
                 'function _hover_leave(self){'
                 'self.style.width="40%";'
                 '}'
                 '')

q.scripts.append('function _image_cycle(){'
                 '_image_cycle_count+=1;'
                 'var images = ["image.png","body_img2.png","body_img2.png"];'
                 'document.getElementById("_body_image").src = images[_image_cycle_count];'
                 'if(_image_cycle_count >= images.length-1){'
                 '_image_cycle_count = -1;'
                 '}'
                 '}')
q.scripts.append('window.onload=function(){setInterval(function(){_image_cycle();},5000)}')

final = q.new("div")

title = q.new("p").set_text("QuykHtml").add_attribute('class="title"').style.set("color:#085d82;")
title_desc = q.new("p").set_text("Generate HTML quickly").set_class("title_desc")

logo = q.new("img").add_attribute('src="logo.png"').style.set("position:absolute;left:20px;top:20px;")

github = q.new("img").add_attribute('src="github.png"').style.set(
    "position:absolute;right:20px;top:50px;width:280px;cursor:pointer;").on_click(
    'window.location=\'https://github.com/mwd1993/QuykHtml\'')

body = q.new("div").style.set("text-align:center;")
body_desc = q.new("p").set_text(
    "QuykHtml is a python library that allows you to quickly generate websites. The key is to chain together commands to quickly define, combine and modify elements.").set_class(
    "body-desc")
body_img = q.new("img").add_attribute('src="image.png"').style.set(
    "border-radius:4px;width:40%;margin:auto;").on_mouse_enter("_hover(this);").on_mouse_leave("_hover_leave(this);").add_attribute('id="_body_image"')

# buttons = q.new("div").style.set("height:80px;width:40%;;margin:auto;")
b_examples = q.new("p").set_text("Examples").on_click("_show(this);").set_class("button-left")
b_methods = q.new("p").set_text("Methods").on_click("_show(this);").set_class("button")
b_faqs = q.new("p").set_text("FAQS").on_click("_show(this);").set_class("button")

body_methods = q.new("div").add_attribute('id="b_m"').set_class("body-methods")
body_methods.insert(q.new("p").set_text('<span style="color:red;">QuykHtml Object</span>').style.set("font-size:42px;"))
body_methods.insert(q.new("p").set_text(
    '<span style="color:red">Object</span>.new( type )<br><br>Returns:<span class="method-return"> <span style="color:orange;">Element Object</span> - Returns an Element Object</span>').set_class(
    "method-name"))
body_methods.insert(q.new("p").set_text(
    '<span style="color:red">Object</span>.render()<br><br>Returns: <span class="method-return">The Raw HTML and opens chrome to render the HTML</span>').set_class(
    "method-name"))
body_methods.insert(q.new("p").set_text(
    '<span style="color:red">Object</span>.generate_skeleton()<br><br>Returns: <span class="method-return">N/A - Generates a simple skeleton of a website in the program directory</span>').set_class(
    "method-name")).insert(q.new("hr").style.set("width:50%;margin:auto;"))

body_methods.insert(
    q.new("p").set_text('<span style="color:orange;">Element Object</span>').style.set("font-size:42px;"))

body_methods.insert(q.new("p").set_text(
    '<span style="color:orange">Object</span>.style.set( html_style_string )<br><br>Returns:<span class="method-return"> <span style="color:orange;">Self</span> - Styles the element IE: "font-size:12px;color:red;"</span>').set_class(
    "method-name"))
body_methods.insert(q.new("p").set_text(
    '<span style="color:orange">Object</span>.insert(<span style="color:orange;">Element Object</span>)<br><br>Returns: <span class="method-return"> <span style="color:orange;">Self</span> - Insert an element object into another</span>').set_class(
    "method-name"))
body_methods.insert(q.new("p").set_text(
    '<span style="color:orange">Object</span>.add_attribute( str_attribute )<br><br>Returns: <span class="method-return"><span style="color:orange;">Self</span> - Applies an attribute to an element IE: \'class="test-class\' or \'onclick="alert(\'clicked!\');"</span>').set_class(
    "method-name"))
body_methods.insert(q.new("p").set_text(
    '<span style="color:orange">Object</span>.set_text( str_text )<br><br>Returns: <span class="method-return"><span style="color:orange;">Self </span>- Sets the innerText value of the Element</span>').set_class(
    "method-name")).insert(q.new("hr").style.set("width:50%;margin:auto;"))

body_faqs = q.new("div").style.set("text-align:center;clear:both;padding-top:80px;padding-bottom:80px;").add_attribute(
    'id="b_f"').style.append("display:none;")

table = q.tables.new(3, 1, [
    {"value": b_examples, "row": "1", "column": "1"},
    {"value": b_faqs, "row": "1", "column": "2"},
    {"value": b_methods, "row": "1", "column": "3"}
]).style.set("width:50%;margin:auto;margin-top:60px;")

body_faqs.insert(q.new("p").set_text("What is QuykHtml?").set_class("faq-q"))
body_faqs.insert(q.new("p").set_text(
    "QuykHtml was designed to make creating website elements really fast and modifying and structuring them with ease.").set_class(
    "faq-a"))
body_faqs.insert(q.new("p").set_text("What python Libraries are required?").set_class("faq-q"))
body_faqs.insert(q.new("p").set_text("The only Libraries required are webbrowser, os and time").set_class("faq-a"))
body_faqs.insert(q.new("p").set_text("How many developers are working on QuykHtml").set_class("faq-q"))
body_faqs.insert(q.new("p").set_text("Currently only one person.").set_class("faq-a"))

body_examples = q.new("div").style.set(
    "text-align:center;clear:both;padding-top:80px;padding-bottom:80px;").add_attribute('id="b_e"').style.append(
    "display:none;")
body_examples.insert(q.new("p").set_text("Create a div and place a paragraph inside:").set_class("example-p"))
body_examples.insert(q.new("img").add_attribute('src="example1.png"'))
body_examples.insert(q.new("p").set_text("Style a Paragraph using inline styling").set_class("example-p"))
body_examples.insert(q.new("img").add_attribute('src="example2.png"'))
body_examples.insert(q.new("p").set_text("Style a Paragraph using classes").set_class("example-p"))
body_examples.insert(q.new("img").add_attribute('src="example3.png"'))
body_examples.insert(
    q.new("p").set_text("Set the elements id and set the place holder attribute on the element as well.").set_class(
        "example-p"))
body_examples.insert(q.new("img").add_attribute('src="example4.png"'))

foot = q.new("div").set_class("foot")

foot.insert(q.new("p").style.set("font-weight:bold;color:white;").set_text("This website was made using QuykHtml"))
# buttons.insert(b_examples).insert(b_methods).insert(b_faqs)
body.insert(logo).insert(title_desc).insert(body_desc).insert(body_img).insert(table).insert(github)
final.insert([title, body, body_methods, body_faqs, body_examples, foot])

q.render()
