def Producer(func):
    func._is_producer_ = True
    return func


def Consumer(func):
    func._is_consumer_ = True
    return func
