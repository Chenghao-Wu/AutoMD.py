#!/usr/bin/env python

# Author: Andrew Jewett (jewett.aij@gmail.com)
# License: MIT License  (See LICENSE.md)
# Copyright (c) 2013


man_page_text = """
Usage (example):

ttree_render.py ttree_assignments.txt < file.template > file.rendered

The argument (ttree_assignments.txt) should be a 2-column file containing
ttree-style variables (1st column), and their values (bindings, 2nd column).

This program reads a text file containing ttree-style variables,
substitutes the corresponding values stored in ttree_assignments.txt,
and prints out the new (rendered) text to the standard-out.

"""


import sys
import gc

try:
    from .ttree import ExtractFormattingCommands
    from .ttree_lex import SplitQuotedString, InputError, TemplateLexer
except (ImportError, SystemError, ValueError):
    # not installed as a package
    from ttree import ExtractFormattingCommands
    from ttree_lex import SplitQuotedString, InputError, TemplateLexer


g_filename = __file__.split('/')[-1]
g_module_name = g_filename
if g_filename.rfind('.py') != -1:
    g_module_name = g_filename[:g_filename.rfind('.py')]
g_date_str = '2019-11-02'
g_version_str = '0.2.4'
g_program_name = g_filename
#sys.stderr.write(g_program_name+' v'+g_version_str+' '+g_date_str+' ')




def main():
    try:
        if (len(sys.argv) < 2):
            raise InputError('Error running  \"' + g_program_name + '\"\n'
                             ' Typical usage:\n'
                             ' ttree_render.py ttree_assignments.txt < file.template > file.rendered\n'
                             '\n'
                             '   Missing argument.\n'
                             '   Expected the name of a 2-column file containing\n'
                             '   variable names and their bindings (values).\n'
                             '   (This is likely a programmer error.\n'
                             '    This script was not intended to be run by end users.)\n')

        bindings_filename = sys.argv[1]
        ftemplate = sys.stdin
        ftemplate_name = '__standard_input_for_ttree_render__'
        if len(sys.argv) >= 3:
            ftemplate_name = sys.argv[2]
            ftemplate = open(ftemplate_name, 'r')


        fbindings = open(bindings_filename)
        assignments = {}

        #BasicUIReadBindingsStream(assignments, f, bindings_filename)

        # The line above is robust but it uses far too much memory.
        # This for loop below works for most cases.
        for line in fbindings:
            #tokens = lines.strip().split()
            # like split but handles quotes
            tokens = SplitQuotedString(line.strip())
            if len(tokens) < 2:
                continue
            assignments[tokens[0]] = tokens[1]

        fbindings.close()
        gc.collect()
       
        lex = TemplateLexer(ftemplate, ftemplate_name)
        lex.var_delim = '$@'

        text_block_list = lex.ReadTemplate(simplify_output=True)

        output = []

        for entry in text_block_list:
            assert(isinstance(entry, str))

            if ((len(entry) > 1) and (entry[0] in lex.var_delim)):

                var_prefix = ''
                var_suffix = ''
                var_format = ''
                if ((len(entry) >= 3) and
                    (entry[1] == '{') and
                    (entry[-1] == '}')):
                    var_prefix = '{'
                    var_suffix = '}'
                    entry = entry[0] + entry[2:-1]

                if '.' in entry:
                    ic = entry.find('.')
                    var_name = entry[:ic]
                    var_format = entry[ic:]
                    if not var_format[0:7] in ('.ljust(', '.rjust('):
                        var_name = entry
                        var_format = ''
                else:
                    var_name = entry
                    var_format = ''

                if var_name not in assignments:
                    #COMMENTING OUT:
                    #raise(InputError('Error(' + g_program_name + ')'
                    #                 #' at '+ErrorLeader(var_ref.src_loc.infile,
                    #                 #                   var_ref.src_loc.lineno)+
                    #                 ' unknown variable:\n'
                    #                 '         \"' + var_name + '\"\n'))
                    # ...actually don't raise an error message:
                    # Actually there are some legitimate reaons this could occur.
                    # Some users want to put LAMMPS-style variables in the 
                    # write_once() {...} text blocks in their moltemplate files.
                    # Variables in both LAMMPS and moltemplate contain $ characters, 
                    # and this script gets confused.  Better to just ignore it
                    # when this happens instead of printing an error message.
                    # Just leave the text alone and print the variable name.
                    #
                    # Do this by substituting the variable's name as it's value:

                    var_value = entry[0] + var_prefix + var_name[1:] + var_suffix

                else:
                    var_value = assignments[var_name]

                format_fname, args = ExtractFormattingCommands(var_format)
                if format_fname == 'ljust':
                    if len(args) == 1:
                        var_value = var_value.ljust(int(args[0]))
                    else:
                        var_value = var_value.ljust(int(args[0]), args[1])
                elif format_fname == 'rjust':
                    if len(args) == 1:
                        var_value = var_value.rjust(int(args[0]))
                    else:
                        var_value = var_value.rjust(int(args[0]), args[1])
                output.append(var_value)
            else:
                output += entry

        sys.stdout.write(''.join(output))

        # If we are not reading the file from sys.stdin, then close the file:
        if ftemplate_name == '__standard_input_for_ttree_render__':
            assert(ftemplate == sys.stdin)
        else:
            ftemplate.close()

    except (ValueError, InputError) as err:
        sys.stderr.write('\n' + str(err) + '\n')
        sys.exit(-1)

    return

if __name__ == '__main__':
    main()
