const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser')

const fs = require('fs')
const path = require('path')

const PORT = process.env.PORT || 8080
const ROUTEDIR = path.join(__dirname, 'routes')
const PREFIX = process.env.PREFIX || 'api'

const app = express()


app.use(cors())
app.use(bodyParser.json())

const routeFiles = fs.readdirSync(ROUTEDIR).filter(f => f.endsWith('.route.js'))

for (const file of routeFiles) {
  const route = [file.replace('.route.js', '')].filter(f => !!f).join('/')
  const handler = require(path.join(ROUTEDIR, file))
  console.log('register route /%s', route)
  app.use(`/${route}`, handler)
}

app.listen(PORT, () => console.log(`ready on port %s`, PORT))
