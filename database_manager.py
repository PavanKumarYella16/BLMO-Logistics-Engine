import mysql.connector
from mysql.connector import Error

class LogisticsDBManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )
            if self.connection.is_connected():
                print("Successfully connected to the enterprise logistics database.")
        except Error as e:
            print(f"Database connection initialization failed: {e}")
            self.connection = None

    def initialize_schema(self):
        if not self.connection or not self.connection.is_connected():
            print("No active connection. Cannot initialize schema.")
            return

        cursor = self.connection.cursor()
        
        create_drivers_table = """
        CREATE TABLE IF NOT EXISTS Drivers (
            driver_id INT AUTO_INCREMENT,
            driver_name VARCHAR(100) NOT NULL,
            vehicle_type VARCHAR(50) DEFAULT 'E-Bike',
            current_status VARCHAR(20) DEFAULT 'Available',
            PRIMARY KEY (driver_id)
        ) ENGINE=InnoDB;
        """

        create_destinations_table = """
        CREATE TABLE IF NOT EXISTS Destinations (
            destination_id INT AUTO_INCREMENT,
            postal_code VARCHAR(10) NOT NULL,
            distance_km DECIMAL(5,2) NOT NULL,
            traffic_zone_factor DECIMAL(3,2) DEFAULT 1.00,
            PRIMARY KEY (destination_id)
        ) ENGINE=InnoDB;
        """

        create_orders_table = """
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT AUTO_INCREMENT,
            weight_kg DECIMAL(5,2) NOT NULL,
            priority_level INT DEFAULT 1,
            driver_id INT,
            destination_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (order_id),
            CONSTRAINT fk_order_driver FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id) ON DELETE SET NULL,
            CONSTRAINT fk_order_destination FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id) ON DELETE RESTRICT
        ) ENGINE=InnoDB;
        """

        try:
            cursor.execute(create_drivers_table)
            cursor.execute(create_destinations_table)
            cursor.execute(create_orders_table)
            self.connection.commit()
            print("🏁 Phase 2 Enterprise Schema initialized successfully without errors.")
        except Error as e:
            print(f"Error executing schema initialization DDL: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    # PASTED RIGHT HERE INSIDE THE SAME CLASS
    def verify_and_insert_order(self, weight, priority, driver_id, dest_id):
        """Validates parent records exist before creating the child record."""
        cursor = self.connection.cursor()
        
        # Check if parent keys exist
        cursor.execute("SELECT driver_id FROM Drivers WHERE driver_id = %s", (driver_id,))
        if not cursor.fetchone():
            print(f"❌ Transaction Blocked: Parent Driver ID {driver_id} missing. Avoided Error 1452.")
            return False
            
        cursor.execute("SELECT destination_id FROM Destinations WHERE destination_id = %s", (dest_id,))
        if not cursor.fetchone():
            print(f"❌ Transaction Blocked: Parent Destination ID {dest_id} missing. Avoided Error 1452.")
            return False

        # Safe to execute insertion once parent integrity is verified
        insert_query = """
        INSERT INTO Orders (weight_kg, priority_level, driver_id, destination_id)
        VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (weight, priority, driver_id, dest_id))
            self.connection.commit()
            print(f"⚡ Order successfully committed to production database state.")
            return True
        except Error as e:
            print(f"Database insertion failed: {e}")
            return False
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection gracefully terminated.")