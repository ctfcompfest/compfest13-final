const ejs = require('ejs')

const { errorMessage, readTemplate } = require('../utils')

const error404 = function(req, res, next){
    res.status(404);
  
    res.format({
        html: function () {
            let err = {'status': 404}
            next(err)
        },
        json: function () {
            res.json({ error:'Not found'})
        },
        default: function () {
            res.type('txt').send('Not found')
        }
    })
}

const errorDefault = function(err, req, res, next){
    let statusCode = err.status || 500
    let statusMsg = errorMessage[statusCode]
    let html = readTemplate('error.html')
        .replace('{{ code }}', statusCode)
        .replace('{{ message }}', statusMsg)

    res.status(statusCode)
    res.send(ejs.render(html))
}

module.exports = {error404, errorDefault}