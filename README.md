prep.py
=======
[![Build Status](https://travis-ci.org/unmanifest/prep.py.png?branch=master)](https://travis-ci.org/unmanifest/prep.py)

A preprocessor

A python version of the Perl Preprocessor found here: https://github.com/drom/prep.pl

See example template files under test/sum. Template rules are fairly simple.
- Lines beginning with '//;' are interpreted as code lines.
- Lines not beginning with that character sequence are interpreted as 'here
  document' print statements.
- By default, the indentation level of the print statement will match the
  indentation of the previous line (immediately preceding it).
- A commented code line '//;[whitespace]#' can be used to update the
  indentation level such that subsequent prints use the new indentation level
  as determined by '[whitespace]' in the comment line format shown above.
