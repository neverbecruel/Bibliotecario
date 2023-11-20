def open_window(window_class):
    def decorator(func):
        def wrapper(self):
            func(self)
            self.new_window = window_class()
            self.new_window.show()
        return wrapper
    return decorator