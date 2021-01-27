const {VM, NodeVM} = require('vm2')
const safevm = new VM({
    timeout: 1000,
})

try {
    // VM has timeout option but not stdout support, so if output needs to be collected (rather than just return value)
    // the program is ran through this vm first, then through NodeVM which can collect output from stdout
    let ret = safevm.run(process.argv[2])
    if(process.argv[3] == "retval-only") { // only the return value needs is needed
        console.log(ret)
        return ret
    }
} catch(error) {
    console.log("TIMEOUT")
    return "ERROR"
}

const outputfulvm = new NodeVM()
outputfulvm.run(process.argv[2])
return 22