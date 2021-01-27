const {VM} = require('vm2')
const safevm = new VM({
    timeout: 1000,
})

user_program = process.argv[2]

function_name = process.argv[2].split(/^function (.*)\(/)[1]
parameters = process.argv[3].split("=")

// turn a parameter array into a string like '(param_1, param_2, ..., param_n)'
let parameter_string = '('
for(parameter of parameters) {
    parameter_string += parameter + ','
}
parameter_string = parameter_string.slice(0, -1) + ')'
// add 'function_name(params)' to the program to actually call the function defined in the input text
user_program += '\n' + function_name + parameter_string
try {
    console.log(safevm.run(user_program))
} catch(error) {
    return "ERROR"
}
