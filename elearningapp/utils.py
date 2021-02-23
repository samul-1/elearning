import re
import subprocess


# takes in a text that might contain TeX formulas wrapped between $ or $$ tags,
# returns the original text unchanged if no $ tags are found, otherwise returns the original text
# where all the TeX formulas have been converted to svg and substituted with the svg code
def tex_to_svg(formula):
    output_str = ""

    # tokenize the string splitting when you encounter $ tags
    tokens = [t for t in re.split(r"(\$\$?[^\$]*\$\$?)", formula)]

    for token in tokens:
        # print("token " + str(token))
        # if this token starts with $, it's a TeX formula: pass it to node and convert to svg
        if len(token) and token[0] == "$":
            if token[1] == "$":  # double $ tag = centered formula
                # strip off the $$ tags
                stripped_token = token[2:-2]
                output_str += "<p class='text-center'>"
            else:
                # strip off the $ tags
                stripped_token = token[1:-1]

            # prepend a backslash: this prevents issues if the TeX formula starts with a - character
            # which node would otherwise interpret as an argument (the node script will remove this backslash)
            stripped_token = "\\" + stripped_token
            res = subprocess.check_output(
                [
                    "node",
                    "-r",
                    "esm",
                    "../elearning/elearningapp/tex-render/component/tex2svg",
                    stripped_token,
                ],
                shell=True,
            )
            # strip off the "b'" and "\n'"
            output_str += str(res)[2:-3]
            if token[1] == "$":  # close <p> tag
                output_str += "</p>"
        else:
            output_str += token
    return output_str
