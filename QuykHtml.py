import webbrowser
import os
import time
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
        self.preview = self.new("div")

        # ** PREVIEW HELPER **
        # Preview helper for on_click_show_preview. Shows the element
        # object that was clicked in full screen. Good for images, but
        # can be used with any element created by qhtml.new(type)
        # -------------------------------------------------------------
        self.css.add(".quykHtml_preview", "display:none;padding-top:20%;text-align:center;z-index:100;position:absolute;top:0;width:100%;height:100%;background-color:rgba(255,255,255,0.9);")
        self.preview.set_class("quykHtml_preview").add_attribute('id="quykHtml_preview"')
        # preview display code
        self.scripts.append('function quykHtml_showPreview(el){d = document.getElementById("quykHtml_preview");if(d.style.display == "none" || d.style.display == ""){d.style.display = "inline";d.appendChild(el.cloneNode(true)); d.innerHTML = d.innerHTML + "<p>Press Escape to close</p>";}}')
        # escape key press code
        self.scripts.append('document.onkeydown = function(evt) {evt = evt || window.event;var isEscape = false;if ("key" in evt) {isEscape = (evt.key === "Escape" || evt.key === "Esc");} else {isEscape = (evt.keyCode === 27);}if (isEscape) {d = document.getElementById('
                            '"quykHtml_preview");if(d){if(d.style.display != "none"){d.innerHTML = ""; d.style.display = "none";}}}};')
        # -------------------------------------------------------------

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

        for _obj_element in self.all:
            if _obj_element.ajax_code != "":
                # print("render ajax code detected")
                self.scripts.append(_obj_element.ajax_code)

        if self.bootstrap.using():
            _bootstrap = self.bootstrap.get()

        for _s in self.css.styles:
            _b = _b + "" + _s

        for _sc in self.scripts:
            _scripts = _scripts + "" + _sc + "\n"

        print("inserting " + str(self.preview))
        self.display.insert(self.preview)

        html_string = "<head>" + _bootstrap + "<style>" + _b + '</style><script type="text/javascript">' + _scripts + '</script></head>' + str(
            self.all[0].innerHTML)

        f = open(os.getcwd() + "/render.html", "w")
        f.write(html_string)
        f.close()

        # print(html_string)

        sleep(0.2)

        webbrowser.get(_path).open(str(os.getcwd()) + "/render.html")

        return html_string

    # CLASS Style sheet attached to the html object

    class ss:

        # INITIALIZE CLASS

        def __init__(self):
            self.styles = []
            self.colors = self._colors()
            self.helpers = self._helpers()

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

        class _helpers:
            def __init__(self):
                pass

            def font_size(self, _value=-1):
                _s = self
                if _value == -1:
                    print("css.helpers.font_size(val) error -> value should be structured like: 1px or 1em etc")
                    return False
                else:
                    return "font-size:" + _value + ";"

            def font_color(self, _color=-1):
                _s = self
                if _color == -1:
                    print("css.helpers.font_color(_color) error -> _color should be formatted like: #ffffff or #000000 etc")
                    return False
                else:
                    return "color:" + _color + ";"

            def bgr_color(self, _value=-1):
                _s = self
                if _value == -1:
                    return False
                else:
                    return "background-color:" + _value + ";"

            def shadow(self, _color, _w="5px", _x="5px", _y="5px", _z="5px"):
                _s = self
                return "box-shadow:" + _w + " " + _x + " " + _y + " " + _z + " " + _color + ";"

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
            self.id = -1
            self.attributes = []
            self.attr_check = []
            self.style = self.style_obj(self)
            self.innerHTML = ""
            self.innerText = ""
            self.ajax_code = ""
            self.ajax_pointer = ""
            self.ajax_callback = ""
            self.onclick_showpreview_html = ""

        # Render - attempts to render the full webpage from the object
        # returns: void

        def render(self):
            if self.parent == "":
                pass
            else:
                self.parent.render()

        # Insert a table into an element as pure html
        # returns: itself/html object

        def insert_table_raw(self, table_raw_obj: object, append_html=False):
            if append_html:
                self.innerHTML += table_raw_obj.build_html()
            else:
                self.innerHTML = table_raw_obj.build_html()
            return self

        def insert_table_html(self, table_html: str, append_html=False):
            if append_html:
                self.innerHTML = self.innerHTML + table_html
            else:
                self.innerHTML = table_html
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

            _attr_name = _str[:_str.find("=")]
            _attr_val = _str[_str.find("=") + 1:]

            if _attr_name in self.attr_check:
                self.clear_attribute(_attr_name)

            self.attr_check.append(_attr_name)
            self.attributes.append(_attr_name + "=" + _attr_val)
            return self

        def clear_attribute(self, _attr_name):
            if _attr_name in self.attr_check:
                print("check")
                for _a in self.attributes:
                    if _attr_name in _a:
                        self.attributes.remove(_a)
                        self.attr_check.remove(_attr_name)
                        break
                    else:
                        print("FALSE\n")
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

        def set_text_ipsum(self):
            self.innerText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " \
                             "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum "
            return self

        def set_text_ipsum_small(self):
            self.innerText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
            return self

        def set_text_ipsum_large(self):
            self.innerText = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit " \
                             "aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et " \
                             "dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae " \
                             "consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? "
            return self

        # Sets/overrides the class on the object with
        # the specified value
        # returns: self/object

        def set_class(self, _str):
            self.add_attribute('class="' + str(_str) + '"')
            return self

        def set_id(self, _str):
            self.add_attribute('id="' + str(_str).replace("#", "") + '"')
            self.id = str(_str).replace("#", "")
            return self

        def set_img_src(self, _str):
            self.add_attribute('src="' + _str + '"')
            return self

        def set_name(self, _str):
            self.add_attribute('name="' + _str + '"')
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

        def on_right_click(self, _code, _block_normal_context=True):
            _block = ''

            if _block_normal_context:
                _block = ' return false;'
            else:
                _block = ''

            self.add_attribute('oncontextmenu="' + _code + _block + '"')
            return self

        def on_click_show_preview(self):
            self.on_click("quykHtml_showPreview(this);")
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

        def ajax_get(self, _type=""):
            if self.ajax_code != "":
                if _type == "":
                    return [self.ajax_code, self.ajax_pointer, self.ajax_callback]
                elif _type == "code":
                    return self.ajax_code
                elif _type == "pointer":
                    return self.ajax_pointer
                elif _type == "callback":
                    return self.ajax_callback
            return False

        def ajax_build(self, _type, _str_path, _js_func_name_and_callback_func: list, _async="true"):
            if isinstance(_js_func_name_and_callback_func, list):
                if len(_js_func_name_and_callback_func) == 2:
                    _func_name = _js_func_name_and_callback_func[0]
                    _func_name = _func_name.replace(";", "")
                    _callback_name = _js_func_name_and_callback_func[1]
                    _callback_name = _callback_name.replace(";", "")
                else:
                    print("error in ajax_build_html(...) - > _js_func_name_and_callback_func should be a list with 2 entries [x,y]. \nX being the function for the ajax to be called and Y being the callback function formatted like 'callback_function(r.responseText)'.")
            else:
                print("ajax_build_html(...) _js_callback_func should be a list, the provided was not a list")

            # print(_js_callback_func)

            _r = 'function ' + _func_name + '{var r = new XMLHttpRequest();'
            _r = _r + 'r.onreadystatechange = function () {'
            _r = _r + 'if (r.readyState != 4 || r.status != 200) {'
            _r = _r + '    ' + _callback_name + ";"
            _r = _r + '} else {'
            _r = _r + '    ' + _callback_name + ";"
            _r = _r + '  }'
            _r = _r + '};'
            _r = _r + 'r.open("' + _type + '", "' + _str_path + '", ' + _async + ');'
            _r = _r + 'r.send();}'

            self.ajax_code = _r
            self.ajax_pointer = _func_name + ";"
            self.ajax_callback = _callback_name

            return self

            # print("ajax code - > " + _r)

            # return _func_name + ";"

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
        def __init__(self, rows_or_file_path, columns_or_styling_dict=-1):
            self.__qhtml = qhtml()
            self.time_start = int(round(time.time() * 1000))
            self.td_styles = []

            if type(rows_or_file_path) != int:
                _styling = columns_or_styling_dict
                if _styling != -1 and type(_styling) is dict:
                    print("Styling passed - > " + str(_styling))

                _file = rows_or_file_path
                if os.path.isfile(_file):
                    # IF THE FILE PASSED IN IS A CSV TYPE
                    if os.path.splitext(_file)[1] == ".csv":
                        _f_open = open(_file, "r")
                        _file_contents = _f_open.read()
                        _f_open.close()
                        _file_contents = _file_contents.split("\n")
                        _columns = _file_contents[1].count(",")

                        if _columns > 1:
                            _columns = _columns + 1

                        _rows = len(_file_contents)

                        print("Create a table with " + str(_columns) + " col and " + str(_rows) + " rows")

                if _rows and _columns:
                    self.rows = _rows
                    self.columns = _columns

                    _row_items = _file_contents
                    _table = self.__qhtml.table(_rows, _columns)

                    _curr_row = -1
                    _curr_col = -1

                    for _ri in _row_items:
                        _curr_row = _curr_row + 1
                        _column_item = _ri.split(",")
                        for _ci in _column_item:
                            _curr_col = _curr_col + 1
                            _p = self.__qhtml.new("p").set_text(_ci)
                            if type(_styling) is dict:
                                if _p.type in _styling:
                                    # here
                                    _styling_value = _styling[_p.type]
                                    _values_dict = _styling[_p.type]
                                    _calls = _values_dict["calls"]
                                    _styling_value = _styling_value["style"]
                                    _p.style.set(_styling_value)

                                    for __call in _calls:
                                        print("call - > " + str(__call))
                                        # call method
                                        __call_m = __call[0]
                                        # call arg ( may need to add support for multiple args )
                                        __call_a = __call[1]

                                        _func = getattr(_p, __call_m)
                                        if _func:
                                            _val = _func(__call_a)
                                            print("call - > " + str(__call) + "\n return - >  " + str(_val))

                            _table.insert_at(_curr_row, _curr_col, _p)
                        _curr_col = -1

                    self.get = _table

                else:
                    self.rows = 0
                    self.columns = 0
                    self.time = "Error"
                    self.error = -1

            else:
                self.objects = []
                self.rows = rows_or_file_path
                self.columns = columns_or_styling_dict
                self.time = 0

        def insert_at(self, row, column, obj):
            _s = self

            if type(obj) is list:
                for li in obj:
                    li.table_inserted_at = [str(row), str(column)]
                    li.table = self
                    self.objects.append(li)
            else:
                obj.table_inserted_at = [str(row), str(column)]
                obj.table = self
                self.objects.append(obj)

            return self

        def style_td_at(self, row, col, style):
            _s = self
            print("\nSTYLING AT " + str(row) + " - " + str(col) + '\n')
            # _s.td_styles
            _s.td_styles.append({
                "style": style,
                "row": row,
                "column": col
            })
            for _style in _s.td_styles:
                print(str(_style))

            return self

        def build_into(self, _obj: object, append_html=False):
            if not isinstance(_obj, qhtml.new_obj):
                print("BUILD " + str(self) + " - obj = " + str(_obj) + " - " + str(type(_obj)))
                print("Error building table -> table.build(_qhtml_object_element) -> argument should be a qhtml.new(type) object.")
                return False

            _obj.insert_table_html(self.build_html(), append_html)
            return _obj

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
                    _td_styling = self.td_styles
                    _td_styling_set = ""
                    for _style in _td_styling:
                        if row_index == _style["row"] and column_index == _style["column"]:
                            _td_styling_set = '<td style="' + _style['style'] + '">'
                            break

                    if _td_styling_set != "":
                        html_mid_build = html_mid_build + _td_styling_set
                    else:
                        html_mid_build = html_mid_build + "<td>"

                    for o in self.objects:
                        if o.table_inserted_at[0] == str(row_index) and o.table_inserted_at[1] == str(column_index):

                            # INSERT OBJECT HTML INTO TABLE HERE
                            # -----------------------------------
                            if o.innerText not in o.innerHTML:
                                html_mid_build += o.get_tag_open() + o.innerText + o.innerHTML + o.get_tag_close() + ""
                            else:
                                html_mid_build += o.get_tag_open() + o.innerHTML + o.get_tag_close() + ""
                            # -----------------------------------

                    html_mid_build += "</td>"

                html_mid_build += "</tr>"

                column_index = -1

            if not html_mid_build == "":
                # print(html_table_open + html_mid_build + html_table_close)
                self.time = int(round(time.time() * 1000)) - self.time_start
                print("\n\n** Table built in " + str(self.time) + " MS with " + str(self.columns) + " columns and " + str(self.rows) + " rows  ** \n\n")
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
