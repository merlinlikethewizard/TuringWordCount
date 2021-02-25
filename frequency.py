import string
from time import time
from sys import argv

class TuringMachine:
    '''
    A real live Turing Machine! Minus the infinate tape.
    
    Creates a model of a Turing Machine with <rules>, <start_state>,
    <start_index>, <default_slot_value>, and <start_tape>.
    
    >>> rules = []
    
    >>>              # Curr. | Read  | New   | Write | Move  
    >>>              # State | Value | State | Value | Dist. 
    >>>              #-------|-------|-------|-------|-------
    >>> rules.append(( 'A'   , '0'   , 'A'   , '1'   , 1     ))
    
    >>> tm = TuringMachine(rules=rules, start_state='A')
    
    >>> for step_num in xrange(5):
    ...     print tm
    ...     tm.step()
    ...     if step_num == 4:
    ...         print tm
    --- Step 0 ---
     0 0 0 0 0 0 0 0 0>0<0 0 0 0 0 0 0 0 0
    State: A
    Index: 0
    --- Step 1 ---
     0 0 0 0 0 0 0 0 1>0<0 0 0 0 0 0 0 0 0
    State: A
    Index: 1
    --- Step 2 ---
     0 0 0 0 0 0 0 1 1>0<0 0 0 0 0 0 0 0 0
    State: A
    Index: 2
    --- Step 3 ---
     0 0 0 0 0 0 1 1 1>0<0 0 0 0 0 0 0 0 0
    State: A
    Index: 3
    --- Step 4 ---
     0 0 0 0 0 1 1 1 1>0<0 0 0 0 0 0 0 0 0
    State: A
    Index: 4
    --- Step 5 ---
     0 0 0 0 1 1 1 1 1>0<0 0 0 0 0 0 0 0 0
    State: A
    Index: 5
    
    >>> tm.get_whole_printout()
    '11111'
    
    '''
    def __init__(self, rules, start_state, start_index=0, default_slot_value='0', start_tape=()):
        self.state = start_state
        self.index = start_index
        self.default_slot_value = default_slot_value
        self.tape = dict(enumerate(start_tape))
        
        self.rules = {}
        for current_state, read_value, new_state, write_value, move_dist in rules:
            self.rules[(current_state, read_value)] = (new_state, write_value, move_dist)
            
        self.steps = 0
        self.halt = False
            
    def __getitem__(self, index):
        if index in self.tape:
            return self.tape[index]
        else:
            return self.default_slot_value
        
    def __setitem__(self, index, value):
        if value == self.default_slot_value:
            if index in self.tape:
                del(self.tape[index])
        else:
            self.tape[index] = value
        
    def __repr__(self):
        s = '--- Step {} ---\n'.format(self.steps)
        for i in xrange(-9, 10):
            if i == 0:
                s += '>'
            elif i == 1:
                s += '<'
            else:
                s += ' '
            s += str(self[self.index + i])
        if self.halt:
            s += ' HALT'
        s += '\nState: ' + str(self.state)
        s += '\nIndex: ' + str(self.index)
        return s
        
    def step(self):
        if self.halt:
            return
        
        self.steps += 1
        
        sitch = (self.state, self[self.index])
        
        if sitch not in self.rules:
            self.halt = True
            return
            
        new_state, write_value, move_dist = self.rules[sitch]
        
        self.state = new_state
        self[self.index] = write_value
        self.index += move_dist
        
    def get_whole_printout(self):
        index = 0
        s = ''
        while True:
            index -= 1
            if index not in self.tape:
                index += 1
                break
        while True:
            if index in self.tape:
                s += self.tape[index]
            else:
                return s
            index += 1
            
            
def getStopWordsRules(base_rule, stop_words, finish):
    rules = []
    rules.append((base_rule, '-', base_rule, '-', 1))
    if '' in stop_words:
        rules.append((base_rule, '#', finish, '-', 1))
    for letter in string.ascii_lowercase:
        word_group = [word[1:] for word in stop_words if word.startswith(letter)]
        if len(word_group) > 0:
            rules.append((base_rule, letter, base_rule + letter, letter, 1))
            rules += getStopWordsRules(base_rule + letter, word_group, finish)
        else:
            rules.append((base_rule, letter, finish, letter, 1))
    return rules


