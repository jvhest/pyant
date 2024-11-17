from pyant.taskdefs import echo, copy, mkdir

_task_defs_ = {
    "echo": echo.Echo,
    "copy": copy.Copy,
    "mkdir": mkdir.MkDir
}
