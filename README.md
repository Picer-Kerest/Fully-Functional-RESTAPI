# Fully Functional RESTAPI
To launch a project from Docker, go to the directory with docker-compose.yml file and run Docker Desktop.
## Docker start
While in the directory, enter the following commands into the terminal
```
docker-compose build
docker-compose up -d
```
If after the entered commands you see «This Site Can’t Be Reached» this mean that the services are being started. The startup speed depends on the power of the computer. It takes me about 10 seconds.

To view the launch status of the services, you can enter the command
```
docker-compose logs -f
```

Upon successful launch, the following should be
```
db   | PostgreSQL Database directory appears to contain a database; Skipping initialization                                                                                                                                                                                                                                                                  
db   | 2023-03-27 18:49:07.423 UTC [1] LOG:  starting PostgreSQL 13.10 (Debian 13.10-1.pgdg110+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 10.2.1-6) 10.2.1 20210110, 64-bit
db   | 2023-03-27 18:49:07.424 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432                                                                                        
db   | 2023-03-27 18:49:07.424 UTC [1] LOG:  listening on IPv6 address "::", port 5432                                                                                             
db   | 2023-03-27 18:49:07.428 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"                                                                          
db   | 2023-03-27 18:49:07.445 UTC [27] LOG:  database system was shut down at 2023-03-27 02:05:39 UTC                                                                             
db   | 2023-03-27 18:49:07.461 UTC [1] LOG:  database system is ready to accept connections                                                                                        
web  | Operations to perform:
web  |   Apply all migrations: admin, auth, authentication, contenttypes, expenses, income, sessions, token_blacklist
web  | Running migrations:      
web  |   No migrations to apply.
web  | Watching for file changes with StatReloader
web  | Performing system checks...
web  | System check identified no issues (0 silenced).
web  | March 27, 2023 - 18:49:14
web  | Django version 4.1.7, using settings 'expenses_api_main.settings'
web  | Starting development server at http://0.0.0.0:8000/
web  | Quit the server with CONTROL-C.
```

After that, go to http://127.0.0.1:8000/

###  Project Information
Registration and authorization of users. Account verification via a token that is sent to the email. CRUD operations 
with expenses and income. Report on expenses and income. Password reset via a token that is sent to an email.

