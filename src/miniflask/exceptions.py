import traceback as tb
from colored import fg, bg, attr

def save_traceback():
    try:
        raise TracebackException("Could not register Variable.")
    except TracebackException as e:
        full_tb = tb.extract_stack()

        # ignore this very function in the traceback
        return full_tb[:-1]

class RegisteringException(Exception):

    def __str__(self):
        base_exc = super().__str__()
        traceback = format_traceback_list(self.traceback)
        return base_exc + "\n\n"+fg('red')+"The variable definition occured in"+attr('reset')+":\n"""+traceback

    def __init__(self, msg='', traceback=tb.extract_stack(), *args, **kwargs):

        # storing the traceback which provides useful information about where the exception occurred
        self.traceback = traceback

        super().__init__(msg)

class TracebackException(Exception):
    pass

def format_traceback_list(traceback_list, ignore_miniflask=True, exc=None):
    if ignore_miniflask:
        traceback_list = [t for t in traceback_list if not t.filename.endswith("src/miniflask/event.py") and (not t.filename.endswith("src/miniflask/miniflask.py") or t.name in ["load","run"])]
    if exc is not None:
        t = traceback_list[-1]
        t.filename = fg('green')+t.filename+attr('reset')
        t.lineno = fg('yellow')+str(t.lineno)+attr('reset')
        t.name = fg('blue')+attr("bold")+t.name+attr('reset')
        exception_type = fg('red')+attr('bold')+type(exc).__name__+attr('reset')
        last_msg = "  File %s, line %s, in %s\n    %s: %s" % (t.filename, t.lineno, t.name, exception_type, str(exc))
        traceback_list = traceback_list[:-1]
    else:
        last_msg = ""
    for t in traceback_list:
        t.filename = fg('green')+t.filename+attr('reset')
        t.lineno = fg('yellow')+str(t.lineno)+attr('reset')
        t.name = fg('blue')+attr("bold")+t.name+attr('reset')
    return "".join(tb.format_list(traceback_list))+last_msg