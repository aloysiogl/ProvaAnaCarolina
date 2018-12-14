from Node import Node


class Grammar:
    def __init__(self, V, T, P, S):
        self.V = V
        self.T = T
        self.P = P
        self.S = S

    def generate_left_derivations(self):
        root = Node(None, self.S)
        self.left_derivations_recursion(root, 0)
        # Grammar.print_tree(root)
        Grammar.dfs_find_derivation(root, [], "((n+n)*n)")

    def left_derivations_recursion(self, root, level):
        subs = self.find_first_non_terminal(root.content)
        for rule in self.P:
            if rule[0] == subs:
                root.add_son(Node(root, self.replace_first_non_terminal(root.content, rule[1])))
        bla = False
        for k in self.V:
            if k in list(root.content):
                bla = True
        if not bla:
            print(root.content)
        if level < 10:
            for son in root.son_list:
                self.left_derivations_recursion(son, level+1)

    def top_down_breadth(self, string):
        queue = []
        root = Node(None, self.S)
        queue.append(root)

        step = 1
        while len(queue) > 0:
            print("Step : " + str(step))
            print([x.content for x in queue])
            step += 1
            current = queue.pop(0)
            if self.consistent_prefix(current.content, string):
                if current.content == string:
                    self.print_tree2(root)
                    break
                subs = self.find_first_non_terminal(current.content)
                for rule in self.P:
                    if rule[0] == subs:
                        new_son = Node(current, self.replace_first_non_terminal(current.content, rule[1]))
                        queue.append(new_son)
                        current.add_son(new_son)

    def top_down_depth(self, string):
        stack = []
        root = Node(None, self.S)
        stack.append(root)
        step = 1

        while len(stack) > 0:
            print("Step : " + str(step))
            print([x.content for x in stack])
            step += 1
            current = stack.pop(len(stack)-1)
            if self.consistent_prefix(current.content, string):
                if current.content == string:
                    self.print_tree2(root)
                    break
                subs = self.find_first_non_terminal(current.content)
                for rule in self.P:
                    if rule[0] == subs:
                        new_son = Node(current, self.replace_first_non_terminal(current.content, rule[1]))
                        stack.append(new_son)
                        current.add_son(new_son)

    def bottom_up_breadth(self, string):
        queue = []
        root = Node(None, string)
        queue.append(root)

        step = 1
        while len(queue) > 0:
            print("Step : " + str(step))
            print([x.content for x in queue])
            step += 1
            current = queue.pop(0)

            if current.content == self.S:
                self.print_tree2(root)
                print("Parsing Ok!")
                break
            for reduct in self.generate_reductions(current.content):
                if self.is_left_reduction(reduct, current.content):
                    new_son = Node(current, reduct)
                    queue.append(new_son)
                    current.add_son(new_son)

    def bottom_up_depth(self, string):
        stack = []
        root = Node(None, string)
        stack.append(root)
        step = 1

        while len(stack) > 0:
            print("Step : " + str(step))
            print([x.content for x in stack])
            step += 1
            current = stack.pop(len(stack)-1)

            if current.content == self.S:
                self.print_tree2(root)
                print("Parsing Ok!")
                break
            for reduct in self.generate_reductions(current.content):
                if self.is_left_reduction(reduct, current.content):
                    new_son = Node(current, reduct)
                    stack.append(new_son)
                    current.add_son(new_son)

            # if self.consistent_prefix(current.content, string):
            #     if current.content == string:
            #         self.print_tree2(root)
            #         break
            #     subs = self.find_first_non_terminal(current.content)
            #     for rule in self.P:
            #         if rule[0] == subs:
            #             new_son = Node(current, self.replace_first_non_terminal(current.content, rule[1]))
            #             stack.append(new_son)
            #             current.add_son(new_son)

    def consistent_prefix(self, test_string, comparator):
        for i in range(min(len(test_string), len(comparator))):
            if test_string[i] in self.V:
                return True
            else:
                if test_string[i] != comparator[i]:
                    return False
        return len(test_string) <= len(comparator)

    def generate_reductions(self, string):
        reducts = []
        for i in range(len(string)+1):
            u = string[0:i]
            v = string[i:len(string)]
            for j in range(len(u)+1):
                for production in self.P:
                    if u[len(u)-j:len(u)] == production[1]:
                        reducts.append(u[0:len(u)-j]+production[0]+v)
        return reducts

    def is_left_reduction(self, reduct, parent):
        subs = self.find_last_non_terminal(reduct)
        for rule in self.P:
            if rule[0] == subs:
                if self.replace_last_non_terminal(reduct, rule[1]) == parent:
                    return True
        return False

    @staticmethod
    def dfs_find_derivation(node, path_list, desire):
        for child in node.son_list:
            Grammar.dfs_find_derivation(child, path_list + [node.content], desire)
        if desire == node.content:
            print(path_list, node.content)

    @staticmethod
    def print_tree(node, level=0):
        ret = "\t" * level + node.content
        print(ret)
        if len(node.son_list) > 0:
            for child in node.son_list:
                Grammar.print_tree(child, level + 1)

    def replace_first_non_terminal(self, string, replace_with):
        for i in range(len(string)):
            if string[i] in self.V:
                return string[0:i] + replace_with + string[i+1:]

    def find_first_non_terminal(self, string):
        for i in range(len(string)):
            if string[i] in self.V:
                return string[i]

    def find_last_non_terminal(self, string):
        for i in range(len(string)):
            if string[len(string)-i-1] in self.V:
                return string[len(string)-i-1]

    def replace_last_non_terminal(self, string, replace_with):
        for i in range(len(string)):
            if string[len(string)-i-1] in self.V:
                return string[0:len(string)-i-1] + replace_with + string[len(string)-i:]

    def print_tree2(self, current_node, indent="", last='updown'):

        nb_children = lambda node: sum(nb_children(child) for child in node.son_list) + 1
        size_branch = {child: nb_children(child) for child in current_node.son_list}

        """ Creation of balanced lists for "up" branch and "down" branch. """
        up = sorted(current_node.son_list, key=lambda node: nb_children(node))
        down = []
        while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
            down.append(up.pop())

        """ Printing of "up" branch. """
        for child in up:
            next_last = 'up' if up.index(child) is 0 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node.content))
            self.print_tree2(child, indent=next_indent, last=next_last)

        """ Printing of current node. """
        if last == 'up':
            start_shape = '┌'
        elif last == 'down':
            start_shape = '└'
        elif last == 'updown':
            start_shape = ' '
        else:
            start_shape = '├'

        if up:
            end_shape = '┤'
        elif down:
            end_shape = '┐'
        else:
            end_shape = ''

        print('{0}{1}{2}{3}'.format(indent, start_shape, current_node.content, end_shape))

        """ Printing of "down" branch. """
        for child in down:
            next_last = 'down' if down.index(child) is len(down) - 1 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.content))
            self.print_tree2(child, indent=next_indent, last=next_last)


