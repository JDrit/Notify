CREATE TABLE IF NOT EXISTS cellCarrierInfo (
    id INT NOT NULL AUTO_INCREMENT, 
    carrierName tinytext NOT NULL,
    domain tinytext NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS users (
    uidNumber NOT NULL,
    cellphoneNumber bigint(20) NOT NULL,
    cellCarrier int NOT NULL,
    admin bit NOT NULL DEFAULT 0,
    PRIMARY KEY(uidNumber),
    CONSTRAINT FOREIGN KEY(cellCarrier) REFERENCES cellCarrierInfo(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS services (
    id NOT NULL AUTO_INCREMENT,
    apiKey tinytext NOT NULL,
    serviceName tinytext NOT NULL,
    owner int NOT NULL,
    subscriptionService bit NOT NULL COMMENT '0 is regular service, 1 is subscription',
    active bit NOT NULL COMMENT '1 if the service is on, 0 if the service is turned off'
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id NOT NULL AUTO_INCREMENT,
    user int NOT NULL,
    service int NOT NULL,
    state int NOT NULL COMMENT '0=email, 1=text, 2=both, 3=none',
    PRIMARY KEY(id),
    CONSTRAINT FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FOREIGN KEY(service) REFERENCES services(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS logs (
    id INT NOT NULL AUTO_INCREMENT,
    date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notificationService INT NOT NULL COMMENT 'service that sent the notification'
    user INT NOT NULL,
    email tinytext NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT FOREIGN KEY(notificationService) REFERENCES services(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FOREIGN KEY(user) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);
