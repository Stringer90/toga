class BaseProxy:
    page_provider = staticmethod(lambda: None)

    def _page(self):
        return type(self).page_provider()

    def __init__(self, obj_id: str, ns: str = "widgets"):
        object.__setattr__(self, "_id", obj_id)
        object.__setattr__(self, "_ns", ns)

    @property
    def id(self) -> str:
        return object.__getattribute__(self, "_id")

    @property
    def js_ref(self) -> str:
        ns = object.__getattribute__(self, "_ns")
        if ns =="widgets":
            return f"self.my_widgets[{repr(self.id)}]"
        else:
            return f"self.my_obj[{repr(self.id)}]"

    @classmethod
    def from_id(cls, widget_id: str, ns: str = "widgets") -> "BaseProxy":
        return cls(widget_id, ns)

    def _unwrap(self, v):
        if isinstance(v, dict) and v.get("$t") == "handle":
            ns = v.get("ns", "widgets")
            return BaseProxy(v["id"], ns)
        # lists/dicts may contain nested handles
        if isinstance(v, list):
            return [self._unwrap(x) for x in v]
        if isinstance(v, dict):
            return {k: self._unwrap(x) for k, x in v.items()}
        return v

    def _is_function(self, name: str) -> bool:
        prop = repr(name)
        code = (
            f"_obj = {self.js_ref}\n"
            f"_attr = getattr(_obj, {prop})\n"
            f"result = callable(_attr)"
        )
        out = self._page().eval_js("(code) => window.test_cmd(code)", code)
        return bool(self._unwrap(out))

    def _encode_value(self, value) -> str:
        # keep existing behavior: proxies pass by reference using code expr
        if isinstance(value, BaseProxy):
            return value.js_ref
        if isinstance(value, (str, int, float, bool)) or value is None:
            return repr(value)
        #if list/tuple
        if isinstance(value, (list, tuple)):
            inner = ", ".join(self._encode_value(v) for v in value)
            if isinstance(value, tuple):
                if len(value) == 1:
                    inner += ","
                return f"({inner})"
            return f"[{inner}]"
        #raise error if not any of this, will need to implement in the future if needed
        raise TypeError(
            f"Don't know how to encode {type(value).__name__}. "
            "Pass a primitive, a Proxy, or a container of those."
        )
    def __setattr__(self, name, value):
        prop = repr(name)
        if name.startswith("_"):
            return object.__setattr__(self, name, value)
        if name == "id":
            raise AttributeError("Proxy 'id' is read-only")

        if name == "text":
            rhs = repr(str(value))
        else:
            rhs = self._encode_value(value)
        code = f"setattr({self.js_ref}, {prop}, {rhs})"
        out = self._page().eval_js("(code) => window.test_cmd(code)", code)
        self._unwrap(out)

    def __getattr__(self, name):
        prop = repr(name)
        if self._is_function(name):
            def _method(*args):
                parts = [self._encode_value(a) for a in args]
                args_py = ", ".join(parts)
                code = (
                    f"_obj = {self.js_ref}\n"
                    f"_fn = getattr(_obj, {prop})\n"
                    f"result = _fn({args_py})"
                )
                out = self._page().eval_js("(code) => window.test_cmd(code)", code)
                return self._unwrap(out)
            return _method

        code = f"result = getattr({self.js_ref}, {prop})"
        out = self._page().eval_js("(code) => window.test_cmd(code)", code)
        return self._unwrap(out)

    def add_to_main_window(self):
        out = self._page().eval_js(
            "(code) => window.test_cmd(code)",
            f"self.main_window.content.add({self.js_ref})",
        )
        self._unwrap(out)