if __name__ == "__main__":
    V = ['S']
    T = ['a', 'b', '1', '2', '3']
    P = [('S', 'bS1'), ('S', 'b1'), ('S', 'aaS2'), ('S', 'aa2'), ('S', 'abS3'), ('S', 'ab3')]
    S = 'S'

    grammar = Grammar(V, T, P, S)

    V2 = ['S']
    T2 = ['a', 'b', '1', '2', '3']
    P2 = [('S', 'bbS1'), ('S', 'bb1'), ('S', 'baaS2'), ('S', 'baa2'), ('S', 'aS3'), ('S', 'a3')]
    S2 = 'S'

    grammar2 = Grammar(V2, T2, P2, S2)

    grammar.bottom_up_depth("abb13")
    # grammar2.top_down_breadth("abababbaba")

    # V3 = ['E', 'A', 'M', 'X', 'Y', 'O', 'C', 'Z']
    # T3 = ['+', '*', '(', ')', "n"]
    # P3 = [('E', 'EX'), ('E', 'EY'), ('E', 'OZ'), ('E', 'n'), ('X', 'AE'), ('Y', 'ME'), ('Z', 'EC'), ('A', '+'),
    #       ('M', '*'), ('O', '('), ('C', ')')]
    # S3 = 'E'
    #
    # chomsky = Grammar(V3, T3, P3, S3)
    #
    # V4 = ['E', 'A', 'M', 'X', 'C', 'K']
    # T4 = ['+', '*', '(', ')', "n"]
    # P4 = [('C', ')'), ('M', '*E'), ('A', '+E'), ('X', 'nC'), ('X', 'nKC'), ('X', '(XC'), ('X', '(XKC'),
    #       ('E', 'n'), ('E', 'nK'), ('E', '(X'), ('E', '(XK'), ('K', '+E'), ('K', '+EK'), ('K', '*E'), ('K', '*EK')]
    # S4 = 'E'
    #
    # greibach = Grammar(V4, T4, P4, S4)

    # grammar.generate_left_derivations()

    # grammar2.generate_left_derivations()

    # chomsky.generate_left_derivations()
    # greibach.generate_left_derivations()
    # greibach.top_down_depth("(n+n)")
    # greibach.top_down_depth("(n+n)")
    # greibach.bottom_up_breadth("(n+n)")
    # greibach.bottom_up_depth("(n+n)")
    #
    # V5 = ['S', 'A', 'T']
    # T5 = ['+', 'b', '(', ')']
    # P5 = [('S', 'A'), ('A', 'T'), ('A', 'A+T'), ('T', 'b'), ('T', '(A)')]
    # S5 = 'S'
    #
    # test = Grammar(V5, T5, P5, S5)
    # test.top_down_depth("(b+b)")
    # tst_str = "S"
    # reductions = test.generate_reductions(tst_str)
    # print(reductions)
    # for redu in reductions:
    #     if test.is_left_reduction(redu, tst_str):
    #         print(redu)
    #         pass
    # test.bottom_up_breadth("(b+b)")
