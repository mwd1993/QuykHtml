import webbrowser
import os
from time import sleep


class qhtml:

    # Initialize class
    def __init__(self):

        # Variables
        # -------------------------------------

        self.all = []
        self.css = self.ss()
        self.scripts = []
        self.display = self.new("div", self)
        self.bootstrap = self.bootstrap()

    # Returns a new object of an html element
    # returns: Object

    def new(self, _type, _p=0):
        _obj = ""

        if _p != 0:
            _obj = self.new_obj(_type, _p)
        else:
            _obj = self.new_obj(_type)

        self.all.append(_obj)
        return _obj

    # Attempts to render the constructed webpage
    # returns: HTML

    def render(self):
        _b = ""
        _scripts = ""
        _path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        _bootstrap = ""
        if self.bootstrap.using():
            _bootstrap = self.bootstrap.get()

        for _s in self.css.styles:
            _b = _b + "" + _s

        for _sc in self.scripts:
            _scripts = _scripts + "" + _sc + "\n"

        html_string = "<head>" + _bootstrap + "<style>" + _b + '</style><script type="text/javascript">' + _scripts + '</script></head>' + str(
            self.all[0].innerHTML)

        f = open(os.getcwd() + "/render.html", "w")
        f.write(html_string)
        f.close()

        print(html_string)

        sleep(0.2)

        webbrowser.get(_path).open(str(os.getcwd()) + "/render.html")

        return html_string

    # Generate a simple QuykHtml skeleton in the script directory
    # returns: HTML String
    def generate_skeleton(self):
        return False

    # CLASS Style sheet attached to the html object

    class ss:

        # INITIALIZE CLASS

        def __init__(self):
            self.styles = []
            self.colors = self._colors()

        # Add a style to an object element
        # returns: class object/itself

        def add(self, name: str or list, style=""):

            if style == "":
                if type(name) is list:
                    for li in name:
                        if type(li) is list:
                            _name = li[0]
                            _style = li[1]
                            self.styles.append(_name + "{" + _style + "}")
                        else:
                            print("Error using add function in class QuykHtml - > ss:")
                            print("Usage: add(style,name) or add([[\"style\",\"name\"],[\"style\",\"name\"]]")
                            return self
            else:
                self.styles.append(name + "{" + style + "}")
                return self

        # Export every style into an external style sheet
        # in the program's directory
        # returns: void

        def export(self, _file):
            if "." not in _file:
                return False
            f = open(_file, "w")
            _b = ""
            for s in self.styles:
                _b = _b + "" + s + "\n"
            print("b = " + _b)
            f.write(_b)
            f.close()

        class _colors:
            def __init__(self):
                self.LIGHT_GRAY = "#9e9e9e"
                self.LIGHT_BLUE = "#699bf5"
                self.LIGHT_RED = "#ed7476"
                self.LIGHT_GREEN = "#53d490"
                self.LIGHT_BROWN = "#82716c"

                self.DARK_GRAY = "#4a4a4a"
                self.DARK_BLUE = "#304873"
                self.DARK_RED = "#633233"
                self.DARK_GREEN = "#21573a"
                self.DARK_BROWN = "#403735"

    # CLASS new_obj, an element object type

    class new_obj:

        # INITIALIZE CLASS

        def __init__(self, _type, _parent=0):
            self.type = _type
            self.children = []
            if _parent != 0:
                self.parent = _parent
            else:
                self.parent = ""
            self.attributes = []
            self.style = self.style_obj(self)
            self.innerHTML = ""
            self.innerText = ""

        # Render - attempts to render the full webpage from the object
        # returns: void

        def render(self):
            if self.parent == "":
                pass
            else:
                self.parent.render()

        # Insert a table into an element as pure html
        # returns: itself/html object

        def insert_table_html(self, html):
            self.innerHTML = html
            return self

        # Insert an object into another object
        # IE: insert a p object inside of a div object
        # returns: itself/html object

        def insert(self, _obj):
            if type(_obj) is list:
                for l in _obj:
                    self.children.append(l)
                    self.innerHTML += l.get_tag_open() + l.innerText + l.innerHTML + l.get_tag_close()
                    self.innerHTML = self.innerHTML.replace("  ", " ")
                    l.parent = self
                    l.__link_self()

            else:
                self.children.append(_obj)
                self.innerHTML += _obj.get_tag_open() + _obj.innerText + _obj.innerHTML + _obj.get_tag_close()
                self.innerHTML = self.innerHTML.replace("  ", " ")
                _obj.parent = self
                _obj.__link_self()

            return self

        # Adds an attribute to an element
        # returns: self/object
        def add_attribute(self, _str):
            self.attributes.append(_str)
            return self

        # Retrieves all attributes from an object
        # returns: html attributes (str)

        def get_attributes(self):
            _b = ""
            for s in self.attributes:
                _b = _b + " " + s
            return _b.strip()

        # Get the full tag of an object as a string
        # returns: string

        def get_tag_open(self):
            return "<" + self.type + " " + self.get_attributes() + ' style="' + self.style.get() + '">'

        # Gets the closing tag of an object as a string
        # returns: string

        def get_tag_close(self):
            return "</" + self.type + ">"

        # Attempts to set the text of an object
        # returns: itself/object

        def set_text(self, _str):
            self.innerText = _str
            return self

        # Sets/overrides the class on the object with
        # the specified value
        # returns: self/object

        def set_class(self, _str):
            self.add_attribute('class="' + _str + '"')
            return self

        def html(self):
            pass

        # Get parent class
        # returns: parent/obj

        def get_parent(self):
            return self.parent

        # Get the highest class in the nested class
        # returns: highest class

        def get_parent_super(self):
            _obj = self
            while _obj.parent:
                _obj = _obj.parent

            return _obj

        def generate_css_id(self, _f):
            if _f not in self.get_tag_open():
                self.add_attribute('id="' + _f + '"')

        # Attempts to link the current object to a higher class
        # returns: Void

        def __link_self(self):
            _obj = self
            _s = self
            while _obj.parent:
                if not hasattr(_obj.parent, "children"):
                    break
                if _s in _obj.parent.children:
                    pass
                else:
                    _obj.parent.children.append(self)

                _obj = _obj.parent

        # Set an onclick function to be called with code (JS)
        # returns: self/object

        def on_click(self, _code):
            self.add_attribute('onClick="' + _code + '"')
            return self

        # Set an on mouse enter to be called with code (JS)
        # returns: self/object

        def on_mouse_enter(self, _code):
            self.add_attribute('onmouseover="' + _code + '"')
            return self

        # Set an onmouseleave function to be called with code (JS)
        # returns: self/object

        def on_mouse_leave(self, _code):
            self.add_attribute('onmouseout="' + _code + '"')
            return self

        # CLASS style object

        class style_obj:

            # INITIALIZE

            def __init__(self, _parent):
                self._style = ""
                self.parent = _parent

            # Gets the style of the object
            # returns: style (str)

            def get(self):
                return self._style

            # Set an object/element's style
            # returns: self/object

            def set(self, _style):
                if type(_style) is list:
                    for l in _style:
                        self.append(l)
                else:
                    self._style = _style

                return self.parent

            def append(self, _style):
                self._style = self._style + _style
                return self.parent

    class table:
        def __init__(self, rows, columns):
            self.objects = []
            self.rows = rows
            self.columns = columns

        def insert_at(self, row, column, obj):
            _s = self
            obj.table_inserted_at = [str(row), str(column)]
            obj.table = self
            self.objects.append(obj)

            return self

        def build_html(self):
            row_index = -1
            column_index = -1

            html_table_open = '<table style="border-collapse: collapse;table-layout: fixed;width:100%;"><tbody ' \
                              'style="width:100%;"> '
            html_table_close = "</tbody></table>"

            html_mid_build = ""

            while row_index < self.rows - 1:
                row_index = row_index + 1
                while column_index < self.columns - 1:
                    column_index = column_index + 1
                    html_mid_build = html_mid_build + "<td>"
                    for o in self.objects:
                        if o.table_inserted_at[0] == str(row_index) and o.table_inserted_at[1] == str(column_index):
                            print(str(o.get_tag_open()) + o.innerText + " -> row " + o.table_inserted_at[0] + " column " +
                                  o.table_inserted_at[1] + " inserted")

                            # INSERT OBJECT HTML INTO TABLE HERE
                            # -----------------------------------
                            html_mid_build = html_mid_build + "" + o.get_tag_open() + o.innerText + o.get_tag_close() + ""
                            # -----------------------------------

                    html_mid_build = html_mid_build + "</td>"
                # <tr><td>"
                # </td></tr>
                html_mid_build = html_mid_build + "</tr>"

                column_index = -1

            if not html_mid_build == "":
                print(html_table_open + html_mid_build + html_table_close)
                return html_table_open + html_mid_build + html_table_close

            return -1

    class bootstrap:
        def __init__(self):
            self._using = False

        def use(self, _bool):
            self._using = _bool

        def using(self):
            return self._using

        def get(self):
            _s = self
            bss = '<!-- CSS only --><link rel="stylesheet" ' \
                  'href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" ' \
                  'integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" ' \
                  'crossorigin="anonymous"><script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" ' \
                  'integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" ' \
                  'crossorigin="anonymous"></script><script ' \
                  'src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" ' \
                  'integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" ' \
                  'crossorigin="anonymous"></script><script ' \
                  'src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" ' \
                  'integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" ' \
                  'crossorigin="anonymous"></script> '
            return bss
