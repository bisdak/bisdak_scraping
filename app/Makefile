DB_URL=postgresql://root:secret@localhost:5432/shop?sslmode=disable


createdb:
	docker exec -it postgres createdb --username=root --owner=root shop

dropdb:
	docker exec -it postgres dropdb shop

postgres:
	docker run --name postgres --network bank-network -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=secret -d postgres:14-alpine

migrateup:
	migrate -path db/migration -database "$(DB_URL)" -verbose up

migrateup1:
	migrate -path db/migration -database "$(DB_URL)" -verbose up 1

migratedown:
	migrate -path db/migration -database "$(DB_URL)" -verbose down

migratedown1:
	migrate -path db/migration -database "$(DB_URL)" -verbose down 1

.PHONY: dropdb createdb postgres migrateup migratedown migrateup1 migratedown1