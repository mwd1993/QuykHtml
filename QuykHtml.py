import webbrowser
import os
import time
import random
from time import sleep
import copy
import platform
import subprocess
import pickle

print("\nQuykHtml is currently using pickle to load and save templates.\nBe aware of templates you are loading, see their warnings on it.\nhttps://docs.python.org/3/library/pickle.html\n")


class qhtml:

    # Initialize class
    def __init__(self):

        # Variables
        # -------------------------------------
        self.all = []
        self.scripts = []
        self.scripts_on_page_load = []
        self.head = []
        self.css = self._css()
        self.display = self.new("div")
        self.bootstrap = self.bootstrap()
        self.preview = self.new("div")
        self.last = None
        # why do i have to do this self self
        self.templates = self._templates(self)
        self.seo = self.__seo(self)

    # Returns a new q_element object
    # returns: Object

    def new(self, _type):
        _split = _type.split(" ")
        _obj = ""
        if len(_split) > 1:
            _first = _split[0]
            _second = _split[1]
            if "button" in _first or "input" in _first:
                if _second == "br":
                    _container = self._q_element("div")
                    _br = self._q_element("br")
                    _obj = self._q_element(_first)
                    _container.insert([_obj, _br])
                    _obj.parent = self
                    self.last = _obj
                    self.all.append(_container)
                    self.all.append(_br)
                    self.all.append(_obj)
                    return _container
                else:
                    return False
            else:
                return False
        else:
            _obj = self._q_element(_type)
            _obj.parent = self
            self.all.append(_obj)
            self.last = _obj
            return _obj

    # Duplicates an element
    # returns: new duped element

    def dupe(self, qhtml_obj):
        if isinstance(qhtml_obj, self._q_element):
            new = copy.copy(qhtml_obj)
            self.all.append(new)
            return new
        else:
            print('q_element instance is not valid or was not provided.')
            return False

    # Attempts to render the constructed webpage
    # returns: HTML

    def render(self, output_file="render.html", only_html=False, set_clip_board=False):
        if "." not in output_file:
            output_file = output_file + ".html"
        _css = ""
        _scripts = ""
        _scripts_on_page_load = ""
        _head_append = ""
        _bootstrap = ""
        _path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        _preview_scripts_loaded = False
        for _obj_element in self.all:
            if _obj_element.has_preview() and _preview_scripts_loaded is False:
                self.__get_preview_scripts()
                _preview_scripts_loaded = True

            if _obj_element.ajax_code != "":
                self.scripts.append(_obj_element.ajax_code)

            if len(_obj_element.scripts_on_page_load) > 0:
                for __scr in _obj_element.scripts_on_page_load:
                    _scripts_on_page_load += __scr

            if len(_obj_element.scripts) > 0:
                _build = ""
                for _scr in _obj_element.scripts:
                    _build += _scr

                self.scripts.append(_build)

        if self.bootstrap.using():
            _bootstrap = self.bootstrap.get()

        for _s in self.css.styles:
            _css = _css + "" + _s

        for _sc in self.scripts:
            _scripts = _scripts + "" + _sc + "\n"

        for h in self.head:
            _head_append += h + "\n"

        if _preview_scripts_loaded:
            self.display.insert(self.preview)

        if _scripts_on_page_load != "":
            _scripts_on_page_load = ' window.addEventListener("load", on_page_load_init); function on_page_load_init() {' + _scripts_on_page_load + '}'

        if _scripts != "" or _scripts_on_page_load != "":
            _scripts = '<script type="text/javascript">' + _scripts + '' + _scripts_on_page_load + '</script>'

        html_string = "<head>" + _head_append + _bootstrap + "<style>" + _css + '</style>' + _scripts + '</head>' + str(self.all[0].innerHTML)

        f = open(os.getcwd() + "/" + output_file, "w")
        f.write(html_string)
        f.close()
        sleep(0.2)

        if not only_html:
            webbrowser.get(_path).open(str(os.getcwd()) + "/" + output_file)

        if set_clip_board:
            self.clip_put(html_string)

        return html_string

    # Attempts to put a string to the users clipboard
    # returns: void

    def clip_put(self, _str):
        s = self
        copy_keyword = ""
        if platform.system() == 'Darwin':
            copy_keyword = 'pbcopy'
        elif platform.system() == 'Windows':
            copy_keyword = 'clip'
        else:
            print('Could not copy to clipboard for some reason.')
            return False
        subprocess.run(copy_keyword, universal_newlines=True, input=_str)

    # Easily read a file. Returns the file's contents as a string
    # returns: file-contents/boolean

    def file_read(self, file_name, file_path='', to_list=False):
        s = self
        if file_name:
            if file_path:
                dir_path = file_path
            else:
                dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
            f = open(dir_path + file_name, 'r')
            read = f.read()
            f.close()
            if to_list:
                read = read.split('\n')
            return read
        return False

    def __get_preview_scripts(self):
        # ** PREVIEW HELPER **
        # -------------------------------------------------------------
        # Preview helper for on_click_show_preview. Shows the element
        # object that was clicked in full screen. Good for images, but
        # can be used with any element created by qhtml.new(type)
        # -------------------------------------------------------------
        self.css.add(".quykHtml_preview", "display:none;padding-top:60px;text-align:center;z-index:100;position:fixed;top:0;width:100%;height:100%;background-color:rgba(255,255,255,0.9);")
        self.preview.set_class("quykHtml_preview").add_attribute('id="quykHtml_preview"')

        # preview display code
        self.scripts.append(
            'function quykHtml_showPreview(el){'
            'd = document.getElementById("quykHtml_preview");'
            'if(d.style.display == "none" || d.style.display == ""){'
            'd.style.display = "inline";'
            'var node = el.cloneNode(true);'
            'node.className = "strat-img-no-hover";'
            'if(node.tagName.toLowerCase() == "img"){'
            'node.style.height = "640px";'
            'node.style.width = "800px";'
            '}'
            'd.appendChild(node);'
            'd.innerHTML = d.innerHTML + "<p style=\'font-weight:bold;font-size:20px;\'>Press Escape to close or click <span onclick=\'quykHtml_preview_close();\' style=\'cursor:pointer;color:green;font-size:24px;\'>here</span></p>";'
            '}'
            '}'
        )
        # preview display escape key press code
        self.scripts.append(
            'document.onkeydown = function(evt) {'
            'evt = evt || window.event;'
            'var isEscape = false;'
            'if ("key" in evt) {'
            'isEscape = (evt.key === "Escape" || evt.key === "Esc");'
            '} else {'
            'isEscape = (evt.keyCode === 27);'
            '}'
            'if(isEscape){'
            'd = document.getElementById("quykHtml_preview");'
            'if(d){'
            'if(d.style.display != "none"){'
            'd.innerHTML = "";'
            'd.style.display = "none";'
            '}'
            '}}};'
        )
        # preview display click here escape option for mobile
        self.scripts.append(
            'function quykHtml_preview_close(){'
            'd = document.getElementById("quykHtml_preview");'
            'if(d){'
            'if(d.style.display != "none"){'
            'd.innerHTML = "";'
            'd.style.display = "none";'
            '}'
            '}'
            '}'
        )
        # -------------------------------------------------------------

        return True

    # CLASS Style sheet attached to the html object

    class _css:

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

                self.WHITE = "#FFFFFF"
                self.BLACK = "#000000"

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

            def rgbtohex(self, rgb):
                _s = self
                '''Takes an RGB tuple or list and returns a hex RGB string.'''
                return f'#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}'

            def hextorgb(self, _hex):
                _s = self
                _hex = _hex.lstrip('#')
                return tuple(int(_hex[i:i + 2], 16) for i in (0, 2, 4))

    # CLASS _q_element, an element object type

    class _q_element:

        # INITIALIZE CLASS

        def __init__(self, _type, _parent=0):
            self.type = _type
            self.children = []
            if _parent != 0:
                self.parent = _parent
            else:
                self.parent = ""
            self.scripts = []
            self.scripts_on_page_load = []
            self.id = -1
            self.attributes = []
            self.attr_check = []
            self.style = self.style_obj(self)
            self.innerHTML = ""
            self.innerText = ""
            self.ajax_code = ""
            self.ajax_pointer = ""
            self.ajax_callback = ""
            self._onclick_showpreview_html = False

        # Render - attempts to render the full webpage from the object
        # returns: void

        def render(self, output_file="render.html", only_html=False, set_clip_board=False):
            if self.parent == "":
                return False
            else:
                if set_clip_board:
                    self.parent.render(output_file, only_html, set_clip_board)
                else:
                    if only_html:
                        self.parent.render(output_file, only_html=True)
                    else:
                        self.parent.render(output_file)

        # Adds javascript code to the main page/display
        # returns: self

        def scripts_add(self, js_code, on_page_load=False):
            if on_page_load:
                self.scripts_on_page_load.append(js_code)
            else:
                self.scripts.append(js_code)
            return self

        # Insert a table into an element as pure html
        # returns: itself/html object

        def insert_table_raw(self, table_raw_obj: object, append_html=False):
            if append_html:
                self.innerHTML += table_raw_obj.__build_html()
            else:
                self.innerHTML = table_raw_obj.__build_html()
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
            if len(_str) < 4:
                print('QuykHtml add_attribute error, no value defined!\n- > ' + _str)
                return self
            _attr_name = _str[:_str.find("=")]
            _attr_val = _str[_str.find("=") + 1:]

            if _attr_name in self.attr_check:
                self.clear_attribute(_attr_name)

            self.attr_check.append(_attr_name)
            self.attributes.append(_attr_name + "=" + _attr_val)
            return self

        # Attempts to clear an attribute from an element
        # returns: self

        def clear_attribute(self, _attr_name):
            if _attr_name in self.attr_check:
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
            first = "<" + self.type + " " + self.get_attributes()
            if self.style.get():
                second = ' style="' + self.style.get() + '">'
            else:
                second = ">"
            return first + second

        # Gets the closing tag of an object as a string
        # returns: string

        def get_tag_close(self):
            return "</" + self.type + ">"

        # Sets a code block to display code
        # returns: self

        def set_text_code_block(self, _str, text_color=False, parentheses_color=False, main_text_color=False, background_color=False):

            if self.type != 'pre':
                print('set_text_code_block type error. Should be used on a "pre" type.\nYou used it on a ' + self.type)
                return False

            replace = {
                ':': '<span style="color:gray;">:</span>',
                '(': '<span style="color:orange;">(<span style="color:yellow;">',
                ')': '</span>)</span>',
            }

            if text_color and parentheses_color:
                replace['('] = '<span style="color:' + parentheses_color + ';">(<span style="color:' + text_color + ';">'
            elif text_color:
                replace['('] = '<span style="color:orange;">(<span style="color:' + text_color + ';">'
            elif parentheses_color:
                replace['('] = '<span style="color:' + parentheses_color + ';">(<span style="color:yellow;">'

            for k in replace:
                v = replace[k]
                if k in _str:
                    _str = _str.replace(k, v)

            if not background_color:
                background_color = 'gray'

            if not main_text_color:
                main_text_color = 'white'

            self.innerText = '<p style="margin:0px;padding:6px;color:' + main_text_color + ';background-color:' + background_color + ';">' + _str + '</p>'

            return self

        # Attempts to set the text of an object
        # returns: itself/object

        def set_text(self, _str):
            self.innerText = _str
            return self

        # Attempts to set a MEDIUM sized text block used as a place holder
        # returns: self

        def set_text_ipsum(self):
            self.innerText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " \
                             "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum "
            return self

        # Attempts to set a SMALL sized text block used as a place holder
        # returns: self

        def set_text_ipsum_small(self):
            self.innerText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
            return self

        # Attempts to set a LARGE sized text block used as a place holder
        # returns: self

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

        # Sets an elements id
        # returns: self

        def set_id(self, _str):
            self.add_attribute('id="' + str(_str).replace("#", "") + '"')
            self.id = str(_str).replace("#", "")
            return self

        # Sets an images source (external url or local url)
        # returns: self

        def set_img_src(self, _str):
            self.add_attribute('src="' + _str + '"')
            return self

        # Sets an images alt text
        # returns: self

        def set_img_alt(self, _str):
            if self.type != 'img':
                print('q_element.set_img_alt ERROR.\nset_img_alt should be used on an img type, it was used on a ' + self.type)
            if _str:
                self.add_attribute('alt="' + _str + '"')

        # Sets an image placeholder. You can specify
        # a size by providing an int.
        # Shout out to via.placeholder.com
        # returns: self

        def set_img_placeholder(self, place_holder_size=150):
            if self.type != 'img':
                print('q_element.set_img_placeholder ERROR.\nShould be used on img type, you used it on ' + self.type)
                return False
            self.set_img_src('https://via.placeholder.com/' + str(place_holder_size))
            return self

        # Sets an elements name attribute
        # returns: self

        def set_name(self, _str):
            self.add_attribute('name="' + _str + '"')
            return self

        # Attempts to set an elements value
        # returns: self

        def set_value(self, _str):
            self.add_attribute('value="' + _str + '"')
            return self

        # Sets an elements tooltip (on mouse hover -> text shows near cursor)
        # returns: self

        def set_tool_tip(self, _str):
            self.add_attribute('title="' + _str + '"')
            return self

        # Sets the element and all of it's children's html into the users' clipboard
        # returns: self

        def set_clip_board(self):
            self.parent.clip_put(self.html())
            return self

        # On click, go to specified url. no_https=True will allow for external domain linking.
        # returns: self

        def on_click_goto(self, url_to_nav_to, new_tab=True, no_https=False):
            if no_https is False:
                if new_tab:
                    self.on_click("window.open('https://" + url_to_nav_to + "');")
                else:
                    self.on_click("window.location.href='https://" + url_to_nav_to + "';")
            else:
                if new_tab:
                    self.on_click("window.open('" + url_to_nav_to + "');")
                else:
                    self.on_click("window.location.href='" + url_to_nav_to + "';")
            return self

        # Sets a form elements form options
        # action="upload.php" method="post" enctype="multipart/form-data"
        # returns: self

        def set_form_options(self, action_php_call, method_get_or_post, enctype="multipart/form-data"):
            method = method_get_or_post
            action = action_php_call
            if self.type != "form":
                print('set_form_options error -> ' + self.type + ' is not a form element')
                return self

            if action and method:
                self.add_attribute('action="' + action + '" method="' + method + '" enctype="' + enctype + '"')
                return self
            else:
                print('set_form_options error -> ' + self.type + ' is missing either action or method argument')
                return self
            return self

        # Makes the submit button inside of a specified URL element a form button
        # which will submit the form
        # returns: self

        def set_form_button(self):
            self.add_attribute('value="submit"')
            return self

        # Sets an iframe element options
        # returns: self

        def set_iframe(self, src_url, title="iframe"):
            if self.type != "iframe":
                print("Cannot set iframe data on type " + self.type)
                return self

            self.add_attribute('src="' + src_url + '" title="' + title + '"')
            return self

        # Makes element (input) auto complete text or not
        # returns: self

        def set_auto_complete(self, _boolean: bool):
            if not _boolean:
                self.add_attribute('autocomplete="off"')
            else:
                self.add_attribute('autocomplete="on"')

            return self

        # Gets all of the html of an element (and innerHtml)
        # returns: self

        def html(self, set_clip_board=False):
            html = self.get_tag_open() + self.innerText + self.innerHTML + self.get_tag_close()
            if set_clip_board:
                self.parent.clip_put(html)
            return html

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

        def on_click(self, _code, _block_normal_context=True):
            if _block_normal_context:
                self.add_attribute('onClick="' + _code + ' return false;"')
            else:
                self.add_attribute('onClick="' + _code + '"')
            return self

        # On right click, run specified code
        # returns: self

        def on_right_click(self, _code, _block_normal_context=True):
            _block = ''

            if _block_normal_context:
                _block = ' return false;'
            else:
                _block = ''

            self.add_attribute('oncontextmenu="' + _code + _block + '"')
            return self

        # Upon element clicked, shows a preview full-screen'd image of the element
        # This can be used for any element, but makes most sense for images
        # returns: self

        def on_click_show_preview(self):
            self._onclick_showpreview_html = True
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

        # Gets ajax data if any and retuns a list
        # of data if no specified type is passed
        # returns: data/boolean

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

        # Attempts to build an ajax request. randomize_call_for.. is used
        # to get the most recent data from the request by providing
        # a piece of raw js code that appends a random number to the call request
        # returns: self

        def ajax_build(self, _type, _str_path, js_callback_func="", _async="true", randomize_call_for_fresh_data=False):
            _ran = []
            for i in range(5):
                _ran.append(str(random.randint(0, 9)))

            _ran = ''.join(_ran)

            if js_callback_func:
                _func_name = "_ajax_handler_" + str(_ran) + "()"
                _func_name = _func_name.replace(";", "")
                _callback_name = js_callback_func
                _callback_name = _callback_name.replace(";", "")

                if "(" not in _callback_name:
                    _callback_name = _callback_name + "(r.responseText)"
            else:
                print("ajax_build FAILED:\nPlease provide a Javascript function name and a Javascript callback method to handle the response text.\nAs js_func_name and js_callback_func")
                return self

            _r = 'function ' + _func_name + '{var r = new XMLHttpRequest();'
            _r = _r + 'r.onreadystatechange = function () {'
            _r = _r + 'if (r.readyState == 4 && r.status == 200) {'
            _r = _r + '    ' + _callback_name + ";"
            _r = _r + '} else {'
            _r = _r + '     var a = "";'
            _r = _r + '  }'
            _r = _r + '};'

            if randomize_call_for_fresh_data:
                _r = _r + 'r.open("' + _type + '", "' + _str_path + '?ran=" + Math.random().toString().slice(2),' + _async + ');'
            else:
                _r = _r + 'r.open("' + _type + '", "' + _str_path + '", ' + _async + ');'
            _r = _r + 'r.send();}'

            self.ajax_code = _r
            self.ajax_pointer = _func_name + ";"
            self.ajax_callback = _callback_name

            return self

        # Returns true if the element has an on click preview
        # returns: self

        def has_preview(self):
            return self._onclick_showpreview_html

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

            # Appends inline styling to an elements style class
            # returns: style.parent (element)

            def append(self, _style):
                self._style = self._style + _style
                return self.parent

            # Helper to align an element
            # returns: style.parent (element)

            def align(self, left_center_right="center"):
                self.append('text-align:' + left_center_right + ';')
                # self._style = self._style + 'text-align:' + left_center_right + ';'
                return self.parent

            # Background color helper
            # returns: style.parent (element)

            def bg_color(self, color='white'):
                self.append('background-color:' + color + ';')
                # self._style = self._style + 'background-color:' + color + ';'
                return self.parent

            # Float helper for an element
            # returns: style.parent (element)

            def float(self, left_or_right="left"):
                self.append('text-align:' + left_or_right + ';')
                # self._style = self._style + 'text-align:' + left_or_right + ';'
                return self.parent

            # Font size helper method
            # returns: style.parent (element)

            def font_size(self, size="18px"):
                self.append('font-size:' + size + ';')
                # self._style = self._style + 'font-size:' + size + ';'
                return self.parent

            # Font color helper method
            # returns: style.parent (element)

            def font_color(self, color='black'):
                self.append('color:' + color + ';')
                # self._style += 'color:' + color + ';'
                return self.parent

            # Height helper method
            # returns: style.parent (element)

            def height(self, height):
                self.append('height:' + height + ';')
                # self._style += 'height:' + height + ';'
                return self.parent

            # Width helper method
            # returns: style.parent (element)

            def width(self, width):
                self.append('width:' + width + ';')
                # self._style += 'width:' + width + ';'
                return self.parent

            # Hide helper method
            # returns: style.parent (element)

            def hide(self, none_or_hidden='none'):
                self.append('display:' + none_or_hidden + ';')
                # self._style += 'display:' + none_or_hidden + ';'
                return self.parent

    class table:
        def __init__(self, rows_or_file_path, columns_or_styling_dict=-1):
            self.__qhtml = qhtml()
            self.time_start = int(round(time.time() * 1000))
            self.td_styles = []
            self.td_classes = []
            self.td_ids = []
            self.objects = []

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
                                    if "calls" in _values_dict:
                                        _calls = _values_dict["calls"]
                                    else:
                                        _calls = []

                                    if "style" in _styling_value:
                                        _styling_value = _styling_value["style"]
                                        _p.style.set(_styling_value)
                                    else:
                                        _styling_value = []

                                    for __call in _calls:
                                        # print("call - > " + str(__call))
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
                    self.objects = []

            else:
                self.objects = []
                self.rows = rows_or_file_path
                self.columns = columns_or_styling_dict
                self.time = 0

        # Insert an element object into *row* and *column* using 0 based index
        # returns: self

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

        # Set the table td id at *row* and *column* using 0 based index
        # returns: self

        def set_td_id_at(self, row, col, _id):
            _s = self
            _s.td_ids.append({
                "id": _id,
                "row": row,
                "column": col
            })
            for _c in _s.td_ids:
                print(str(_c))

            return self

        # Set the table td class at *row* and *column* using 0 based index
        # returns: self

        def set_td_class_at(self, row, col, _class):
            _s = self
            _s.td_classes.append({
                "class": _class,
                "row": row,
                "column": col
            })
            for _c in _s.td_classes:
                print(str(_c))

            return self

        # Set the table td style at *row* and *column* using 0 based index
        # returns: self

        def style_td_at(self, row, col, style):
            _s = self
            _s.td_styles.append({
                "style": style,
                "row": row,
                "column": col
            })
            for _style in _s.td_styles:
                print(str(_style))

            return self

        # Attempts to build the table and then insert it into a div
        # returns: div (table inside)

        def build(self, append_html=False):
            """Builds the table object into a div object and returns that div."""
            q = self.__qhtml
            div = q.new("div")
            self.__build_into(div, append_html)
            return div

        def __build_into(self, _obj: object, append_html=False):
            if not isinstance(_obj, qhtml._q_element):
                print("BUILD " + str(self) + " - obj = " + str(_obj) + " - " + str(type(_obj)))
                print("Error building table -> table.build(_qhtml_object_element) -> argument should be a qhtml.new(type) object.")
                return False

            _obj.insert_table_html(self.__build_html(), append_html)
            return _obj

        def __build_html(self):
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
                            _class_val = ""
                            _id_val = ""
                            for _c in self.td_classes:
                                if row_index == _c["row"] and column_index == _c["column"]:
                                    _class_val = _c['class']
                                    break

                            for _ids in self.td_ids:
                                if row_index == _ids["row"] and column_index == _ids["column"]:
                                    _id_val = _ids['id']
                                    break

                            if _id_val:
                                _td_id_set = 'id="' + _id_val + '" '
                            else:
                                _td_id_set = ' '

                            if _class_val:
                                _td_styling_set = '<td ' + _td_id_set + 'style="' + _style['style'] + '" class="' + _class_val + '">'
                            else:
                                _td_styling_set = '<td ' + _td_id_set + 'style="' + _style['style'] + '">'
                            break

                    if len(_td_styling) <= 0:

                        for _c in self.td_classes:
                            if row_index == _c["row"] and column_index == _c["column"]:
                                _class_val = _c['class']
                                _td_styling_set = '<td class="' + _class_val + '"</td>'
                                break

                    if _td_styling_set != "":
                        html_mid_build = html_mid_build + _td_styling_set
                    else:
                        html_mid_build = html_mid_build + "<td>"

                    _td_id_set = ""
                    try:
                        ob = self.objects
                        if len(self.objects) == 0:
                            ob = self.get.objects
                        for o in ob:
                            if o.table_inserted_at[0] == str(row_index) and o.table_inserted_at[1] == str(column_index):

                                # INSERT OBJECT HTML INTO TABLE HERE
                                # -----------------------------------
                                if o.innerText not in o.innerHTML:
                                    html_mid_build += o.get_tag_open() + o.innerText + o.innerHTML + o.get_tag_close() + ""
                                else:
                                    html_mid_build += o.get_tag_open() + o.innerHTML + o.get_tag_close() + ""
                                # -----------------------------------
                    except Exception as e:
                        print(e)

                    html_mid_build += "</td>"

                html_mid_build += "</tr>"

                column_index = -1

            if not html_mid_build == "":
                self.time = int(round(time.time() * 1000)) - self.time_start
                print("\n** Table built in " + str(self.time) + " MS with " + str(self.columns) + " columns and " + str(self.rows) + " rows  ** \n")
                return html_table_open + html_mid_build + html_table_close

            return -1

    class bootstrap:
        def __init__(self):
            self._using = False

        # Set using bootstrap true or false
        # returns: void

        def use(self, _bool):
            self._using = _bool

        # Returns true if using bootstrap
        # returns: Boolean

        def using(self):
            return self._using

        # Get the bootstrap raw code
        # returns: string (bootstrap code)
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

    # TODO convert from pickle to no required library
    #   dir(obj) and obj.__dict__ are helpers
    class _templates:
        def __init__(self, qhtml_instance):
            self.parent = qhtml_instance
            self.__path = os.getcwd() + '/Templates/'
            self.__path2 = 'Templates/'

        def __space_to_underscore(self, _str, vice_versa=False):
            s = self
            if vice_versa:
                return _str.replace('_', ' ')
            else:
                return _str.replace(' ', '_')

            return False

        # Saves the template (list of quykhtml elements) to a pickle object
        # returns: boolean

        def save(self, template_name: str, qhtml_obj_list: list):
            s = self
            if template_name:
                template_name = self.__space_to_underscore(template_name)
                index = -1
                p = self.__path + template_name + '/'
                if not os.path.isdir(p):
                    os.mkdir(p)
                for el in qhtml_obj_list:
                    index += 1
                    if not os.path.isfile(self.__path2 + template_name + '/' + template_name + '_' + str(index) + '.pickle'):
                        open('templates/' + template_name + '/' + template_name + '_' + str(index) + '.pickle', 'w').close()
                    pickle.dump(el, file=open('templates/' + template_name + '/' + template_name + '_' + str(index) + '.pickle', 'wb'))
                    print('Pickle saving - > ' + str(el))

            return True

        # Attempts to load the FOLDER containing all or one pickle object
        # returns: list (of quykhtml elements)

        def load(self, template_name):
            s = self
            if template_name:
                template_name = self.__space_to_underscore(template_name)
                p = self.__path + template_name + '/'
                p2 = self.__path2 + template_name + '/'
                _templates = []
                if os.path.isdir(p):
                    index = -1
                    for file in os.listdir(p):
                        index += 1
                        qhtml_obj = pickle.load(file=open(p2 + file, 'rb'))
                        _templates.append(qhtml_obj)

                if len(_templates) > 0:
                    print('Pickles Loaded - > ' + str(_templates))
                    return _templates

            return False

    class __seo:
        def __init__(self, qhtml_parent):
            self.__title = ""
            self.__description = ""
            self.parent = qhtml_parent  # type: qhtml

        def display_all_seo(self):
            print(str(len(self.parent.head)) + ' SEO Head Tags - > ' + str(self.parent.head))
            return self.parent.head

        def set_page_title(self, _str):
            if _str:
                self.parent.head.append('<title>' + _str + '<title>')

        def set_page_description(self, _str):
            if _str:
                self.parent.head.append('<meta name="description" content="' + _str + '">')

        def set_page_keywords(self, _str):
            if _str:
                self.parent.head.append('<meta name="keywords" content="' + _str + '">')

        def set_page_author(self, _str):
            if _str:
                self.parent.head.append('<meta name="author" content="' + _str + '">')

        def set_page_viewport(self, _str):
            if _str:
                self.parent.head.append('<meta name="author" content="' + _str + '">')

        def set_page_auto_refresh(self, seconds: int):
            if seconds:
                self.parent.head.append('<meta http-equiv="refresh" content="' + str(seconds) + '">')

        def set_page_robots(self, _str):
            allowed = ['noindex', 'nofollow', 'index', 'follow']
            passed = False
            for a in allowed:
                if a in _str:
                    passed = True
            if _str:
                if passed:
                    self.parent.head.append('<meta name="robots" content="' + _str + '">')
                else:
                    print('seo.set_page_robots ERROR.\nThese are the allowed strings to be passed: ' + str(allowed))

        def set_page_encoding(self, encoding='UTF-8'):
            if encoding:
                self.parent.head.append('<meta charset="' + encoding + '">')

        def set_page_subject(self, _str):
            if _str:
                self.parent.head.append('<meta name="subject" content="' + _str + '">')

        def set_page_classification(self, _str):
            if _str:
                self.parent.head.append('<meta name="Classification" content="' + _str + '">')

        def set_page_designer(self, _str):
            if _str:
                self.parent.head.append('<meta name="designer" content="' + _str + '">')

        def set_page_copyright(self, _str):
            if _str:
                self.parent.head.append('<meta name="copyright" content="' + _str + '">')

        def set_page_category(self, _str):
            if _str:
                self.parent.head.append('<meta name="category" content="' + _str + '">')
