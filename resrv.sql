CREATE TABLE user (
        id INTEGER NOT NULL, 
        username VARCHAR, 
        password VARCHAR, 
        PRIMARY KEY (id)
);

CREATE TABLE machine (
        id INTEGER NOT NULL, 
        hostname VARCHAR, 
        address VARCHAR, 
        alias VARCHAR, 
        sys_user VARCHAR, 
        sys_passwd VARCHAR, 
        console_type VARCHAR(255), 
        console_sys VARCHAR, 
        console_user VARCHAR, 
        console_passwd VARCHAR, 
        console_ipmi_user VARCHAR, 
        console_ipmi_passwd VARCHAR, 
        machine VARCHAR, 
        pname VARCHAR, 
        tport VARCHAR, 
        line VARCHAR, 
        PRIMARY KEY (id), 
        UNIQUE (hostname), 
        UNIQUE (alias)
);

CREATE TABLE reservation (
        id INTEGER NOT NULL, 
        user INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(id) REFERENCES machine (id), 
        FOREIGN KEY(user) REFERENCES user (id)
);

CREATE TABLE reservation_history (
        id INTEGER NOT NULL, 
        machine_id INTEGER, 
        user_id INTEGER, 
        start DATETIME, 
        "end" DATETIME, 
        PRIMARY KEY (id), 
        FOREIGN KEY(machine_id) REFERENCES machine (id), 
        FOREIGN KEY(user_id) REFERENCES user (id)
);
