INSERT INTO users (id, name) VALUES
    (1, 'Ada'), (2, 'Linus'), (3, 'Grace'), (4, 'Dennis')
ON CONFLICT (id) DO NOTHING;

INSERT INTO follows (follower_id, followee_id) VALUES
    (1, 2), (1, 3), (2, 3), (3, 4)
ON CONFLICT DO NOTHING;

INSERT INTO posts (id, author_id, text, created_at) VALUES
    (101, 2, 'Shipping the new scheduler today',  now() - interval '1 hour'),
    (102, 3, 'Compilers are just very patient maps', now() - interval '2 hours'),
    (103, 4, 'Wrote a tiny shell over the weekend',  now() - interval '30 minutes'),
    (104, 3, 'Hiring two backend engineers',         now() - interval '5 hours'),
    (105, 2, 'TIL about KRaft mode',                 now() - interval '10 minutes')
ON CONFLICT (id) DO NOTHING;

-- keep the sequences ahead of the explicit ids we inserted
SELECT setval('users_id_seq', (SELECT max(id) FROM users));
SELECT setval('posts_id_seq', (SELECT max(id) FROM posts));
