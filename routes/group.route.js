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
    text ? 'g.name LIKE $text' : null,
    terms.length ? `g.id IN (
      SELECT e.group_id
      FROM wp_terms t
      INNER JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id
      INNER JOIN wp_term_relationships tr ON tr.term_taxonomy_id = tt.term_taxonomy_id
      INNER JOIN wp_em_events e ON tr.object_id = e.post_id
      WHERE t.slug IN (${terms.map(t => `'${t}'`)})
    )` : null,
  ].filter(w => !!w)
  const rows = await sequelize.query(`SELECT
  g.id, g.name, g.slug,
  (CASE WHEN gl.logo_name IS NULL THEN NULL ELSE CONCAT('/wp-content/uploads/group-avatars/', g.id, '/', gl.logo_name) END) AS "logo"

  FROM wp_bp_groups g
  LEFT JOIN wp_bp_groups_logo gl ON g.id = gl.group_id

  ${WHERE.length ? `WHERE ${WHERE.join(' AND ')}` : ''}

  ORDER BY g.name ASC
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

app.get('/terms', async (req, res) => {
  const rows = await sequelize.query(`SELECT t.name, t.slug, COUNT(g.id) AS "groups"
  FROM
  wp_terms t
  JOIN wp_term_taxonomy tt ON tt.term_id = t.term_id
  JOIN wp_term_relationships tr ON tr.term_taxonomy_id = tt.term_taxonomy_id
  JOIN wp_em_events e ON e.post_id = tr.object_id
  JOIN wp_bp_groups g ON e.group_id = g.id
  GROUP BY t.name, t.slug`, {
    type: QueryTypes.SELECT,
  })
  res.send(rows)
})

app.get('/:id_slug', async (req, res) => {
  const id = req.params.id_slug.trim()
  const type = isNaN(+id) ? 'slug' : 'id'
  const field = `${type}`

  const WHERE = [
    `g.${field} = $id`
  ]
  const [group] = await sequelize.query(`SELECT
  g.id, g.name, g.slug,
  (CASE WHEN gl.logo_name IS NULL THEN NULL ELSE CONCAT('/wp-content/uploads/group-avatars/', g.id, '/', gl.logo_name) END) AS "logo"

  FROM wp_bp_groups g
  LEFT JOIN wp_bp_groups_logo gl ON g.id = gl.group_id
  WHERE ${WHERE.filter(w => !!w).join(' AND ')}
  LIMIT 1`, {
    type: QueryTypes.SELECT,
    bind: {
      id,
    },
  })
  if (!group) return res.status(404).send({
    error: 'no such group',
  })

  res.send(group)
})
module.exports = app