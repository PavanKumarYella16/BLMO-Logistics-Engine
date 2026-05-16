import psycopg2
from psycopg2 import extensions

class LogisticsDBManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establishes connection to the PostgreSQL server and ensures the database exists."""
        try:
            # 1. Connect to default 'postgres' database first to check/create your custom DB
            conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database="postgres"  # Default administrative DB
            )
            # Postgres requires autocommit to be True to run CREATE DATABASE statements
            conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Check if our target database already exists
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.database}';")
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute(f"CREATE DATABASE {self.database};")
                print(f"📦 Created new PostgreSQL database: '{self.database}'")
                
            cursor.close()
            conn.close()

            # 2. Now connect directly to your target thesis database
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✅ Successfully connected to PostgreSQL database: '{self.database}'")
        except Exception as err:
            print(f"PostgreSQL connection initialization failed: {err}")
            self.connection = None

    def initialize_schema(self):
        """Creates parent and child tables with strict table-level constraints."""
        if not self.connection:
            print("❌ No active database connection to initialize schema.")
            return

        try:
            cursor = self.connection.cursor()
            
            # 1. Create Parent Table: Drivers
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Drivers (
                    driver_id SERIAL,
                    driver_name VARCHAR(100) NOT NULL,
                    CONSTRAINT pk_drivers PRIMARY KEY (driver_id)
                );
            """)

            # 2. Create Parent Table: Destinations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Destinations (
                    dest_id SERIAL,
                    city_name VARCHAR(100) NOT NULL,
                    CONSTRAINT pk_destinations PRIMARY KEY (dest_id)
                );
            """)

            # 3. Create Child Table: Orders (with structural Table-Level FK constraints)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Orders (
                    order_id SERIAL,
                    weight NUMERIC(10, 2) NOT NULL,
                    priority_level INT NOT NULL,
                    driver_id INT NOT NULL,
                    dest_id INT NOT NULL,
                    CONSTRAINT pk_orders PRIMARY KEY (order_id),
                    CONSTRAINT fk_orders_drivers FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id),
                    CONSTRAINT fk_orders_destinations FOREIGN KEY (dest_id) REFERENCES Destinations(dest_id)
                );
            """)
            
            self.connection.commit()
            cursor.close()
            print("🗄️ Relational database schema verified and ready.")
            
            # 💡 DEMO AUTO-SEED: Let's automatically insert a dummy driver and destination
            # so your demo script runs successfully on row 1!
            self._seed_demo_data()

        except Exception as e:
            print(f"❌ Error setting up schema tables: {e}")
            self.connection.rollback()

    def _seed_demo_data(self):
        """Helper to inject default records so parent tables aren't completely blank."""
        try:
            cursor = self.connection.cursor()
            # Ensure at least Driver ID 1 exists
            cursor.execute("INSERT INTO Drivers (driver_id, driver_name) VALUES (1, 'Default Fleet Driver') ON CONFLICT (driver_id) DO NOTHING;")
            # Ensure at least Destination ID 1 exists
            cursor.execute("INSERT INTO Destinations (dest_id, city_name) VALUES (1, 'Berlin HQ') ON CONFLICT (dest_id) DO NOTHING;")
            self.connection.commit()
            cursor.close()
        except Exception:
            self.connection.rollback()

    def verify_and_insert_order(self, weight, priority, driver_id, dest_id):
        """Applies programmatic parent validation to intercept foreign key violations gracefully."""
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()
            
            # Step A: Live check if parent keys exist before inserting
            cursor.execute("SELECT 1 FROM Drivers WHERE driver_id = %s;", (driver_id,))
            driver_exists = cursor.fetchone()
            
            cursor.execute("SELECT 1 FROM Destinations WHERE dest_id = %s;", (dest_id,))
            dest_exists = cursor.fetchone()
            
            # Step B: Guardrail intercept logic
            if not driver_exists or not dest_exists:
                print(f"⚠️  [GUARDRAIL BLOCKED] Cannot insert Order. Parent reference missing: "
                      f"Driver ID {driver_id} exists? {bool(driver_exists)} | "
                      f"Destination ID {dest_id} exists? {bool(dest_exists)}")
                cursor.close()
                return

            # Step C: Safe insert execution
            query = """
                INSERT INTO Orders (weight, priority_level, driver_id, dest_id)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (weight, priority, driver_id, dest_id))
            self.connection.commit()
            print(f"📥 Order successfully saved to DB (Weight: {weight}kg, Priority Level: {priority})")
            cursor.close()

        except Exception as e:
            print(f"❌ Transaction failed inside database row handler: {e}")
            self.connection.rollback()

    def close_connection(self):
        """Gracefully closes down the communication socket."""
        if self.connection:
            self.connection.close()
            print("🔌 PostgreSQL database connection disconnected cleanly.")