CREATE TABLE "products" (
  "id" bigserial PRIMARY KEY,
  "name" varchar NOT NULL,
  "price" float,
  "volume" varchar,
  "url" varchar NOT NULL,
  "img" varchar,
  "variant_id" varchar,
  "site_id" varchar NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT (now())
);