def generateRules(charset, stop_words):
    
    #############
    ### RULES #######################################################
    #################################################################
    # Curr. | Read  | New   | Write | Move  
    # State | Value | State | Value | Dist. 
    #-------|-------|-------|-------|-------

    rules = []
    
    
    ########################
    ### \/ Word count \/
    
    
    for letter in string.ascii_lowercase + ' ':
        rules.append(('scrub', letter, 'scrub', letter, 1))
        rules.append(('scrub', letter.upper(), 'scrub', letter, 1))
        
    for char in charset.difference(string.ascii_letters + ' '):
        rules.append(('scrub', char, 'scrub', ' ', 1))
        
    rules.append(('scrub', '+', 'mark_end', ' ', 1))
    rules.append(('mark_end', '+', 'cap_mem', '$', 1))
    rules.append(('cap_mem', '+', 'go_mark_beginning', '>', -1))
    
    for skip_letter in string.ascii_lowercase + ' $':
        rules.append(('go_mark_beginning', skip_letter, 'go_mark_beginning', skip_letter, -1))
        
    rules.append(('go_mark_beginning', '+', 'find_word', ' ', 1))
    
    rules.append(('find_word', ' ', 'find_word', ' ', 1))
    
    for letter in string.ascii_lowercase:
        rules.append(('find_word', letter, 'go_match_letter_' + letter, '*', 1))
    
    for letter in string.ascii_lowercase:
        rules.append(('find_letter', letter, 'go_match_letter_' + letter, '*', 1))
        
    for match_letter in string.ascii_lowercase:
        for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
            rules.append(('go_match_letter_' + match_letter, skip_letter, 'go_match_letter_' + match_letter, skip_letter, 1))
        rules.append(('go_match_letter_' + match_letter, '[', 'match_letter_' + match_letter, '-', 1))
        rules.append(('match_letter_' + match_letter, match_letter, 'match_success_' + match_letter, match_letter, 1))
        rules.append(('match_success_' + match_letter, '-', 'go_replace_letter_' + match_letter, '[', -1))
        for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
            rules.append(('go_replace_letter_' + match_letter, skip_letter, 'go_replace_letter_' + match_letter, skip_letter, -1))
        rules.append(('go_replace_letter_' + match_letter, '*', 'find_letter', match_letter, 1))
        
        rules.append(('match_success_' + match_letter, '#', 'go_replace_letter_' + match_letter, '@', -1))
        rules.append(('go_match_letter_' + match_letter, '@', 'match_failure_' + match_letter, '#', 1))
        
        rules.append(('go_match_letter_' + match_letter, '>', 'new_word_' + match_letter, '>', -1))
        rules.append(('match_letter_' + match_letter, '>', 'new_word_' + match_letter, '>', -1))
        for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
            rules.append(('new_word_' + match_letter, skip_letter, 'new_word_' + match_letter, skip_letter, -1))
        rules.append(('new_word_' + match_letter, '*', 'new_word_reset', match_letter, -1))
        
        for mismatch_letter in string.ascii_lowercase:
            if mismatch_letter != match_letter:
                rules.append(('match_letter_' + match_letter, mismatch_letter, 'match_failure_' + match_letter, mismatch_letter, 1))
                
    for match_letter in string.ascii_lowercase + ' ':
        for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
            rules.append(('match_failure_' + match_letter, skip_letter, 'match_failure_' + match_letter, skip_letter, 1))
        rules.append(('match_failure_' + match_letter, '~', 'new_match_mark_' + match_letter, '~', 1))
        rules.append(('new_match_mark_' + match_letter, '-', 'new_match_' + match_letter, '[', -1))
        rules.append(('new_match_mark_' + match_letter, '>', 'new_word_' + match_letter, '>', -1))
        for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
            rules.append(('new_match_' + match_letter, skip_letter, 'new_match_' + match_letter, skip_letter, -1))
        rules.append(('new_match_' + match_letter, '*', 'new_match_reset', match_letter, -1))
        
    for skip_letter in string.ascii_lowercase:
        rules.append(('new_word_reset', skip_letter, 'new_word_reset', skip_letter, -1))
        
    rules.append(('new_word_reset', ' ', 'new_word_copy', ' ', 1))
    
    for letter in string.ascii_lowercase:
        rules.append(('new_word_copy', letter, 'go_place_' + letter, '*', 1))
        
    for skip_letter in string.ascii_lowercase:
        rules.append(('new_match_reset', skip_letter, 'new_match_reset', skip_letter, -1))
    
    rules.append(('new_match_reset', ' ', 'find_letter', ' ', 1))
        
    for place_letter in string.ascii_lowercase:
        for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
            rules.append(('go_place_' + place_letter, skip_letter, 'go_place_' + place_letter, skip_letter, 1))
        rules.append(('go_place_' + place_letter, '>', 'place_' + place_letter, '-', 1))
        rules.append(('place_' + place_letter, '+', 'move_cap_' + place_letter, place_letter, 1))
        rules.append(('move_cap_' + place_letter, '+', 'new_word_go_replace_letter_' + place_letter, '>', -1))
        for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
            rules.append(('new_word_go_replace_letter_' + place_letter, skip_letter, 'new_word_go_replace_letter_' + place_letter, skip_letter, -1))
        rules.append(('new_word_go_replace_letter_' + place_letter, '*', 'new_word_copy', place_letter, 1))
        
    rules.append(('new_word_copy', ' ', 'go_end_new_word', '*', 1))
    for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
        rules.append(('go_end_new_word', skip_letter, 'go_end_new_word', skip_letter, 1))
        
    rules.append(('go_end_new_word', '>', 'first_zero_dash', '#', 1))
    rules.append(('first_zero_dash', '+', 'first_zero', '-', 1))
    rules.append(('first_zero', '+', 'second_zero_dash', '0', 1))
    rules.append(('second_zero_dash', '+', 'second_zero', '-', 1))
    rules.append(('second_zero', '+', 'third_zero_dash', '0', 1))
    rules.append(('third_zero_dash', '+', 'third_zero', '-', 1))
    rules.append(('third_zero', '+', 'one_dash', '0', 1))
    rules.append(('one_dash', '+', 'one', '-', 1))
    rules.append(('one', '+', 'tild', '1', 1))
    rules.append(('tild', '+', 'new_word_cap', '~', 1))
    rules.append(('new_word_cap', '+', 'go_reset_lookup', '>', -1))
    
    for skip_letter in string.ascii_lowercase + ' -#0123456789~':
        rules.append(('go_reset_lookup', skip_letter, 'go_reset_lookup', skip_letter, -1))
        
    rules.append(('go_reset_lookup', '$', 'reset_lookup', '$', 1))
    rules.append(('reset_lookup', '-', 'go_replace_space', '[', -1))
    
    for skip_letter in string.ascii_lowercase + ' $':
        rules.append(('go_replace_space', skip_letter, 'go_replace_space', skip_letter, -1))
        
    rules.append(('go_replace_space', '*', 'find_word', ' ', 1))
    
    rules.append(('find_letter', ' ', 'check_if_end_of_word', '*', 1))
    for skip_letter in string.ascii_lowercase + ' $-#0123456789~':
        rules.append(('check_if_end_of_word', skip_letter, 'check_if_end_of_word', skip_letter, 1))
    
    rules.append(('check_if_end_of_word', '[', 'match_failure_ ', '-', 1))
    rules.append(('check_if_end_of_word', '@', 'find_tild', '#', 1))
    
    for skip_letter in string.ascii_lowercase + ' $-#0123456789':
        rules.append(('find_tild', skip_letter, 'find_tild', skip_letter, 1))
    rules.append(('find_tild', '~', 'inc_num', '~', -1))
    
    rules.append(('inc_num', '-', 'inc_num', '-', -1))
    for i in xrange(9):
        rules.append(('inc_num', str(i), 'go_reset_lookup', str(i+1), -1))
    rules.append(('inc_num', '9', 'inc_num', '0', -1))
    rules.append(('inc_num', '#', 'WORD_COUNT_EXCEEDED_9999', '#', -1))
    
    
    ### /\ Word count /\
    ########################
    ### \/ Stop Words \/
    
    
    rules.append(('find_word', '$', 'check_stop_word_', '$', 1))
    rules.append(('check_stop_word_', '[', 'check_stop_word_', '-', 1))
    rules += getStopWordsRules('check_stop_word_', stop_words, 'go_check_stop_word')
    for skip_letter in string.ascii_lowercase + '-#0123456789':
        rules.append(('go_check_stop_word', skip_letter, 'go_check_stop_word', skip_letter, 1))
    rules.append(('go_check_stop_word', '~', 'check_stop_word_', '~', 1))
    rules.append(('check_stop_word_', '>', 'place_two_four', '>', 1))
    
    
    ### /\ Stop Words /\
    ########################
    ### \/ Highest 25 \/
    
    
    rules.append(('place_two_four', '+', 'place_four', '2', 1))
    rules.append(('place_four', '+', 'make_max_register', '4', 1))
    rules.append(('make_max_register', '+', 'max_register_first_zero_dash', '|', 1))
    rules.append(('max_register_first_zero_dash', '+', 'max_register_first_zero', '-', 1))
    rules.append(('max_register_first_zero', '+', 'max_register_second_zero_dash', '0', 1))
    rules.append(('max_register_second_zero_dash', '+', 'max_register_second_zero', '-', 1))
    rules.append(('max_register_second_zero', '+', 'max_register_third_zero_dash', '0', 1))
    rules.append(('max_register_third_zero_dash', '+', 'max_register_third_zero', '-', 1))
    rules.append(('max_register_third_zero', '+', 'max_register_fourth_zero_dash', '0', 1))
    rules.append(('max_register_fourth_zero_dash', '+', 'max_register_fourth_zero', '-', 1))
    rules.append(('max_register_fourth_zero', '+', 'cap_max_register', '0', 1))
    rules.append(('cap_max_register', '+', 'reset_max_register', '=', -1))
    
    for digit in '0123456789':
        rules.append(('reset_max_register', digit, 'reset_max_register', '0', -1))
    rules.append(('reset_max_register', '-', 'reset_max_register', '-', -1))
    rules.append(('reset_max_register', '[', 'reset_max_register', '[', -1))
    rules.append(('reset_max_register', '|', 'mark_max_register', '|', 1))
    rules.append(('mark_max_register', '-', 'reset_max_search', '[', -1))
    rules.append(('mark_max_register', '[', 'reset_max_search', '[', -1))
    
    for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
        rules.append(('reset_max_search', skip_letter, 'reset_max_search', skip_letter, -1))
    rules.append(('reset_max_search', '@', 'reset_max_search', '-', -1))
    rules.append(('reset_max_search', '$', 'find_number', '$', 1))
    for skip_letter in string.ascii_lowercase + '-0123456789~':
        rules.append(('find_number', skip_letter, 'find_number', skip_letter, 1))
    rules.append(('find_number', '#', 'go_find_digit', '#', 1))
    for skip_digit in '0123456789':
        rules.append(('go_find_digit', skip_digit, 'go_find_digit', skip_digit, 1))
    rules.append(('go_find_digit', '-', 'find_digit', '[', 1))
    
    for match_digit in '0123456789':
        rules.append(('find_digit', match_digit, 'go_match_digit_' + match_digit, match_digit, 1))
        for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
            rules.append(('go_match_digit_' + match_digit, skip_letter, 'go_match_digit_' + match_digit, skip_letter, 1))
        rules.append(('go_match_digit_' + match_digit, '[', 'match_digit_' + match_digit, '-', 1))
        for register_digit in '0123456789':
            if match_digit > register_digit:
                rules.append(('match_digit_' + match_digit, register_digit, 'match_greater', match_digit, 1))
            elif match_digit < register_digit:
                rules.append(('match_digit_' + match_digit, register_digit, 'match_less', register_digit, -1))
            else:
                rules.append(('match_digit_' + match_digit, register_digit, 'match_equal', register_digit, 1))
                
    rules.append(('match_equal', '-', 'go_get_next_digit', '[', -1))
    for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
        rules.append(('go_get_next_digit', skip_letter, 'go_get_next_digit', skip_letter, -1))
    rules.append(('go_get_next_digit', '[', 'go_find_digit', '-', 1))
    
    rules.append(('match_equal', '=', 'match_less', '=', -1))
    
    rules.append(('match_greater', '-', 'go_find_copy_digit', '[', -1))
    for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
        rules.append(('go_find_copy_digit', skip_letter, 'go_find_copy_digit', skip_letter, -1))
    rules.append(('go_find_copy_digit', '[', 'go_copy_digit', '-', 1))
    for skip_digit in '0123456789':
        rules.append(('go_copy_digit', skip_digit, 'go_copy_digit', skip_digit, 1))
    rules.append(('go_copy_digit', '-', 'copy_digit', '[', 1))
    
    for copy_digit in '0123456789':
        rules.append(('copy_digit', copy_digit, 'go_place_digit_' + copy_digit, copy_digit, 1))
        for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
            rules.append(('go_place_digit_' + copy_digit, skip_letter, 'go_place_digit_' + copy_digit, skip_letter, 1))
        rules.append(('go_place_digit_' + copy_digit, '[', 'place_digit_' + copy_digit, '-', 1))
        for replace_digit in '0123456789':
            rules.append(('place_digit_' + copy_digit, replace_digit, 'match_greater', copy_digit, 1))
            
    rules.append(('match_greater', '=', 'copy_reset_max_register', '=', -1))
    for skip_letter in '-0123456789':
        rules.append(('copy_reset_max_register', skip_letter, 'copy_reset_max_register', skip_letter, -1))
    rules.append(('copy_reset_max_register', '|', 'copy_mark_max_register', '|', 1))
    rules.append(('copy_mark_max_register', '-', 'finish_number_copy', '[', -1))
    
    for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
        rules.append(('finish_number_copy', skip_letter, 'finish_number_copy', skip_letter, -1))
    rules.append(('finish_number_copy', '[', 'label_highest', '-', -1))
    
    for skip_letter in string.ascii_lowercase + '-0123456789':
        rules.append(('label_highest', skip_letter, 'label_highest', skip_letter, -1))
    rules.append(('label_highest', '#', 'clear_previous_highest', '@', -1))
    
    for skip_letter in string.ascii_lowercase + '-#~0123456789':
        rules.append(('clear_previous_highest', skip_letter, 'clear_previous_highest', skip_letter, -1))
    rules.append(('clear_previous_highest', '@', 'go_to_highest', '#', 1))
    rules.append(('clear_previous_highest', '$', 'go_to_highest', '$', 1))
    
    for skip_letter in string.ascii_lowercase + '-#~0123456789':
        rules.append(('go_to_highest', skip_letter, 'go_to_highest', skip_letter, 1))
    rules.append(('go_to_highest', '@', 'find_number', '@', 1))
    
    for skip_letter in '-0123456789':
        rules.append(('match_less', skip_letter, 'match_less', skip_letter, -1))
    rules.append(('match_less', '|', 'less_reset_max_register', '|', 1))
    rules.append(('less_reset_max_register', '-', 'go_find_copy_number', '[', -1))
    for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
        rules.append(('go_find_copy_number', skip_letter, 'go_find_copy_number', skip_letter, -1))
    rules.append(('go_find_copy_number', '[', 'find_number', '-', 1))
    
    rules.append(('find_number', '>', 'go_copy_max_word', '>', 1))
    
    for skip_letter in string.ascii_lowercase + '-#~0123456789>|':
        rules.append(('go_copy_max_word', skip_letter, 'go_copy_max_word', skip_letter, -1))
    rules.append(('go_copy_max_word', '@', 'begin_copy_max_word', '@', -1))
    
    for skip_letter in string.ascii_lowercase + '-':
        rules.append(('begin_copy_max_word', skip_letter, 'begin_copy_max_word', skip_letter, -1))
    rules.append(('begin_copy_max_word', '~', 'go_copy_max_letter', '~', 1))
    rules.append(('begin_copy_max_word', '$', 'go_copy_max_letter', '$', 1))
    rules.append(('go_copy_max_letter', '-', 'copy_max_letter', '{', 1))
    for skip_letter in string.ascii_lowercase:
        rules.append(('go_copy_max_letter', skip_letter, 'go_copy_max_letter', skip_letter, 1))
    
    for copy_letter in string.ascii_lowercase:
        rules.append(('copy_max_letter', copy_letter, 'go_place_max_letter_' + copy_letter, copy_letter, 1))
        for skip_letter in string.ascii_lowercase + ' -@#~0123456789>|[=\n':
            rules.append(('go_place_max_letter_' + copy_letter, skip_letter, 'go_place_max_letter_' + copy_letter, skip_letter, 1))
        rules.append(('go_place_max_letter_' + copy_letter, '+', 'go_find_next_letter', copy_letter, -1))
            
    for skip_letter in string.ascii_lowercase + ' -@#~0123456789>|[=\n':
        rules.append(('go_find_next_letter', skip_letter, 'go_find_next_letter', skip_letter, -1))
    rules.append(('go_find_next_letter', '{', 'go_copy_max_letter', '-', 1))
    
    rules.append(('go_copy_max_letter', '@', 'place_word_number_spacer1', '@', 1))
    
    for skip_letter in string.ascii_lowercase + ' -@#~0123456789>|[=\n':
        rules.append(('place_word_number_spacer1', skip_letter, 'place_word_number_spacer1', skip_letter, 1))
    rules.append(('place_word_number_spacer1', '+', 'place_word_number_spacer2', ' ', 1))
    rules.append(('place_word_number_spacer2', '+', 'place_word_number_spacer3', '-', 1))
    rules.append(('place_word_number_spacer3', '+', 'go_get_max_number', ' ', -1))
    
    for skip_letter in string.ascii_lowercase + ' -@#~0123456789>|[=\n':
        rules.append(('go_get_max_number', skip_letter, 'go_get_max_number', skip_letter, -1))
        
    rules.append(('go_get_max_number', '@', 'find_first_max_number', '@', 1))
        
    rules.append(('find_first_max_number', '-', 'find_first_max_number', '-', 1))
    rules.append(('find_first_max_number', '0', 'find_first_max_number', '0', 1))
    for digit in '123456789':
        rules.append(('find_first_max_number', digit, 'found_first_max_number', digit, -1))
    rules.append(('found_first_max_number', '-', 'copy_max_digit', '{', 1))
    
    for copy_digit in '0123456789':
        rules.append(('copy_max_digit', copy_digit, 'go_place_max_digit_' + copy_digit, copy_digit, 1))
        for skip_letter in string.ascii_lowercase + ' -#~0123456789>|[=\n':
            rules.append(('go_place_max_digit_' + copy_digit, skip_letter, 'go_place_max_digit_' + copy_digit, skip_letter, 1))
        rules.append(('go_place_max_digit_' + copy_digit, '+', 'go_find_max_digit', copy_digit, -1))
        
    for skip_letter in string.ascii_lowercase + ' -#~0123456789>|[=\n':
        rules.append(('go_find_max_digit', skip_letter, 'go_find_max_digit', skip_letter, -1))
    rules.append(('go_find_max_digit', '{', 'go_copy_max_digit', '-', 1))
    for skip_digit in '0123456789':
        rules.append(('go_copy_max_digit', skip_digit, 'go_copy_max_digit', skip_digit, 1))
    rules.append(('go_copy_max_digit', '-', 'copy_max_digit', '{', 1))
    
    rules.append(('go_copy_max_digit', '~', 'go_place_line_break', '~', 1))
    for skip_letter in string.ascii_lowercase + ' -#~0123456789>|[=\n':
        rules.append(('go_place_line_break', skip_letter, 'go_place_line_break', skip_letter, 1))
    rules.append(('go_place_line_break', '+', 'go_decrement_twenty_four', '\n', -1))
    
    for skip_letter in string.ascii_lowercase + ' -0123456789[=\n':
        rules.append(('go_decrement_twenty_four', skip_letter, 'go_decrement_twenty_four', skip_letter, -1))
    rules.append(('go_decrement_twenty_four', '|', 'decrement_twenty_four', '|', -1))
    
    for digit in '123456789':
        rules.append(('decrement_twenty_four', digit, 'go_reset_max_register', str(int(digit) - 1), 1))
    rules.append(('decrement_twenty_four', '0', 'decrement_twenty_four', '9', -1))
    
    for skip_letter in '-0123456789|[':
        rules.append(('go_reset_max_register', skip_letter, 'go_reset_max_register', skip_letter, 1))
    rules.append(('go_reset_max_register', '=', 'reset_max_register', '=', -1))
    
    rules.append(('go_copy_max_word', '$', 'go_mark_mass_copy_start', '$', -1))
    rules.append(('decrement_twenty_four', '>', 'go_mark_mass_copy_start', '>', -1))
    
    for skip_letter in string.ascii_lowercase + '$ -~0123456789#@':
        rules.append(('go_mark_mass_copy_start', skip_letter, 'go_mark_mass_copy_start', skip_letter, -1))
    rules.append(('go_mark_mass_copy_start', '+', 'erase_first_space', '+', 1))
    rules.append(('erase_first_space', ' ', 'mark_mass_copy_start', '+', 1))
    
    for letter in string.ascii_lowercase + '$ -~0123456789#@>|[':
        rules.append(('mark_mass_copy_start', letter, 'go_find_mass_copy', '*', 1))
        rules.append(('go_find_mass_copy', letter, 'go_find_mass_copy', letter, 1))
    rules.append(('go_find_mass_copy', '=', 'go_mass_copy', '=', 1))
    rules.append(('go_mass_copy', '=', 'go_mass_copy', '=', 1))
    
    for copy_letter in string.ascii_lowercase + ' -0123456789\n':
        rules.append(('go_mass_copy', copy_letter, 'go_place_mass_letter_' + copy_letter, '=', -1))
        for skip_letter in string.ascii_lowercase + '$ -~0123456789#@>|[=':
            rules.append(('go_place_mass_letter_' + copy_letter, skip_letter, 'go_place_mass_letter_' + copy_letter, skip_letter, -1))
        rules.append(('go_place_mass_letter_' + copy_letter, '*', 'mark_mass_copy_start', copy_letter, 1))
        
    rules.append(('go_mass_copy', '+', 'clear_end', '+', -1))
    for clear_letter in string.ascii_lowercase + '$ -~0123456789#@>|[=':
        rules.append(('clear_end', clear_letter, 'clear_end', '+', -1))
    rules.append(('clear_end', '*', 'clear_end2', '+', -1))
    rules.append(('clear_end2', '\n', 'find_beginning', '+', -1))
    for skip_letter in string.ascii_lowercase + ' -0123456789\n':
        rules.append(('find_beginning', skip_letter, 'find_beginning', skip_letter, -1))
    rules.append(('find_beginning', '+', 'DONE', '+', 1))
    
    return rules
        

