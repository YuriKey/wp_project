INSERT INTO wp_posts(
    post_title,
    post_date,
    post_date_gmt,
    post_modified,
    post_modified_gmt,
    post_content,
    post_excerpt,
    to_ping,
    pinged,
    post_content_filtered)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);