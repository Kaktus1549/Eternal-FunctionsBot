CREATE TABLE discord_tickets (
    Ticket_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- Ticket ID
    Discord_ID BIGINT NOT NULL, -- Discord ID of the ticket creator
    Opened BOOLEAN NOT NULL DEFAULT TRUE, -- Whether the ticket is open or closed
    Open_Date Date NOT NULL DEFAULT (DATE_ADD(CURDATE(), INTERVAL 30 DAY)), -- Date the ticket was opened
    Claimed_by TEXT NULL DEFAULT NULL -- Discord ID of the staff member who claimed the ticket
);