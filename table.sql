CREATE TABLE departments (
	department_id SERIAL PRIMARY KEY,
	department_name VARCHAR(32)
);
CREATE TABLE products (
	product_id SERIAL PRIMARY KEY,
	product_name VARCHAR(16)
);
CREATE TABLE items (
	item_id SERIAL NOT NULL PRIMARY KEY,
	sensor_serial VARCHAR(64) NOT NULL ,
	create_date DATE,
	expired_date DATE,
	department_id INT NOT NULL REFERENCES departments(department_id),
	product_id INT NOT NULL REFERENCES products(product_id)
);