Schema
1. **users**: Stores user-specific details.
2. **codes**: A lookup table to manage different types of codes, like the bike's status.
3. **bikes**: Contains information about each bike, including its type, last maintenance date, and current status.
4. **maintenance_records**: Logs maintenance activities for each bike.
5. **payment_history**: Records each payment made by users for their trips.
6. **bikeshare_stations**: Provides information about each station, such as its name, status, and location.
7. **trip_data**: Captures details about each trip, including duration, start and end times, associated stations, the bike used, and the user.
8. **payment_types**: A lookup table for various payment methods.
9. **user_payment_types**: Represents the many-to-many relationship between users and their chosen payment methods.

The relationships (foreign keys) between the tables are well-defined, ensuring data consistency and referential integrity.
