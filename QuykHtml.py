import webbrowser
import os
import time
import random
from time import sleep
import copy
import platform
import subprocess


class qhtml:

    """
    Main qhtml class
    """
    def __init__(self):

        # Variables
        # -------------------------------------
        self.all = []
        self.scripts = []
        self.scripts_on_page_load = []
        self.head = []
        self.css = self._css()
        self.display = self.new("div").style.append('background-color:transparent;')
        self.bootstrap = self.bootstrap()
        self.preview = self.new("div")
        self.last = None  # type: qhtml._q_element
        self.seo = self.__seo(self)
        self._animation_scripts = False
        self.themes = self._themes(self)
        self.__body_background = ''

    def new(self, _type):
        """
        Returns a new q_element object
        div, pre, p, a, img, iframe, etc
        """
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
                    return _container  # type: qhtml._q_element
                else:
                    return False
            else:
                return False
        else:
            _obj = self._q_element(_type)
            _obj.parent = self
            self.all.append(_obj)
            self.last = _obj
            return _obj  # type: qhtml._q_element

    def dupe(self, q_element):
        """
        Dupes an element:\n
        p = q.new('p').set_text('hi')\n
        p_dupe = q.dupe(p).style.set('background-color:gray;')\n
        """
        if isinstance(q_element, self._q_element):
            new = copy.deepcopy(q_element)
            new.parent = self
            self.all.append(new)
            return new
        else:
            print('q_element instance is not valid or was not provided.')
            return False

    def prettify_html(self, html):
        return html

    def render(self, output_file="render.html", only_html=False, set_clip_board=False, prettify_html=True):
        """
        Renders a file, returns the html generated
        """

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

            # noinspection PyProtectedMember
            if _obj_element._ajax_code != "":
                # noinspection PyProtectedMember
                self.scripts.append(_obj_element._ajax_code)

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

        if _scripts != "" or _scripts_on_page_load != "" or self._animation_scripts:
            _anim_scripts = ""
            if self._animation_scripts:
                _anim_scripts = self.__get_anim_scripts()

            _scripts = '<script type="text/javascript">' + _scripts + '' + _scripts_on_page_load + _anim_scripts + '</script>'

        if self.__body_background:
            print('body background - >\n' + self.__body_background)

        html_string = "<head>" + _head_append + _bootstrap + "<style>" + _css + '</style>' + _scripts + '</head><body' + self.__body_background + '>' + str(self.display.html()) + '</body>'

        f = open(os.getcwd() + "/" + output_file, "w")
        f.write(html_string)
        f.close()
        sleep(0.2)

        if prettify_html:
            html_string = self.prettify_html(html_string)

        if not only_html:
            webbrowser.get(_path).open(str(os.getcwd()) + "/" + output_file)

        if set_clip_board:
            self.clip_put(html_string)

        return html_string

    def clip_put(self, _str):
        """
        Attempts to put a string to your clipboard
        """
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
        """
        Easily read a file. Returns the file's contents as a string
        """
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

    def set_body_background(self, _src, _transparency_strength=0.15):
        """Set the body background image for the page.\n
        Transparency Range (0,1) | 1 = full transparency
        """
        self.__body_background = ' style="background: linear-gradient(rgba(255,255,255,' + str(_transparency_strength) + '), rgba(255,255,255,' + str(_transparency_strength) + ')),'
        self.__body_background += 'url(\'' + _src + '\');background-attachment:fixed;background-repeat:no-repeat;background-position:center;background-size: cover;"'
        return self

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

    def __get_anim_scripts(self):
        # '       els[i].classList.add("fade-in-now");' \
        # '       els[i].classList.remove("fade-in");' \
        _anim_scripts = 'window.onscroll = function(e){' \
                        'var els = document.getElementsByTagName("*");' \
                        'for(var i=0; i<els.length; i++) {' \
                        '   if(isScrolledIntoView(els[i]) && els[i].id.includes("fade-in")) {' \
                        '       if(els[i].id.includes("-now") == false)' \
                        '           els[i].id = els[i].id + "-now";' \
                        '   }' \
                        '} \n' \
                        'var elss = document.getElementsByTagName("*");' \
                        'for(i=0; i<elss.length; i++) {' \
                        '   if(isScrolledIntoView(elss[i]) && window.jQuery.hasData(elss[i])) {' \
                        '       var _data = e.currentTarget.window.jQuery.data(elss[i]);' \
                        '       var _anim = _data["animation"];' \
                        '       var _anim_length = JSON.stringify(_data["animation_length"]);' \
                        '       $("#" + elss[i].id).animate(_anim,_anim_length,function(){});' \
                        '       elss[i].classList.add("slide-in-horiz-now");' \
                        '       elss[i].classList.remove("slide-in-horiz");' \
                        '   }' \
                        '} \n' \
                        '}\n'

        # alert("invalid el for scroll");
        _anim_scripts += 'function isScrolledIntoView(el) {' \
                         'if(!el){ return false;}' \
                         'var rect = el.getBoundingClientRect();' \
                         'var elemTop = rect.top;' \
                         'var elemBottom = rect.bottom;' \
                         'var isVisible = (elemTop >= 0) && (elemBottom <= window.innerHeight);' \
                         'var _new = parseInt(elemTop) + parseInt(document.body.scrollTop);' \
                         'return isVisible;' \
                         '}\n'

        return _anim_scripts

    class _themes:
        """Themes class which contains theme objects.\n
        print(q.themes.basic.about())
        """

        def __init__(self, parent=''):
            if parent:
                self.parent = parent

            theme_info = {
                'name': 'basic',
                'description': 'A basic theme with: Green buttons, Gray Text and white backgrounds.',
                'css': [
                    [
                        'button',
                        'color:white;font-size:24px;background-color:#6dad7a;padding:16px;padding-top:5px;'
                        'padding-bottom:5px;border:solid 1px black;border-radius:6px;margin-top:20px;margin-bottom:20px;'
                    ],
                    [
                        'button:hover',
                        'background-color:#7ecc8e;'
                    ],
                    [
                        'p',
                        'font-size:18px;font-weight:bold;margin-top:12px;margin-bottom:12px;color:#454a46;'
                    ],
                    [
                        'input',
                        'font-size:18px;font-weight:bold;padding:6px;border-radius:2px;border: 1px solid black;'
                    ]
                ]
            }

            self.basic = self._theme_object(theme_info['css'], theme_info['name'], theme_info['description'])

            theme_info['name'] = 'greens'
            theme_info['description'] = 'A green theme with: Green buttons, White Text and Green Divs and a White backgrounds.'
            theme_info['css'] = [
                [
                    'button',
                    'color:white;font-size:24px;background-color:#739e7e;padding-top:5px;'
                    'padding-bottom:5px;border:solid 1px black;border-radius:6px;margin-top:20px;margin-bottom:20px;'
                    'padding:16px;padding-top:5px;padding-bottom:5px;'
                ],
                [
                    'button:hover',
                    'background-color:#84b591;'

                ],
                [
                    'p',
                    'font-size:18px;font-weight:bold;margin-top:12px;margin-bottom:12px;color:#454a46;'
                    'color:white;'
                ],
                [
                    'div',
                    'background-color:#597560;'
                ],
                ['.dark-green-text', 'color:#27362b;']
            ]

            self.greens = self._theme_object(theme_info['css'], theme_info['name'], theme_info['description'])

            theme_info['name'] = 'blues'
            theme_info['description'] = 'A Blue theme with: Blue buttons, Gray Text and Blue Divs and a Light Gray background.'
            theme_info['css'] = [
                [
                    'button',
                    'color:white;font-size:24px;background-color:#5987a8;padding:16px;padding-top:5px;'
                    'padding-bottom:5px;border:solid 1px black;border-radius:6px;margin-top:20px;margin-bottom:20px;'
                ],
                [
                    'button:hover',
                    'background-color:#699dc2;'
                ],
                [
                    'div',
                    'background-color:#426b8a;color:white;'
                ],
                [
                    'body',
                    'background-color:#a9bdcc;'
                ],
                [
                    'p',
                    'font-size:18px;font-weight:bold;margin-top:12px;margin-bottom:12px;'
                    'color:#265373;'
                ],
            ]

            self.blues = self._theme_object(theme_info['css'], theme_info['name'], theme_info['description'])

            theme_info['name'] = 'night'
            theme_info['description'] = 'A Night-Mode theme where everything is mostly dark.'
            theme_info['css'] = [
            ]

        class _theme_object:
            def __init__(self, css, name, about):
                self.css = css
                self.__name = name
                self.__about = about

            def about(self):
                """Get the description of a theme and available classes you can use\n
                print(q.themes.basic.about())
                """
                _avail_classes = []
                for ee in self.css:
                    _ind = 0
                    for e in ee:
                        if _ind == 1:
                            _ind = 0
                            break
                        _ind += 1

                        if e[:1] == ".":
                            _avail_classes.append(e)
                _append = ""
                if len(_avail_classes) > 0:
                    _append = ' '.join(_avail_classes)
                else:
                    _append = 'None'
                return '***** Theme \'' + self.__name + '\' ***** \n' + self.__about + '\nClasses Available For Use:\n\t\t' + _append + ''

            def __repr__(self):
                print(self.about())
                return 'Usage: q.css.add(q.themes.' + str(self.__name).lower() + ')\n'

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
            """
            Add a style to an object element
            q.css.add( [\n\t['p','font-size:64px;], ['div','background-color:gray;'] \n] )\n
            or\n
            q.css.add('p','font-size:64px;')\n
            q.css.add('div','background-color:gray;')
            """
            # noinspection PyProtectedMember
            if type(name) is qhtml._themes._theme_object:
                name = name.css

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

        def export(self, _file):
            """
            Export every style into an external style sheet in the program's directory
            """
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
        """
        An 'element' which allows us to simulate a web element
        """

        # INITIALIZE CLASS

        def __init__(self, _type, _parent=0):

            self.type = _type
            self.children = []
            self.animations = self.__animations(self)
            if _parent != 0:
                self.parent = _parent
            else:
                self.parent = ""
            self.scripts = []
            self.scripts_on_page_load = []
            self.id = -1
            self.attributes = []
            self._attr_check = []
            self.style = self._style_obj(self)
            self.innerHTML = ""
            self.innerText = ""
            self._ajax_code = ""
            self._ajax_pointer = ""
            self._ajax_callback = ""
            self._onclick_showpreview_html = False

        def render(self, output_file="render.html", only_html=False, set_clip_board=False, prettify_html=True):
            """
            Attempts to render the full webpage from the object
            """
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

        def scripts_add(self, js_code, on_page_load=False):
            """
            Adds javascript code to the main page/display
            """
            if on_page_load:
                self.scripts_on_page_load.append(js_code)
            else:
                self.scripts.append(js_code)
            return self

        def insert_table_raw(self, table_raw_obj: object, append_html=False):
            """
            Insert a table into an element as pure html
            returns: itself/html object
            """
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

        def insert(self, _obj):
            """
            Insert an object into another object
            IE: insert a p object inside of a div object
            returns: itself/html object
            """
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

        def add_attribute(self, _str, append=False):
            """
            Adds an attribute to an element
            returns: self/object
            """
            if len(_str) < 4:
                print('QuykHtml add_attribute error, no value defined!\n- > ' + _str)
                return self
            _attr_name = _str[:_str.find("=")]
            _attr_val = _str[_str.find("=") + 1:]

            # TODO - allow for appending of different attribute types.
            # TODO For now, it only works with class attribute type
            if append is False:
                if _attr_name in self._attr_check:
                    self.clear_attribute(_attr_name)

                self._attr_check.append(_attr_name)
                self.attributes.append(_attr_name + "=" + _attr_val)
            else:
                # TODO For now, it only works with class attribute type
                _index = -1
                _found = False
                for attr in self.attributes:
                    _index += 1
                    if "class=" in attr:
                        self.attributes[_index] = attr[:-1] + " " + _attr_val.replace('"', "") + '"'
                        _found = True

                if _found is False:
                    self._attr_check.append(_attr_name)
                    self.attributes.append(_attr_name + "=" + _attr_val)
            return self

        def clear_attribute(self, _attr_name):
            """
            Attempts to clear an attribute from an element
            returns: self
            """
            if _attr_name in self._attr_check:
                for _a in self.attributes:
                    if _attr_name in _a:
                        self.attributes.remove(_a)
                        self._attr_check.remove(_attr_name)
                        break
                    else:
                        print("FALSE\n")
            return self

        def get_attributes(self):
            """
            Retrieves all attributes from an object
            returns: html attributes (str)
            """
            _b = ""
            for s in self.attributes:
                _b = _b + " " + s
            return _b.strip()

        def get_attribute(self, _attr: str):
            if _attr:
                for s in self.attributes:
                    if _attr.lower() in s:
                        return s

            return False

        def get_tag_open(self):
            """
            Get the full tag of an object as a string
            returns: string
            """
            first = "<" + self.type + " " + self.get_attributes()
            if self.style.get():
                second = ' style="' + self.style.get() + '">'
            else:
                second = ">"
            return first + second

        def get_tag_close(self):
            """
            Gets the closing tag of an object as a string
            returns: string
            """
            return "</" + self.type + ">"

        def set_text_code_block(self, _str, text_color=False, parentheses_color=False, main_text_color=False, background_color=False):
            """
            Sets a code block to display code
            returns: self
            """
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

        def set_text(self, _str):
            """
            Attempts to set the text of an object
            returns: itself/object
            """
            self.innerText = _str
            return self

        def set_text_ipsum(self):
            """
            Attempts to set a MEDIUM sized text block used as a place holder
            returns: self
            """
            self.innerText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " \
                             "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum "
            return self

        def set_text_ipsum_small(self):
            """
            Attempts to set a SMALL sized text block used as a place holder
            returns: self
            """
            self.innerText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
            return self

        def set_text_ipsum_large(self):
            """
            Attempts to set a LARGE sized text block used as a place holder
            returns: self
            """
            self.innerText = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit " \
                             "aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et " \
                             "dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae " \
                             "consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? "
            return self

        def set_class(self, _str, append=False):
            """
            Sets/overrides the class on the object with
            the specified value
            returns: self/object
            """
            self.add_attribute('class="' + str(_str) + '"', append=append)
            return self

        def set_id(self, _str):
            """
            Sets an elements id
            returns: self
            """
            self.add_attribute('id="' + str(_str).replace("#", "") + '"')
            self.id = str(_str).replace("#", "")
            return self

        def set_img_src(self, _str):
            """
            Sets an images source (external url or local url)
            returns: self
            """
            self.add_attribute('src="' + _str + '"')
            return self

        def set_img_background(self, _source, _transparency_strength=0.2):
            """
            Sets an images background
            """
            _str = 'background: linear-gradient(rgba(255,255,255,' + str(_transparency_strength) + '), rgba(255,255,255,' + str(_transparency_strength) + ')), '
            _str += 'url(\'' + _source + '\');background-attachment:fixed;background-repeat:no-repeat;background-position:center;background-size: cover;'
            self.style.append(_str)
            return self

        def set_img_alt(self, _str):
            """
            Sets an images alt text
            returns: self
            """
            if self.type != 'img':
                print('q_element.set_img_alt ERROR.\nset_img_alt should be used on an img type, it was used on a ' + self.type)
            if _str:
                self.add_attribute('alt="' + _str + '"')

            return self

        def set_img_placeholder(self, place_holder_size=150):
            """
            Sets an image placeholder. You can specify
            a size by providing an int.
            Shout out to via.placeholder.com\n
            returns: self
            """
            if self.type != 'img':
                print('q_element.set_img_placeholder ERROR.\nShould be used on img type, you used it on ' + self.type)
                return False
            self.set_img_src('https://via.placeholder.com/' + str(place_holder_size))
            return self

        def set_name(self, _str):
            """
            Sets an elements name attribute\n
            returns: self
            """
            self.add_attribute('name="' + _str + '"')
            return self

        def set_value(self, _str):
            """
            Attempts to set an elements value\n
            returns: self
            """
            self.add_attribute('value="' + _str + '"')
            return self

        def set_tool_tip(self, _str):
            """
            Sets an elements tooltip (on mouse hover -> text shows near cursor)\n
            returns: self
            """
            self.add_attribute('title="' + _str + '"')
            return self

        def set_clip_board(self):
            """
            Sets the element and all of it's children's html into the users' clipboard\n
            returns: self
            """
            self.parent.clip_put(self.html())
            return self

        def on_click_goto(self, url_to_nav_to, new_tab=True, no_https=False):
            """
            On click, go to specified url. no_https=True will allow for external domain linking.\n
            returns: self
            """
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

        def set_form_options(self, action_php_call, method_get_or_post, enctype="multipart/form-data"):
            """
            Sets a form elements form options\n
            action="upload.php" method="post" enctype="multipart/form-data"\n
            returns: self
            """
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

        def set_form_button(self):
            """
            Makes the submit button inside of a specified URL element a form button
            which will submit the form
            returns: self
            """
            self.add_attribute('value="submit"')
            return self

        def set_iframe(self, src_url, title="iframe"):
            """
            Sets an iframe element options
            returns: self

            """
            if self.type != "iframe":
                print("Cannot set iframe data on type " + self.type)
                return self

            self.add_attribute('src="' + src_url + '" title="' + title + '"')
            return self

        def set_auto_complete(self, _boolean: bool):
            """
            Makes element (input) auto complete text or not
            returns: self
            """
            if not _boolean:
                self.add_attribute('autocomplete="off"')
            else:
                self.add_attribute('autocomplete="on"')

            return self

        def html(self, set_clip_board=False):
            """
            Gets all of the html of an element (and innerHtml)
            returns: self
            """
            html = self.get_tag_open() + self.innerText + self.innerHTML + self.get_tag_close()
            if set_clip_board:
                self.parent.clip_put(html)
            return html

        def get_parent(self):
            """
            Get parent class
            returns: parent/obj
            """
            return self.parent

        def get_parent_super(self):
            """
            Get the highest class in the nested class
            returns: highest class
            """
            _obj = self
            while _obj.parent:
                _obj = _obj.parent

            return _obj

        def generate_css_id(self, _f):
            if _f not in self.get_tag_open():
                self.add_attribute('id="' + _f + '"')

        def __link_self(self):
            """
            Attempts to link the current object to a higher class
            returns: Void
            """
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

        def on_click(self, _code, _block_normal_context=True):
            """
            Set an onclick function to be called with code (JS)
            returns: self/object
            """
            if _block_normal_context:
                self.add_attribute('onClick="' + _code + ' return false;"')
            else:
                self.add_attribute('onClick="' + _code + '"')
            return self

        def on_right_click(self, _code, _block_normal_context=True):
            """
            On right click, run specified code
            returns: self
            """
            _block = ''
            if _block_normal_context:
                _block = ' return false;'
            else:
                _block = ''
            self.add_attribute('oncontextmenu="' + _code + _block + '"')
            return self

        def on_click_show_preview(self):
            """
            Upon element clicked, shows a preview full-screen'd image of the element
            This can be used for any element, but makes most sense for images
            returns: self
            """
            self._onclick_showpreview_html = True
            self.on_click("quykHtml_showPreview(this);")
            return self

        def on_mouse_enter(self, _code):
            """
            Set an on mouse enter to be called with code (JS)
            returns: self/object
            """
            self.add_attribute('onmouseover="' + _code + '"')
            return self

        def on_mouse_leave(self, _code):
            """
            Set an onmouseleave function to be called with code (JS)
            returns: self/object
            """
            self.add_attribute('onmouseout="' + _code + '"')
            return self

        def on_mouse_scroll(self, _code):
            """
            Sets an onmousescroll function to be called with code (JS)
            """
            self.add_attribute('onscroll="' + _code + '"')
            return self

        def ajax_get(self, _type=""):
            """
            Gets ajax data if any and retuns a list
            of data if no specified type is passed
            returns: data/boolean
            """
            if self._ajax_code != "":
                if _type == "":
                    return [self._ajax_code, self._ajax_pointer, self._ajax_callback]
                elif _type == "code":
                    return self._ajax_code
                elif _type == "pointer":
                    return self._ajax_pointer
                elif _type == "callback":
                    return self._ajax_callback
            return False

        def ajax_build(self, _type, _str_path, js_callback_func="", _async="true", randomize_call_for_fresh_data=False):
            """
            Attempts to build an ajax request. randomize_call_for.. is used\n
            to get the most recent data from the request by providing\n
            a piece of raw js code that appends a random number to the call request\n
            returns: self
            """
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

            self._ajax_code = _r
            self._ajax_pointer = _func_name + ";"
            self._ajax_callback = _callback_name

            return self

        def has_preview(self):
            """
            Returns true if the element has an on click preview
            returns: self
            """
            return self._onclick_showpreview_html

        class _style_obj:
            """
            Style class instantiated in the main QHTML class
            """

            def __init__(self, _parent):
                self._style = ""
                self.parent = _parent  # type: qhtml._q_element

            def get(self):
                """
                Gets the style of the object
                :return: str
                """
                return self._style

            def set(self, _style):
                """
                Set an object/element's style\n
                returns: self/object
                :param _style: str
                :return: self
                """
                if type(_style) is list:
                    for l in _style:
                        self.append(l)
                else:
                    self._style = _style

                return self.parent

            def append(self, _style):
                """
                Appends inline styling to an elements style class
                :param _style:
                :return:
                """
                self._style = self._style + _style
                return self.parent

            def align(self, left_center_right="center"):
                """
                Helper to align an element
                :param left_center_right:
                :return: q_element object
                """
                self.append('text-align:' + left_center_right + ';')
                # self._style = self._style + 'text-align:' + left_center_right + ';'
                return self.parent

            def bg_color(self, color='white'):
                """
                Background color helper
                :param color: str
                :return: q_element object
                """
                self.append('background-color:' + color + ';')
                # self._style = self._style + 'background-color:' + color + ';'
                return self.parent

            def float(self, left_or_right="left"):
                """
                Float helper for an element
                :param left_or_right: str
                :return: q_element object
                """
                self.append('text-align:' + left_or_right + ';')
                return self.parent

            def font_size(self, size="18px"):
                """
                Font size helper method
                :param size: str
                :return: q_element object
                """
                if 'px' not in size:
                    size = size + 'px'
                self.append('font-size:' + size + ';')
                return self.parent

            def font_color(self, color='black'):
                """
                Font color helper method
                :param color: str
                :return: q_element object
                """
                self.append('color:' + color + ';')
                return self.parent

            def height(self, height):
                """
                Height helper method
                :param height: str
                :return: q_element object
                """
                self.append('height:' + height + ';')
                return self.parent

            def width(self, width):
                """
                Width helper method
                :param width:
                :return: q_element object
                """
                self.append('width:' + width + ';')
                return self.parent

            # Hide helper method
            # returns: style.parent (element)

            def hide(self, none_or_hidden='none'):
                """
                Hide an element, helper method
                :param none_or_hidden: str
                :return: q_element object
                """
                self.append('display:' + none_or_hidden + ';')
                return self.parent

        class __animations:
            """
            Animations for an element\n
            Sliding and Fade In are supported at the moment
            """
            __fade_in_loaded = False

            def __init__(self, q_element):
                self.parent = q_element  # type: qhtml._q_element
                self._total_anims = 0

            def on_inview_fade_in(self, fade_in_speed=4.0):
                """
                When the element is in view, fade in
                :param fade_in_speed: seconds (float)
                :return: q_element object
                """
                self._total_anims += 1
                element = self.parent
                _qhtml = element.parent  # type: qhtml
                if _qhtml._animation_scripts is False:
                    _qhtml._animation_scripts = True

                if str(element.id) == "-1":

                    def get_ran_id():
                        n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
                        _rn = ""
                        for i in range(8):
                            _rn += str(n[random.randint(0, 9)])

                        _id = 'fade-in-' + str(_rn)
                        return _id

                    element.set_id(get_ran_id())
                    print('No element ID, generating one for fade in functionality: ' + element.id)

                _qhtml.css.add('#' + element.id, 'opacity:5%;transition:opacity 0.8s;')
                _qhtml.css.add('#' + element.id + '-now', 'opacity:100%;transition:opacity ' + str(fade_in_speed) + 's;')
                _anim_script_onLoad = 'var el = document.getElementById("' + element.id + '");' \
                                                                                          '   if(isScrolledIntoView(el)) {' \
                                                                                          '   el.id = "' + element.id + '-now";' \
                                                                                                                        '}'
                element.scripts_add(_anim_script_onLoad, on_page_load=True)
                return element

            def on_inview_slide_in(self, slide_to='50%', x_or_y='x', _from='left', duration=2000.0, force_position="left:-100%;"):
                """
                When the element is in view, slide in\n
                Allows slide in from left or right, element will then use
                Absolute positioning\n
                :param slide_to: position (50%, 400px, etc)
                :param x_or_y: slide horizontal (vertical slide not supported yet)
                :param _from: left or right
                :param duration: Amount of time until the element reaches the set position
                :param force_position: Force the initial position of the element (ie: left:-100%; or left:-200px;, etc)
                :return: q_element object
                """
                self._total_anims += 1
                _from = _from.lower()
                element = self.parent  # type: qhtml._q_element
                _qhtml = element.parent  # type: qhtml
                element.style.append('position:absolute;')
                element.set_class('slide-in-horiz', append=True)

                if _qhtml._animation_scripts is False:
                    if _qhtml.bootstrap.using() is False:
                        _qhtml.bootstrap.use(True)
                        print('Animations require bootstrap. It has been auto loaded for you.')
                    print('Horizontal Slide (warning): Forces an element to use absolute positioning!')
                    _qhtml._animation_scripts = True
                    _qhtml.display.style.append('overflow-x:hidden;')
                    _jq = ('var _style = $(document.body).attr("style");'
                           '_style += "overflow-x:hidden;width:100%;";'
                           'setTimeout(function(){$(document.body).scrollLeft(0);},0.001);')
                    element.scripts_add(_jq, on_page_load=True)

                if x_or_y == 'x':
                    def get_ran_id():
                        n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
                        _rn = ""
                        for i in range(8):
                            _rn += str(n[random.randint(0, 9)])

                        _id = 'slide-in-' + str(_rn)
                        return _id

                    _anim_str = ""
                    if _from == 'left':
                        _anim_str = 'left:"' + slide_to + '"'
                        element.style.append(force_position)
                        if element.id == -1:
                            _id_get = get_ran_id()
                            element.set_id(_id_get)

                    elif _from == 'right':
                        force_position = 'left:100%;'
                        element.style.append(force_position)
                        if element.id == -1:
                            _id_get = get_ran_id()
                            element.set_id(_id_get)
                        _anim_str = 'left:"' + slide_to + '"'

                    _anim_data = {
                        _from.replace('right', 'left'): slide_to
                    }
                    _jquery = (
                            '$(document).ready(function(){'
                            'if(isScrolledIntoView(el=document.getElementById("' + str(element.id) + '"))){'
                                                                                                     'el.classList.add("slide-in-horiz-now");'
                                                                                                     'el.classList.remove("slide-in-horiz");'
                                                                                                     '$("#' + str(element.id) + '").animate({'
                                                                                                                                '' + _anim_str + ''
                                                                                                                                                 '}, ' + str(duration) + ', function(){'
                                                                                                                                                                         '  '
                                                                                                                                                                         '});'
                                                                                                                                                                         '}});'
                    )
                    _jquery += 'var _el = document.getElementById("' + str(element.id) + '");'
                    _jquery += 'window.jQuery.data(_el,"animation",' + str(_anim_data) + ');'
                    _jquery += 'window.jQuery.data(_el,"animation_length","' + str(duration) + '");'
                    # print(_jquery)
                    element.scripts_add(_jquery, on_page_load=True)
                    return element

    class table:
        """
        Create a raw table or use a .csv file and generate a table\n
        table = q.table(1,2) # raw table of 1 row and 2 columns
        table.insert_at(0,0,q.new('p').set_text('row 1 column 1')\n
        table.insert_at(0,1,q.new('p').set_text('row 1 column 2')\n
        table = table.build()\n
        Or from a .csv:\n
        table = q.table('my_csv_file',{'p':'font-size:26px;'}).build()
        """

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
            """
            Insert an element object into *row* and *column* using 0 based index\n
            insert_at(0, 0, q.new('p').set_text('QuykHtml Rocks!')
            """
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

        def set_td_id_at(self, row, col, _id):
            """
            Set the table td id at *row* and *column* using 0 based index\n
            set_td_id_at(0, 0, 'some_id')\n
            Set the ID of the td element at row 1 column 1
            """
            _s = self
            _s.td_ids.append({
                "id": _id,
                "row": row,
                "column": col
            })
            for _c in _s.td_ids:
                print(str(_c))

            return self

        def set_td_class_at(self, row, col, _class):
            """
            Set the table td class at *row* and *column* using 0 based index\n
            set_td_class_at(0, 0, 'some_class')\n
            Set the class of the td element at row 1 column 1
            """
            _s = self
            _s.td_classes.append({
                "class": _class,
                "row": row,
                "column": col
            })
            for _c in _s.td_classes:
                print(str(_c))

            return self

        def style_td_at(self, row, col, style):
            """
            Set the table td style at *row* and *column* using 0 based index\n
            style_td_at(0, 0, 'font-size:42px;background-color:green;')\n
            Set the styling of the td element at row 1 column 1
            """
            _s = self
            _s.td_styles.append({
                "style": style,
                "row": row,
                "column": col
            })
            for _style in _s.td_styles:
                print(str(_style))

            return self

        def build(self, append_html=False):
            """
            Builds the table object into a div object and returns that div.\n
            correct usage:\n
            t = q.table(1,1)\n
            t = t.build()\n
            incorrect usage:\n
            t = q.table(1,1)\n
            t.build()\n
            """
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
        """
        Bootstrap loader
        """

        def __init__(self):
            self._using = False

        def use(self, _bool):
            """
            Set using bootstrap true or false
            :param _bool:
            :return: None
            """
            self._using = _bool

        def using(self):
            """
            Returns true if using bootstrap
            :return: boolean
            """
            return self._using

        # Get the bootstrap raw code
        # returns: string (bootstrap code)
        def get(self):
            """
            Get the bootstrap raw code
            :return: string
            """
            _s = self
            bss = '<!-- CSS only --><link rel="stylesheet" ' \
                  'href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" ' \
                  'integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" ' \
                  'crossorigin="anonymous"><script src="https://code.jquery.com/jquery-3.5.1.js" ' \
                  'integrity="sha256-QWo7LDvxbWT2tbbQ97B53yJnYU3WhH/C8ycbRAkjPDc=" ' \
                  'crossorigin="anonymous"></script><script ' \
                  'src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" ' \
                  'integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" ' \
                  'crossorigin="anonymous"></script><script ' \
                  'src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" ' \
                  'integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" ' \
                  'crossorigin="anonymous"></script> '
            return bss

    class __seo:
        """
        Class to manage SEO Data.\n
        You can see some various help links which\n
        explain what SEO is and how to use it:\n
        q.seo.help_links()
        """

        def __init__(self, qhtml_parent):
            self.__title = ""
            self.__description = ""
            self.parent = qhtml_parent  # type: qhtml

        def help_links(self):
            """
            Help links which print to the console, which allows users to learn what seo is
            :return: list
            """
            links = [
                'http://static.googleusercontent.com/media/www.google.com/en/us/webmasters/docs/search-engine-optimization-starter-guide.pdf',
                'https://github.com/joshbuchea/HEAD'
            ]
            print('QuykHtml - Links on what SEO is and how to use them (shoutout to the authors):')
            for li in links:
                print(li)

            return links

        def display_all_seo(self):
            """
            Displays all seo user has defined, if any
            :return: html head string value
            """
            print(str(len(self.parent.head)) + ' SEO Head Tags - > ' + str(self.parent.head))
            return self.parent.head

        def set_page_title(self, _str):
            """
            Set the SEO page title
            :param _str: Title
            :return: none
            """
            if _str:
                self.parent.head.append('<title>' + _str + '</title>')

        def set_page_description(self, _str):
            """
            Set the SEO page description
            :param _str: description
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="description" content="' + _str + '">')

        def set_page_keywords(self, _str):
            """
            Set the SEO page keywords (think google search keywords)
            :param _str: key words
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="keywords" content="' + _str + '">')

        def set_page_author(self, _str):
            """
            Set the SEO page author
            :param _str: author string
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="author" content="' + _str + '">')

        def set_page_viewport(self, _str):
            """
            Set the SEP page view port (desktop, mobile, etc)
            :param _str: view port string content
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="viewport" content="' + _str + '">')

        def set_page_auto_refresh(self, seconds: int):
            """
            Set the SEO, page to auto refresh every 'seconds'
            :param seconds: int
            :return: none
            """
            if seconds:
                self.parent.head.append('<meta http-equiv="refresh" content="' + str(seconds) + '">')

        def set_page_robots(self, _str):
            """
            Set SEO page robots, allowed keywords:\n
            noindex\n
            nofollow\n
            index\n
            follow\n
            :param _str: str
            :return: none
            """
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
            """
            Set the SEO page encoding, default value is UTF-8
            :param encoding: encoding type (str)
            :return: none
            """
            if encoding:
                self.parent.head.append('<meta charset="' + encoding + '">')

        def set_page_subject(self, _str):
            """
            Set the SEO page subject
            :param _str: Subject (str)
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="subject" content="' + _str + '">')

        def set_page_classification(self, _str):
            """
            Set the SEO classification of the page
            :param _str: classification details (str)
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="Classification" content="' + _str + '">')

        def set_page_designer(self, _str):
            """
            Set the SEO page designer
            :param _str: Designer (str)
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="designer" content="' + _str + '">')

        def set_page_copyright(self, _str):
            """
            Set SEO page copyright
            :param _str: str
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="copyright" content="' + _str + '">')

        def set_page_category(self, _str):
            """
            Set the page category
            :param _str: str
            :return: none
            """
            if _str:
                self.parent.head.append('<meta name="category" content="' + _str + '">')

        def export(self, file_path='seo_export.txt'):
            """
            Export all of the SEO out to a file
            :param file_path: 'path/to/file.txt' (str)
            :return: none
            """
            if len(self.parent.head) > 0:
                qf = QuykFile(file_path, force_create=True)
                if qf.success:
                    qf.write(self.parent.head)
            else:
                print('no len')


class QuykFile:
    """
    QuykFile Class:\n
    Allows easy file manipulation:\n
    \n
    qf = QuykFile('path/to/file.txt')\n
    if qf:
    \t  qf.write('QuykFile!')\n
    \t  read = qf.read()\n
    \t  read_list = qf.read(as_list=True)\n
    \t  qf.rename('file_renamed.txt')\n
    \t  print(str(qf.file_data))

    """

    def __init__(self, path, as_full_dir=False, force_create=False):
        self.success = False
        self.file_data = {
            'full': '',
            'path': '',
            'name': ''
        }

        if force_create:
            if as_full_dir:
                full_path = path
            else:
                full_path = os.getcwd() + '/' + path

            if os.path.isfile(full_path):
                _path, _file = os.path.split(full_path)
                if _path:
                    self.file_data['path'] = _path
                else:
                    self.file_data['path'] = _path
                self.file_data['name'] = _file
                self.file_data['full'] = full_path
                self.success = True
            else:
                _path, _file = os.path.split(full_path)
                self.file_data['path'] = _path
                self.file_data['name'] = _file
                self.file_data['full'] = path
                if _path:
                    if os.path.isdir(_path) is False:
                        os.mkdir(_path)

                if os.path.isfile(full_path) is False:
                    f = open(full_path, 'w+')
                    f.close()
                    while os.path.isfile(full_path) is False:
                        time.sleep(1.5)

                if os.path.isfile(full_path):
                    self.success = True

            if self.success is False:
                print('QuykFile - Error could not create a valid object for ( Dir Creation Failed ) :\n' + full_path)
        else:
            _reason = ""
            if as_full_dir:
                full_path = path
            else:
                full_path = os.getcwd() + '/' + path

            if os.path.isfile(full_path):
                _path, _file = os.path.split(full_path)
                if _path:
                    self.file_data['path'] = _path
                else:
                    self.file_data['path'] = _path
                self.file_data['name'] = _file
                self.file_data['full'] = full_path
                self.success = True
            else:
                self.success = False
                _reason = "( No Such File )"

            if self.success is False:
                print('QuykFile - Error could not create a valid object ' + _reason + ':\n' + full_path)

    def read(self, as_list=False):
        if self.success:
            f = open(self.file_data['full'])
            r = f.read()
            f.close()
            if as_list:
                r = r.split('\n')
            return r

    def write(self, text):
        if self.success:
            _type = str(type(text))
            if 'str' in _type:
                f = open(self.file_data['full'], 'w')
                f.write(text)
                f.close()
            elif 'list' in _type:
                f = open(self.file_data['full'], 'w')
                t = '\n'.join(text)
                f.write(t)
                f.close()

    def append(self, text, as_new_line=True, before=False):
        if self.success:
            _type = str(type(text))
            if 'str' in _type:
                f = open(self.file_data['full'], 'a')
                if as_new_line:
                    text = '\n' + text
                f.write(text)
                f.close()
            elif 'list' in _type:
                f = open(self.file_data['full'], 'a')
                _text = '\n'.join(text)

                if as_new_line:
                    text = '\n' + _text
                else:
                    text = _text

                f.write(text)
                f.close()

    def insert(self, text, line_index: int):
        if self.success:
            _type = str(type(text))
            if 'str' in _type:
                rl = self.read(as_list=True)
                rl.insert(line_index, text)
                f = open(self.file_data['full'], 'w')
                t = '\n'.join(rl)
                f.write(t)
                f.close()

            elif 'list' in _type:
                pass

    def copy_to(self, path, as_full_dir=False):
        if self.success:
            c = self.read()
            if c:
                if as_full_dir is False:
                    path = os.getcwd() + '/' + path

                _path, _file = os.path.split(path)
                if os.path.isdir(_path):
                    f = open(path, 'w+')
                    f.write(c)
                    f.close()
                    return True

        return False

    def rename(self, name):
        if self.success:
            if self.copy_to(name):
                os.remove(self.file_data['full'])
                n_replace = self.file_data['name']
                self.file_data['full'] = self.file_data['full'].replace(n_replace, name)
                self.file_data['name'] = name
                print(str(self.file_data))
                return True
        return False

    def delete(self):
        if self.success:
            os.remove(self.file_data['full'])
            self.file_data = {}
            self.success = False
