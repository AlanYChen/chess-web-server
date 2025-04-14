const express = require('express')
const {exec} = require('child_process')
const {Mutex} = require('async-mutex')

const app = express()
const PORT = 8000

const mutex = new Mutex()

const platform = process.platform
const command = (platform === "win32" ? "python" : "python3")

console.log(`platform: ${platform}`)

// TEST CHANGE

console.log("Hi")

// TEST CHANGE END

// Set body field with no parsing applied
app.use((req, res, next) => {
    let data = '';
    req.on('data', chunk => {
        data += chunk;
    });
    req.on('end', () => {
        req.body = data;
        next();
    });
});

function runPythonScript(req, resp, release) {
    const fen = req.body

    let startTime = Date.now()

    exec(command + ' python.py "' + fen + '"', (error, stdout, stderr) => {
        let endTime = Date.now()
        console.log(`Python subprocess time: ${endTime - startTime}`)
        
        release()

        if (error) {
            console.error(`error: ${error.message}`)
            return
        }

        if (stderr) {
            console.error(`error: ${stderr}`)
            return
        }

        console.log(`stdout: ${stdout}`)

        data = stdout.toString()
        resp.send(data)
    })
}

app.post('/', async (req, resp) => {
    mutex.acquire()
        .then((release) => {
            console.log("Start")
            runPythonScript(req, resp, release)
            console.log("End")
        })
})

app.listen(PORT, () => {
    console.log(`Listening to port ${PORT}`)
})