const { Router } = require('express')
const moment = require('moment')
const { sequelize, Sequelize: { QueryTypes } } = require('../models/models')

const app = new Router()

app.get('/', async (req, res) => {
  const page = Math.max(0, Math.floor(+(req.query.page || 1)) - 1)
  const per_page = Math.max(1, Math.min(100, Math.floor(+(req.query.per_page || 20))))
  const group_ids = (req.query.group_ids || '').split(',').filter(g => !!g.trim()).map(g => +g).filter(n => !isNaN(n))
  const location_ids = (req.query.location_ids || '').split(',').filter(g => !!g.trim()).map(g => +g).filter(n => !isNaN(n))
  const types = (req.query.types || '').split(',').filter(g => !!g.trim()).map(g => g.replace(/[^a-zA-Z0-9\&,\. _-]/g, '')).filter(g => !!g.trim())
  const terms = (req.query.terms || '').split(',').filter(g => !!g.trim()).map(g => g.replace(/[^a-zA-Z0-9 _-]/g, '')).filter(g => !!g.trim())
  const text = (req.query.text || '').replace(/[^a-zA-Z0-9 _-]/g, '')
  const backwards = (req.query.backwards === 'true')
  const from_datetime = req.query.from_datetime && moment(req.query.from_datetime).isValid() ? moment(req.query.from_datetime).toISOString() : null
  
  const WHERE = [
    `event_start_date ${backwards ? '<' : '>='} ${from_datetime ? '$from_datetime' : 'current_date'}`,
    text ? 'e.event_name LIKE $text' : null,
    group_ids.length ? `e.group_id IN (${group_ids})` : null,
    location_ids.length ? `e.location_id IN (${location_ids})` : null,
    types.length ? `e.post_id IN (
      SELECT post_id
      FROM wp_postmeta
      WHERE meta_key = 'Veranstaltungsart' AND meta_value IN (${types.map(t => `'${t}'`)})
    )` : null,
    terms.length ? `e.post_id IN (
      SELECT tr.object_id
      FROM wp_terms t
      INNER JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id
      INNER JOIN wp_term_relationships tr ON tr.term_taxonomy_id = tt.term_taxonomy_id
      WHERE t.slug IN (${terms.map(t => `'${t}'`)})
    )` : null,
  ]
  const rows = await sequelize.query(`SELECT
  e.event_id AS id,
  e.event_start AS start,
  e.event_end AS end,
  e.event_name AS name,
  e.event_slug AS slug,
  JSON_REMOVE(JSON_OBJECTAGG(IFNULL(pm.meta_key, 'null__'), pm.meta_value), '$.null__') AS meta,
  JSON_REMOVE(JSON_OBJECTAGG(IFNULL(t.slug, 'null__'), t.name), '$.null__') AS terms,
  JSON_OBJECT('name', l.location_name, 'slug', l.location_slug, 'id', l.location_id) AS location,
  JSON_OBJECT(
    'name', g.name, 'slug', g.slug, 'id', g.id,
    'logo', (CASE WHEN gl.logo_name IS NULL THEN NULL ELSE CONCAT('/wp-content/uploads/group-avatars/', g.id, '/', gl.logo_name) END)
  ) AS \`group\`
  FROM wp_em_events e
  LEFT JOIN wp_bp_groups g ON e.group_id = g.id
  LEFT JOIN wp_bp_groups_logo gl ON g.id = gl.group_id
  LEFT JOIN wp_em_locations l ON l.location_id = e.location_id
  LEFT JOIN wp_postmeta pm ON (pm.meta_key NOT LIKE '\\_%' OR pm.meta_key = '_wp_attached_file') AND e.post_id = pm.post_id
  LEFT JOIN wp_term_relationships tr ON e.post_id = tr.object_id
  LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
  LEFT JOIN wp_terms t ON tt.term_id = t.term_id
  WHERE ${WHERE.filter(w => !!w).join(' AND ')}
  AND e.event_private = 0
  GROUP BY e.event_id, e.event_start, e.event_end, e.event_name, e.event_slug
  ORDER BY event_start_date ${backwards ? 'DESC' : 'ASC'}
  LIMIT $per_page
  OFFSET $offset`, {
    type: QueryTypes.SELECT,
    bind: {
      per_page,
      offset: page * per_page,
      text: `%${text}%`,
      from_datetime,
    },
  })
  res.send(rows.map(r => ({
    ...r,
    thumbnail: r.meta._wp_attached_file || r.group.logo || null,
  })))
})

app.get('/terms', async (req, res) => {
  const rows = await sequelize.query(`SELECT t.name, t.slug, COUNT(e.event_id) AS events
  FROM
  wp_terms t
  JOIN wp_term_taxonomy tt ON tt.term_id = t.term_id
  JOIN wp_term_relationships tr ON tr.term_taxonomy_id = tt.term_taxonomy_id
  JOIN wp_em_events e ON e.post_id = tr.object_id
  GROUP BY t.name, t.slug`, {
    type: QueryTypes.SELECT,
  })
  res.send(rows)
})

