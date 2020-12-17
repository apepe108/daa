from TdP_collections.tree.tree import Tree
import bisect


class ABTree(Tree):
    """A Currency a-b tree implementation. Use Currency code for implementing most algorithms."""

    # -------------- Nested class _Node -------------------------------------
    class _Node:
        """Non public class for storing a node."""
        __slots__ = '_elements', '_parent', '_children'

        def __init__(self, elements=None, children=None, parent=None):
            """Constructor for _ABNode class.

            :parameter elements: a list of elements to store in the node. By default it is empty.
            :parameter children: the children list of the node. By default it is empty.
            :parameter parent: the node node of the current node. By default the node have not node.
            """
            if children is None:
                children = []
            if elements is None:
                elements = []
            self._parent = parent
            self._elements = elements
            self._children = children

    # -------------- Nested class ABPosition----------------------------------
    class ABPosition(Tree.Position):
        """Abstraction that represents a node of the three."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """:return: the list of elements stored at this position."""
            return self._node._elements

        def __eq__(self, other):
            """:return: True if other Position represent the same location."""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Return associated node, if position is valid.

        :parameter p: The position that you would get the node."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """:return: Position instance for given node (or None if no node)."""
        return self.ABPosition(self, node) if node is not None else None

    # ---------------  ABTree constructor --------------------------

    def __init__(self, a=2, b=8):
        """An a-b tree constructor. For default is a 2-8 tree.
        :return: an a-b tree object.

        :parameter a: the minimum number of children in the node.
        :parameter b: the biggest number of children in the node.

        :raise ValueError if 2 <= a <= (b + 1) // 2."""
        if not 2 <= a <= (b + 1) // 2:
            raise ValueError('a must be 2 <= a <= (b + 1) // 2')
        self._root = None
        self.b = b
        self.a = a
        self._size = 0

    # ------------- abstract method that class must support ------------

    def root(self):
        """:return: Position representing the tree's _root (or None if Empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """:return: Position representing p's node.

        :parameter p: The position who we're searching the node."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def num_children(self, p):
        """:return: the number of children that Position p has

        :parameter p: The position who we're searching the number of children."""
        node = self._validate(p)
        return len(node._children)

    def children(self, p):
        """Generate an iteration of Position representing p's children.

        :parameter p: The position who we're generating a iteration."""
        node = self._validate(p)
        for n in node._children:
            yield self._make_position(n)

    def __len__(self):
        """:return: the total number of elements in the tree."""
        return self._size

    # -------- concrete methods implemented in this class --------------------

    def child(self, p, i):
        """:returns: the Position of the child of p in index i."""
        if not 0 <= i <= self.num_children(p)-1:
            raise IndexError('index out of range')
        node = self._validate(p)
        return self._make_position(node._children[i])

    def inorder(self):
        """Return an iterator of the inorder visit."""
        if not self.is_empty():
            for e in self._subtree_inorder(self.root()):  # start recursion
                yield e

    def _subtree_inorder(self, p):
        if self.is_leaf(p):
            for e in p.element():
                yield e
        else:
            elements = p.element()
            children = [c for c in self.children(p)]
            for i in range(len(elements)):
                for x in self._subtree_inorder(children[i]):
                    yield x
                yield elements[i]
            for x in self._subtree_inorder(children[-1]):  # last child is not in range
                yield x

    def _subtree_last_position(self, p):
        """Find the maximum in the subtree rooted in p."""
        if self.is_leaf(p):
            return p, len(p.element())-1
        else:
            return self._subtree_last_position(self.child(p, self.num_children(p)-1))

    def _subtree_first_position(self, p):
        """Find the minimum in the subtree rooted in p."""
        if self.is_leaf(p):
            return p, 0
        else:
            return self._subtree_first_position(self.child(p, 0))

    def after(self, p, i):
        """Return the Position and the index just after p at index i in the natural order.

        Return None if p at index i is the last position."""
        self._validate(p)
        if not 0 >= i >= len(p.element()) - 1:
            raise IndexError('index out of range')
        if self.is_leaf(p):
            return None if i == len(p.element()) - 1 else p, i + 1
        else:
            return self._subtree_first_position(self.child(p, i + 1))

    def before(self, p, i):
        """Return the Position and the index just before p at index i in the natural order.

        Return None if p at index i is the first position."""
        self._validate(p)
        if not 0 <= i <= len(p.element())-1:
            raise IndexError('index out of range')
        if self.is_leaf(p):
            return None if i == 0 else p, i-1
        else:
            return self._subtree_last_position(self.child(p, i))

    def _add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.

        :raise ValueError if tree nonempty.
        :parameter e: The element that you would set at root of the tree."""
        if self._root is not None:
            raise ValueError('root exists')
        self._size = 1
        self._root = self._Node([e])
        return self._make_position(self._root), 0

    def _add_element(self, p, i, e):
        p.element().insert(i, e)
        self._size += 1
        self._rebalance_insert(p)  # check for overflow

    def _delete_element(self, p, i):
        if not self.is_leaf(p):
            p_before, i_before = self.before(p, i)
            # swap with the predecessor
            p.element()[i], p_before.element()[i_before] = p_before.element()[i_before], p.element()[i]
            p = p_before
            i = i_before
        p.element().pop(i)
        self._size -= 1
        self._rebalance_delete(p)

    def _rebalance_insert(self, p):
        """Check overflow and make split algorithm"""
        if len(p.element()) < self.b:
            return
        node = p._node
        median = len(node._elements) // 2
        median_element = node._elements[median]
        new_right_node = self._Node(elements=node._elements[median + 1:], children=node._children[median + 1:])
        for child in new_right_node._children:
            child._parent = new_right_node
        node._elements = node._elements[:median]
        node._children = node._children[:median + 1]
        if node._parent is None:
            node._parent = new_right_node._parent = self._root = self._Node(elements=[median_element],
                                                                            children=[node, new_right_node])
        else:
            new_right_node._parent = node._parent
            bisect.insort(node._parent._elements, median_element)
            i = self._index(node._parent._elements, median_element)
            node._parent._children.insert(i + 1, new_right_node)
        self._rebalance_insert(self._make_position(node._parent))

    def _rebalance_delete(self, p):
        if self._size == 0:
            self._root = None
            p._node._parent = p._node     # deprecate old root
            return
        if self.is_root(p):
            if len(p.element()) < 1:
                self._root = p._node._children[0]  # make the new node the root
                self._root._parent = None
                p._node._children[0] = p._node  # deprecate old root
                p._node._parent = p._node
        elif len(p.element()) < self.a - 1:
            child_index = 0
            for c in self.children(self.parent(p)):         # search for the parent
                if c == p:
                    break
                child_index += 1
            # if has left sibling
            if not child_index == 0:
                left_sibling = self.child(self.parent(p), child_index-1)
                if len(left_sibling.element()) >= self.a:
                    self._transfer(self.parent(p), child_index, child_index-1, True)
                    return
            # if has right sibling
            if not child_index == self.num_children(self.parent(p))-1:
                right_sibling = self.child(self.parent(p), child_index+1)
                if len(right_sibling.element()) >= self.a:
                    self._transfer(self.parent(p), child_index+1, child_index, False)
                    return
            # if could not do a transfer does a fusion
            self._fusion(self.parent(p), child_index if child_index < self.num_children(self.parent(p))-1 else child_index-1)

    def _transfer(self, p, r_index, l_index, clockwise):
        """Executes the transfer algorithm to resolve underflows."""
        r_child = self.child(p, r_index)
        r_child_node = r_child._node
        l_child = self.child(p, l_index)
        l_child_node = l_child._node
        node = p._node
        if clockwise:
            elem = l_child_node._elements.pop()
            node._elements[l_index], elem = elem, node._elements[l_index]
            r_child_node._elements.insert(0, elem)
            if not self.is_leaf(l_child):
                child_transfer = l_child_node._children.pop()
                r_child_node._children.insert(0, child_transfer)
                child_transfer._parent = r_child._node
        else:
            elem = r_child_node._elements.pop(0)
            node._elements[l_index], elem = elem, node._elements[l_index]
            l_child_node._elements.append(elem)
            if not self.is_leaf(r_child):
                child_trasfer = r_child_node._children.pop(0)
                l_child_node._children.append(child_trasfer)
                child_trasfer._parent = l_child_node

    def _fusion(self, p, index):
        """Executes the fusion algorithm to resolve underflows.

        :parameter p: nodo contenente l'elemento da fondere con child_index figli
        :parameter index: indice dell'elemento da fondere con child_index figli"""
        node = p._node
        right_child = node._children[index + 1]
        left_child = node._children[index]
        parent_element = node._elements.pop(index)
        new_node = self._Node(elements=left_child._elements + [parent_element] + right_child._elements,
                              children=left_child._children + right_child._children,
                              parent=node)
        for c in new_node._children:  # update children's parent
            c._parent = new_node
        node._children[index] = new_node  # save the new fused node
        node._children.pop(index + 1)  # remove the no more existing child
        self._rebalance_delete(p)

    def __repr__(self):
        str(self)

    def __str__(self):
        return self._print_tree(self.root())

    def _print_tree(self, p, file=None, _prefix="", _last=True):
        """
        `- [CHF, GMD, KZT, MXN, TTD]
           |- [ANG, AWG, BHD, BRL, BYN]
           |  |- [AED, AFN, ALL, AMD]
           |  |- [AOA, ARS, AUD]
           |  |- [AZN, BAM, BBD, BDT, BGN]
           |  |- [BIF, BMD, BND, BOB, BOV]
           |  |- [BSD, BTN, BWP]
           |  `- [BZD, CAD, CDF, CHE]
           `- [CNY, DJF, ETB]
              |- [CHW, CLF, CLP]
              |- [COP, COU, CRC, CUC, CUP, CVE, CZK]
              |- [DKK, DOP, DZD, EGP, ERN]
              `- [EUR, FJD, FKP, GBP, GEL, GHS, GIP]
        """
        if self.is_empty():
            return ''
        # print(_prefix, "`- " if _last else "|- ", p.element(), sep="", file=file)
        s = str(_prefix) + str("`- " if _last else "|- ") + str(p.element()) + '\n'
        _prefix += "   " if _last else "|  "
        child_count = self.num_children(p)
        for i, child in enumerate(self.children(p)):
            _last = i == (child_count - 1)
            s += self._print_tree(child, file, _prefix, _last)
        return s

    @staticmethod
    def _index(a, x):
        """Locate the leftmost value exactly equal to x"""
        i = bisect.bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError
