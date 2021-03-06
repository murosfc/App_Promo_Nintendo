use `db_apppromonintendo`;

create table users (    
    id VARCHAR (20) NOT NULL,
    pass VARCHAR (15) NOT NULL, 
    email VARCHAR (50),
    rec_key VARCHAR (5),
	PRIMARY KEY(id)    
  );
  
create table user_favs (
	FK_nsuid VARCHAR(20) NOT NULL,
	FK_user_id VARCHAR (20) NOT NULL,
    FOREIGN KEY (FK_nsuid) REFERENCES DB_Nintendo_BR(nsuid),
    FOREIGN KEY (FK_user_id) REFERENCES users(id)
    );
