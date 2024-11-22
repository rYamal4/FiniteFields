class ListSet(list):
    """
    Derived from: https://stackoverflow.com/a/15993515

    Initialization:
        Same as with list (basically same as with set):
        (including sets, lists, tuples,
        generator expressions and range() expressions.)

    Setlike behaviors:
        for x in S():
        if x in S:  This is constant time.
        S.add(x)     "    "    "      "
        S.remove(x)  "    "    "      "
        len(s)       "    "    "      "
        print(S), str(S), repr(S)
        copy(S), list(S), set(S)  copy or cast.

    Listlike behaviors use internal list positions:
        S[3], S[-1]  # Returns an item.
        S[10:20]     # Returns a list, not ListSet.
        random.choice(S)  This is constant time.
        S += [4, 5, 6]
        S.append(7), same as S.add(7).
        len(s) in constant time.
        x = S.pop()  # Pop last element from internal list.
        y = S.pop(3) # Pop S[3] from internal list.
    """

    def __init__(self, *args, idx_of=None):
        super(ListSet, self).__init__(*args)
        if idx_of:
            self.idx_of = idx_of.copy()
        else:
            self.idx_of = {item: i
                           for (i, item) in enumerate(self)}

    def add(self, item):
        if item not in self.idx_of:
            super(ListSet, self).append(item)
            self.idx_of[item] = len(self) - 1

    def append(self, item):
        """
        append and += always append to the internal list,
        but remove and pop from other than the end
        can change the internal list's order.
        """
        self.add(item)

    def copy(self):
        """ Return a shallow copy of the ListSet. """
        return ListSet(self, idx_of=self.idx_of)

    def list(self):
        return super(ListSet, self).copy()

    def __iadd__(self, items):
        """ self += items """
        for item in items:
            self.add(item)
        return self

    def remove(self, element):
        """
        Remove an element from a set; it must be a member.

        If the element is not a member, raise a KeyError.
        """
        try:
            position = self.idx_of.pop(element)
        except:
            raise (KeyError(element))

        last_item = super(ListSet, self).pop()
        if position != len(self):
            self[position] = last_item
            self.idx_of[last_item] = position

    def pop(self, i=-1):
        """ Remove by internal list position. """
        item = self[i]
        self.remove(item)
        return item

    def __contains__(self, item):
        return item in self.idx_of

    def _str_body(self):
        return ", ".join(repr(item) for item in self)

    def __repr__(self):
        return "ListSet([" + self._str_body() + "])"

    def __str__(self):
        if self:
            return "{" + self._str_body() + "}"
        else:
            return "ListSet()"