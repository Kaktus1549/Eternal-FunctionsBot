CREATE TABLE IF NOT EXISTS discord_tickets_logs (
    Ticket_ID INT NOT NULL PRIMARY KEY, -- Reference to the ticket ID
    Category VARCHAR(255) NULL, -- Category of the ticket
    Transcript MEDIUMTEXT NULL, -- Transcript of the ticket
    FOREIGN KEY (Ticket_ID) REFERENCES discord_tickets(Ticket_ID)
);
