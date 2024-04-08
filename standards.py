ETX = "ETX"
EOL = '\n'


STRING_ESCAPE = {
    'n': '\n',
    'r': '\r',
    't': '\t',
    '\\': '\\',
}

# two chars newline
# first_char : second_char
NEWLINE = {
    '\n': '\r',  # check 'EOL: \n\r' ACORN BBC and RISC OS standard
    '\r': '\n'  # check 'EOL: \r\n' Microsoft Windows, DOS, Atari TOS standard
}