app.get('/types', async (req, res) => {
  const rows = await sequelize.query(`SELECT meta_value FROM
  wp_postmeta pm
  JOIN wp_em_events e ON pm.post_id = e.post_id
  WHERE pm.meta_key = 'Veranstaltungsart'
  GROUP BY meta_value
  `, {
    type: QueryTypes.SELECT,
  })
  res.send(rows.map(({ meta_value }) => meta_value))
})

app.get('/by-day/:date', async (req, res) => {
  const date = moment(req.params.date)
  if (!req.params.date || !date.isValid()) return res.status(400).send({
    error: 'invalid date',
  })
  const dayStart = date.clone().startOf('day').toISOString()
  const dayEnd = date.clone().startOf('day').toISOString()
  const page = Math.max(0, Math.floor(+(req.query.page || 1)) - 1)
  const per_page = Math.max(1, Math.min(100, Math.floor(+(req.query.per_page || 20))))
  const WHERE = [
    `e.event_start < $dayEnd`,
    `e.event_end > $dayStart`,
  ]
  const rows = await sequelize.query(`SELECT
  e.event_id AS id,
  e.event_start AS start,
  e.event_end AS end,
  e.event_name AS name,
  e.event_slug AS slug,
  JSON_REMOVE(JSON_OBJECTAGG(IFNULL(pm.meta_key, 'null__'), pm.meta_value), '$.null__') AS meta,
  JSON_REMOVE(JSON_OBJECTAGG(IFNULL(t.slug, 'null__'), t.name), '$.null__') AS terms,
  JSON_OBJECT('name', l.location_name, 'slug', l.location_slug, 'id', l.location_id) AS location,
  JSON_OBJECT(
    'name', g.name, 'slug', g.slug, 'id', g.id,
    'logo', (CASE WHEN gl.logo_name IS NULL THEN NULL ELSE CONCAT('/wp-content/uploads/group--avatars/', g.id, '/', gl.logo_name) END)
  ) AS \`group\`
  FROM wp_em_events e
  LEFT JOIN wp_bp_groups g ON e.group_id = g.id
  LEFT JOIN wp_bp_groups_logo gl ON g.id = gl.group_id
  LEFT JOIN wp_em_locations l ON l.location_id = e.location_id
  LEFT JOIN wp_postmeta pm ON (pm.meta_key NOT LIKE '\\_%' OR pm.meta_key = '_wp_attached_file') AND e.post_id = pm.post_id
  LEFT JOIN wp_term_relationships tr ON e.post_id = tr.object_id
  LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
  LEFT JOIN wp_terms t ON tt.term_id = t.term_id
  WHERE ${WHERE.filter(w => !!w).join(' AND ')}
  AND e.event_private = 0
  GROUP BY e.event_id, e.event_start, e.event_end, e.event_name, e.event_slug
  ORDER BY event_end ASC
  LIMIT $per_page
  OFFSET $offset`, {
    type: QueryTypes.SELECT,
    bind: {
      per_page,
      offset: page * per_page,
      dayStart,
      dayEnd,
    },
  })

  res.send(rows)
})
app.get('/:id_slug', async (req, res) => {
  const id = req.params.id_slug.trim()
  const type = isNaN(+id) ? 'slug' : 'id'
  const field = `event_${type}`

  const WHERE = [
    `${field} = $id`
  ]
  const [event] = await sequelize.query(`SELECT
  e.event_id AS id,
  e.event_start AS start,
  e.event_end AS end,
  e.event_name AS name,
  e.event_slug AS slug,
  JSON_REMOVE(JSON_OBJECTAGG(IFNULL(pm.meta_key, 'null__'), pm.meta_value), '$.null__') AS meta,
  JSON_REMOVE(JSON_OBJECTAGG(IFNULL(t.slug, 'null__'), t.name), '$.null__') AS terms,
  JSON_OBJECT('name', l.location_name, 'slug', l.location_slug, 'id', l.location_id) AS location,
  JSON_OBJECT(
    'name', g.name, 'slug', g.slug, 'id', g.id,
    'logo', (CASE WHEN gl.logo_name IS NULL THEN NULL ELSE CONCAT('/wp-content/uploads/group--avatars/', g.id, '/', gl.logo_name) END)
  ) AS \`group\`
  FROM wp_em_events e
  LEFT JOIN wp_bp_groups g ON e.group_id = g.id
  LEFT JOIN wp_bp_groups_logo gl ON g.id = gl.group_id
  LEFT JOIN wp_em_locations l ON l.location_id = e.location_id
  LEFT JOIN wp_postmeta pm ON (pm.meta_key NOT LIKE '\\_%' OR pm.meta_key = '_wp_attached_file') AND e.post_id = pm.post_id
  LEFT JOIN wp_term_relationships tr ON e.post_id = tr.object_id
  LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
  LEFT JOIN wp_terms t ON tt.term_id = t.term_id
  WHERE ${WHERE.filter(w => !!w).join(' AND ')}
  AND e.event_private = 0
  GROUP BY e.event_id, e.event_start, e.event_end, e.event_name, e.event_slug
  ORDER BY event_start_date DESC
  LIMIT 1`, {
    type: QueryTypes.SELECT,
    bind: {
      id,
    },
  })
  if (!event) return res.status(404).send({
    error: 'no such event',
  })

  res.send(event)
})
module.exports = app