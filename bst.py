# bst.py
# Ben Prince
# ===================================================
# Implement a binary search tree that can store any
# arbitrary object in the tree.
# ===================================================


class Student:
    def __init__(self, number, name):
        self.grade = number  # this will serve as the object's key
        self.name = name

    def __lt__(self, kq):
        return self.grade < kq.grade

    def __gt__(self, kq):
        return self.grade > kq.grade

    def __eq__(self, kq):
        return self.grade == kq.grade

    def __str__(self):
        if self.grade is not None:
            n = str(self.name)
            g = str(self.grade)
            return n + "'s grade is " + g


class TreeNode:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val  # when this is a primitive, this serves as the node's key


class BST:
    def __init__(self, start_tree=None) -> None:
        """ Initialize empty tree """
        self.root = None

        # populate tree with initial nodes (if provided)
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self):
        """
        Traverses the tree using "in-order" traversal
        and returns content of tree nodes as a text string
        """
        values = [str(_) for _ in self.in_order_traversal()]
        return "TREE in order { " + ", ".join(values) + " }"

    def add(self, val):
        """
        Creates and adds a new node to the BSTree.
        If the BSTree is empty, the new node should added as the root.

        Args:
            val: Item to be stored in the new node
        """
        node = TreeNode(val)

        parent = None
        cur = self.root
        while cur is not None:
            parent = cur
            if node.val < cur.val:
                cur = cur.left
            else:
                cur = cur.right
        if parent is None:
            self.root = node
        elif node.val < parent.val:
            parent.left = node
        else:
            parent.right = node

    def in_order_traversal(self, cur_node=None, visited=None) -> []:
        """
        Perform in-order traversal of the tree and return a list of visited nodes
        """
        if visited is None:
            # first call to the function -> create container to store list of visited nodes
            # and initiate recursive calls starting with the root node
            visited = []
            self.in_order_traversal(self.root, visited)

        # not a first call to the function
        # base case - reached the end of current subtree -> backtrack
        if cur_node is None:
            return visited

        # recursive case -> sequence of steps for in-order traversal:
        # visit left subtree, store current node value, visit right subtree
        self.in_order_traversal(cur_node.left, visited)
        visited.append(cur_node.val)
        self.in_order_traversal(cur_node.right, visited)
        return visited

    def pre_order_traversal(self, cur_node=None, visited=None) -> []:
        """
        Perform pre-order traversal of the tree and return a list of visited nodes

        Returns:
            A list of nodes in the specified ordering
        """
        # first call
        if visited is None:
            visited = []
            self.pre_order_traversal(self.root, visited)

        # Base case
        if cur_node is None:
            return visited

        # pre order traversal sequence of steps: NLR
        # append, cur.left, cur.right, return
        visited.append(cur_node.val)
        self.pre_order_traversal(cur_node.left, visited)
        self.pre_order_traversal(cur_node.right, visited)
        return visited

    def post_order_traversal(self, cur_node=None, visited=None) -> []:
        """
        Perform post-order traversal of the tree and return a list of visited nodes

        Returns:
            A list of nodes in the specified ordering
        """
        # first call
        if visited is None:
            visited = []
            self.post_order_traversal(self.root, visited)

        # Base case
        if cur_node is None:
            return visited

        # pre order traversal sequence of steps: LRN
        # cur.left, cur.right, append, return
        self.post_order_traversal(cur_node.left, visited)
        self.post_order_traversal(cur_node.right, visited)
        visited.append(cur_node.val)
        return visited

    def contains(self, kq):
        """
        Searches BSTree to determine if the query key (kq) is in the BSTree.

        Args:
            kq: query key

        Returns:
            True if kq is in the tree, otherwise False
        """
        cur = self.root
        while cur is not None:
            if cur.val == kq:
                return True
            elif kq < cur.val:
                cur = cur.left
            else:
                cur = cur.right

        # if the value is not found, return false
        return False

    def left_child(self, node):
        """
        Returns the left-most child in a subtree.

        Args:
            node: the root node of the subtree

        Returns:
            The left-most node of the given subtree
        """
        while node.left is not None:
            node = node.left
        return node

    def get_parent(self, node):
        """
        Returns the parent of the argument passed
        Args:
             node: node passed to function
        """
        if node is self.root:
            return None
        else:
            cur = self.root
            while cur is not node:
                if node.val < cur.val:
                    if cur.left.val == node.val:
                        return cur
                    else:
                        cur = cur.left
                else:
                    if cur.right.val == node.val:
                        return cur
                    else:
                        cur = cur.right

            # If we get here the node was not found
            return False

    def remove(self, kq):
        """
        Removes node with key k, if the node exists in the BSTree.

        Args:
            kq: key of node to remove

        Returns:
            True if k is in the tree and successfully removed, otherwise False
        """
        # if the node is the root then call self.remove_first()
        if kq == self.root.val:
            self.remove_first()
            return

        # node at kq
        if self.contains(kq):
            node = self.root
            while node.val != kq:
                if kq < node.val:
                    node = node.left
                else:
                    node = node.right
        else:
            return False

        # parent of passed node
        kq_p = self.get_parent(node)

        # if node has no children, point kq_p to None
        if node.left is None and node.right is None:
            if node.val < kq_p.val:
                kq_p.left = None
            else:
                kq_p.right = None
        else:
            # node's in-order successor, if there isn't a node.right
            # move up node.left into its position and return
            if node.right is None:
                # in-order successor
                ios = node.left
                if node.val < kq_p.val:
                    kq_p.left = ios
                else:
                    kq_p.right = ios
                # free up node
                node.left = None
                node.right = None
                return True
            else:
                ios = self.left_child(node.right)

            # ios parent
            ios_p = self.get_parent(ios)
            ios.left = node.left
            if ios is not node.right:
                ios_p.left = ios.right
                ios.right = node.right

            # update kq_p to point to ios instead of node
            if node.val < kq_p.val:
                kq_p.left = ios
            else:
                kq_p.right = ios

        # free up node
        node.left = None
        node.right = None
        return True

    def get_first(self):
        """
        Gets the val of the root node in the BSTree.

        Returns:
            val of the root node, return None if BSTree is empty
        """
        if self.root is None:
            return None
        else:
            return self.root.val

    def remove_first(self):
        """
        Removes the val of the root node in the BSTree.

        Returns:
            True if the root was removed, otherwise False
        """
        if self.root is None:
            return False
        else:
            # root has no children
            if self.root.left is None and self.root.right is None:
                self.root = None
                return True
            # root doesn't have a right child
            elif self.root.right is None:
                self.root = self.root.left
                return True
            else:
                # root has both right and left children
                # in-order successor
                ios = self.left_child(self.root.right)
                # ios parent
                ios_p = self.get_parent(ios)

                if ios_p == self.root:
                    ios.left = self.root.left
                    self.root = ios
                    return True
                else:
                    ios.left = self.root.left
                    ios_p.left = ios.right
                    ios.right = self.root.right
                    self.root = ios
                    return True
