import webbrowser
import os
from time import sleep


class qhtml:

    def __init__(self):
        self.all = []
        self.styleSheet = self.ss()
        self.tables = self.table_helper(self)
        self.scripts = []

        self.css = {
            "head": [
                "background-color:#8a85ed;",
                "font-size:24px;",
                "font-weight:bold;",
                "height:400px;"
            ],

            "body": [
                "font-size:24px;",
                "height:600px;",
                "text-align:center"
            ],

            "foot": [
                "height:40px;",
                "font-size:20px;",
                "color:white;",
                "background-color:#8a85ed;"
            ],

            "p": [
                "font-weight:bold;",
                "color:gray;"
            ],

            "space-top": [
                "padding-top:60px;"
            ]
        }

    def new(self, _type):
        _obj = self.new_obj(_type)
        self.all.append(_obj)
        return _obj

    def render(self):
        _b = ""
        _scripts = ""
        for _s in self.styleSheet.styles:
            _b = _b + "" + _s

        for _sc in self.scripts:
            _scripts = _scripts + "" + _sc +"\n"
        f = open(os.getcwd() + "/render.html", "w")
        f.write("<head><style>" + _b + '</style><script type="text/javascript">' + _scripts + '</script></head>' + str(self.all[0].innerHTML))
        f.close()
        print("<head><style>" + _b + '</style><script type="text/javascript">' + _scripts + '</script>' + "</head>" + str(self.all[0].innerHTML))
        sleep(0.2)
        webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(
            str(os.getcwd()) + "/render.html")

        return "<head><style>" + _b + "</style></head>" + str(self.all[0].innerHTML)

    def generate_skeleton(self):
        _self = self
        _str = "from QuykHtml import qhtml\n\n"
        _str += 'q = qhtml()\n\ncontainer = q.new("div")\n\n'
        _str += 'head = q.new("div").style.set(q.css["head"])\n\nhead_text = q.new("p").set_text("Header Text")\n\n\n'
        _str += 'body = q.new("div").style.set(q.css["body"])\n\nbody_text = q.new("p").set_text("Body Text")\n\n\n'
        _str += 'foot = q.new("div").style.set(q.css["foot"])\n\nfoot_text = q.new("p").set_text("Footer Text")\n\n\n'
        _str += '_p = q.new("p").set_text("Table Text 1")\n'
        _str += '__p = q.new("p").set_text("Table Text 2")\n'
        _str += '_p2 = q.new("p").set_text("Table Text 3")\n\n\n'

        _str += 'table_objs = [{"value": _p, "row": "1", "column": "1"},{"value": __p, "row": "1", "column": "1"},{"value": _p2, "row": "1", "column": "1"},{"value": _p2, "row": "1", "column": "2"}]\ntable = q.tables.new(2, 1, table_objs)\ntable.style.set("width:100%;")'
        _str += '\n\nhead.insert(head_text)\nbody.insert(body_text).insert(table)\nfoot.insert(foot_text)\n\ncontainer.insert([head, body, foot])\nq.render()'

        f = open("skeleton.py", "w")
        f.write(_str)
        f.close()

        return _str

    class ss:
        def __init__(self):
            self.styles = []

        def add(self, name, style):
            self.styles.append(name + "{" + style + "}")
            return self

        def export(self, _file):
            if "." not in _file:
                return False
            f = open(_file,"w")
            _b = ""
            for s in self.styles:
                _b = _b + "" + s + "\n"
            print("b = " + _b)
            f.write(_b)
            f.close()

    class new_obj:
        def __init__(self, _type):
            self.type = _type
            self.children = []
            self.parent = ""
            self.attributes = []
            self.style = self.style_obj(self)
            self.innerHTML = ""
            self.innerText = ""

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

        def add_attribute(self, _str):
            self.attributes.append(_str)
            return self

        def get_attributes(self):
            _b = ""
            for s in self.attributes:
                _b = _b + " " + s
            return _b.strip()

        def get_tag_open(self):
            return "<" + self.type + " " + self.get_attributes() + ' style="' + self.style.get() + '">'

        def get_tag_close(self):
            return "</" + self.type + ">"

        def set_text(self, _str):
            self.innerText = _str
            return self

        def set_class(self,_str):
            self.add_attribute('class="' + _str + '"')
            return self

        def html(self):
            pass

        def get_parent(self):
            return self.parent

        def get_parent_super(self):
            _obj = self
            while _obj.parent:
                _obj = _obj.parent

            return _obj

        def generate_css_id(self, _f):
            if _f not in self.get_tag_open():
                self.add_attribute('id="' + _f + '"')

        def __link_self(self):
            _obj = self
            _s = self
            while _obj.parent:
                if _s in _obj.parent.children:
                    pass
                else:
                    _obj.parent.children.append(self)
                _obj = _obj.parent

        def on_click(self,_code):
            self.add_attribute('onclick="' + _code + '"')
            return self

        def on_mouse_enter(self,_code):
            self.add_attribute('onmouseover="' + _code + '"')
            return self

        def on_mouse_leave(self,_code):
            self.add_attribute('onmouseout="' + _code + '"')
            return self

        class style_obj:
            def __init__(self, _parent):
                self._style = ""
                self.parent = _parent

            def get(self):
                return self._style

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

    class table_helper:
        def __init__(self, _parent):
            self.parent = _parent

        def new(self, columns, rows, objs_to_add):

            o = self.table_obj(self, columns, rows, objs_to_add)

            return o.table

        class table_obj:
            def __init__(self, _parent, columns, rows, objs_to_add):
                self.parent = _parent
                table = self.parent.parent.new("table")
                trs = []
                tcs = []
                _append = ""
                _append_list = []

                for r in range(rows):
                    for c in range(columns):
                        for o in objs_to_add:
                            if str(int(o["row"]) - 1) == str(r) and str(int(o["column"]) - 1) == str(c):
                                _append = True
                                _append_obj = o["value"]
                                _append_list.append(_append_obj)
                                continue

                        td = self.parent.parent.new("td")
                        td.style.set("text-align:center;")

                        if _append:
                            for a in _append_list:
                                td.insert(a)

                            _append = False
                            _append_list = []
                            _append_obj = ""

                        tcs.append(td)

                    d = self.parent.parent.new("tr")
                    d.insert(tcs)
                    trs.append(d)

                table.insert(trs)
                self.table = table