def parse(s, verbose=False, save_rules_to_file=False, user_stepthrough=False):
    
    charset = set()
    for char in s:
        charset.add(char)
        
    if '+' in charset:
        raise Exception("'+' in charset")
        
    stop_words = ['a', 'able', 'about', 'across', 'after', 'all', 'almost',
                  'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as',
                  'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot',
                  'could', 'dear', 'did', 'do', 'does', 'either', 'else',
                  'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has',
                  'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however',
                  'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least',
                  'let', 'like', 'likely', 'may', 'me', 'might', 'most',
                  'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off',
                  'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather',
                  'said', 'say', 'says', 'she', 'should', 'since', 'so',
                  'some', 'than', 'that', 'the', 'their', 'them', 'then',
                  'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas',
                  'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where',
                  'which', 'while', 'who', 'whom', 'why', 'will', 'with',
                  'would', 'yet', 'you', 'your']
        
    rules = generateRules(charset, stop_words)
    
    if verbose:
        print '--------------------------\n'
        print '{} rules generated.'.format(len(rules))
    
    if save_rules_to_file:
        rules_string  = ' Current State                | Read  |: New State                    | Write | Move  \n'
        rules_string += '------------------------------|-------|:------------------------------|-------|-------\n'
        rules_string += '\n'.join([' {:28} | {:5} |: {:28} | {:5} | {:5} '.format(*[str(thing).replace('\n', '\\n').replace(' ', 'SPACE') for thing in rule]) for rule in rules])
        open('rules.txt', 'w').write(rules_string)
        if verbose:
            print 'Rules saved to file rules.txt.'
        
    
    tm = TuringMachine(rules, start_state='scrub', start_tape=s, default_slot_value='+')
    
    if user_stepthrough:
        while True:
            print tm
            user_input = raw_input()
            if user_input in ('finish', 'fin', 'f'):
                break
            if len(user_input) > 0:
                for i in xrange(int(user_input)-1):
                    tm.step()
            tm.step()
        
    epoch = time()
    while not tm.halt:
        tm.step()
    elapsed = time() - epoch
        
    if verbose:
        print
        print 'Halted after {:.2f}s on step {}.'.format(elapsed, tm.steps)
        print 'State: {}'.format(tm.state)
        print 'Read: {}'.format(tm[tm.index])
        print '\nTape Printout:'
        
    return tm.get_whole_printout()


def main():
    if len(argv) < 2:
        print 'Usage:\n$ python frequency.py <filename>'
    else:
        input_string = open(argv[1]).read()
        print parse(input_string, verbose=('-v' in argv), save_rules_to_file=('-s' in argv), user_stepthrough=('-u' in argv))
        if ('-v' in argv):
            print '\n--------------------------'
    
if __name__=='__main__':
    import doctest
    doctest.testmod()
    main()