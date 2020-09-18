const { Router } = require('express')
const moment = require('moment')
const { sequelize, Sequelize: { QueryTypes } } = require('../models/models')

const app = new Router()

app.get('/', async (req, res) => {
  const page = Math.max(0, Math.floor(+(req.query.page || 1)) - 1)
  const per_page = Math.max(1, Math.min(100, Math.floor(+(req.query.per_page || 20))))
  const terms = (req.query.terms || '').split(',').filter(g => !!g.trim()).map(g => g.replace(/[^a-zA-Z0-9 _-]/g, '')).filter(g => !!g.trim())
  const text = (req.query.text || '').replace(/[^a-zA-Z0-9 _-]/g, '')
  
  const WHERE = [
    'l.location_slug != \'\' AND l.location_slug != \'test\'',
    text ? 'l.location_name LIKE $text' : null,
  ].filter(w => !!w)
  const rows = await sequelize.query(`SELECT
  l.location_id AS id, l.location_name AS name, l.location_slug AS slug

  FROM wp_em_locations l

  ${WHERE.length ? `WHERE ${WHERE.join(' AND ')}` : ''}
  LIMIT $per_page
  OFFSET $offset`, {
    type: QueryTypes.SELECT,
    bind: {
      per_page,
      offset: page * per_page,
      text: `%${text}%`,
    },
  })
  res.send(rows.map(r => ({
    ...r,
  })))
})


app.get('/:id_slug', async (req, res) => {
  const id = req.params.id_slug.trim()
  const type = isNaN(+id) ? 'slug' : 'id'
  const field = `location_${type}`

  const WHERE = [
    `l.${field} = $id`
  ]
  const [location] = await sequelize.query(`SELECT
  l.location_id AS id, l.location_name AS name, l.location_slug AS slug
  
  FROM wp_em_locations l
  WHERE ${WHERE.filter(w => !!w).join(' AND ')}
  LIMIT 1`, {
    type: QueryTypes.SELECT,
    bind: {
      id,
    },
  })
  if (!location) return res.status(404).send({
    error: 'no such location',
  })

  res.send(location)
})
module.exports = app