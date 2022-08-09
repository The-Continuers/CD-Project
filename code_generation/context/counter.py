def get_counter():
    def counter_generator():
        counter_ = 0
        while True:
            yield (counter_ := counter_ + 1)

    it_ = counter_generator()

    def counter():
        return it_.__next__()

    return counter
