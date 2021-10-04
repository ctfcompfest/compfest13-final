const bodyParser = require('body-parser')
const express = require('express')
const path = require('path')

const { error404, errorDefault } = require('./routes/errors')
const index = require('./routes/index')

const app = express()
const port = process.env.PORT || 3000

app.set('views', path.join(__dirname, 'views'))

app.use(bodyParser.json())

app.use('/', index)
app.use(error404)
app.use(errorDefault)

app.listen(port, () => {
    console.log(`Express started on port ${port}`)
})