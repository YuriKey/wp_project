SELECT DISTINCT
    u.ID,
    u.user_login,
    u.user_email,
    u.display_name,
    m.meta_value AS last_name
FROM
    wp_users u
LEFT JOIN
    wp_usermeta m
ON
    u.ID = m.user_id AND m.meta_key = 'last_name'
WHERE
    u.ID = ?;