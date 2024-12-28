- Unit 28.5 Hashing and Login
    - Using Flask and Python tools to save login information and create "hash" which is when a password is transcribed to enter a site. This information is a one time and one way use, it cannot be retrieved again.
    - Salt - random string of letters that can also be accompanied with hash results
- Bcrypt
    - pip install bcrypt
    - import bcrypt
    - Helps with encoding hash and salt passwords
    - Can help register and authenticating users
_____________________________________________________
- Assignment - Authentication/Authorization
    - Signup form where you can register a user, store their information and then login while passing an authentification
    - User model includes - username, password, email, first_name, last_name
    - Routes:
        - GET / or /register - Shows registration form
        - POST /register - processes information.
        - GET /login - Login screen for registered users
        - POST /login - Returns text "You made it!"
        - /secret - only available if user is logged in
        - GET /logout - Clears user infromation and redirects to /
        - GET /users/<username> - will only show information about user if you are logged in
        - POST /users/<username>/delete - can delete user

- Feedback Model
    - Form to add feeback - id, title, content, username
    - Routes:
        - GET /users/<username>/feedback/add - form to add feedback
        - POST /users/<username>/feedback/add - submits feedback
        - GET /feedback/<feedback-id>/update - can edit feedback
        - POST /feedback/<feedback-id>/update - submits update
        - PIST /feedback/<feedback-id>/delete - deletes feedback

_____________________________________________________________________
- Be sure to look at requirements.txt to know what programs to install