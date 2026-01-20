IMPORTANT: 

The project will only run if you follow all steps below in a clean environment. Skipping any step will cause errors.

Remember: Create and activate a virtual environment before installing dependencies

After creating and activating venv, make sure Python and pip are available:
python --version
pip --version

---

Docker notice:
This project does not require Docker.
It runs using standard Python virtual environment and requirements.txt.
Docker was not specified as a mandatory requirement in the assignment.
The recommended and supported way to run the project is via venv.

---

OPTIONAL

* The .venv / venv folders are NOT included intentionally

* The virtual environment must be created on the tester's local machine

* The project was tested by running it completely from scratch in a clean environment


---

Project Setup & Usage Guide

Notice:

* All API requests are provided in a Postman collection.
  Import the collection into Postman before testing.
* For email functionality:

  * Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py.
  * Use your Gmail address and App Password.

* Python version: 3.10+ recommended.
* Always activate the virtual environment before installing dependencies and running the server.

---

Note: The .venv/venv folder is not included. Create a new virtual environment and install dependencies using requirements.txt before running the server.

---

OPTIONAL

* The .venv / venv folders are NOT included intentionally

* The virtual environment must be created on the tester's local machine

* The project was tested by running it completely from scratch in a clean environment

---

ABOUT TESTING

The project was tested:

* via the console

* via Postman (all requests from the collection)

* taking into account roles and permissions

* with JWT authentication

* with a separate frontend (HTML + JS)

* All functionality was tested before submission.

---

---

IMPORTANT:
The project will ONLY launch after ALL steps below have been completed in a clean environment.

---

Activation:

For server activation:

```bash (Recommend to type commands on console by order in order to launch the server)
1. python -m venv venv(on Windows), python3 -m venv venv(on Linux/Mac)
2. venv/Scripts/activate(on Windows), source venv/bin/activate(on Linux/Mac)
3. pip install -r requirements.txt
4. python manage.py runserver
```

Skipping any of steps 1–3 will result in a server startup error.

Server runs at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

Users & Roles

Console:

* Create superuser (Admin):

```bash
python manage.py createsuperuser
```

Used to manage staff and system settings.

Postman:

* Create user: Test_DRF/users/CreateUser (Anyone can create an account)
* Become seller: Test_DRF/users/Become_a_seller (User becomes basic seller)
* Become client: Test_DRF/users/Become_a_client (User becomes client)
* Get all users: Test_DRF/users/allUsers (Accessible mainly by staff/admin)
* Delete user: Test_DRF/users/DeleteUser (Authorized users delete own account; Admin/Staff delete any user)
* Buy premium: Test_DRF/users/buy_premium (Payment simulated; set force_fail=true to simulate failure)

Admin & Staff:

* Create staff: Test_DRF/users/Admin and staff/createManager (Admin only)
* Block user: Test_DRF/users/Admin and staff/BlockUser
* Unblock user: Test_DRF/users/Admin and staff/UnBlockUser

---

Authentication

Postman Login Endpoints:

* Admin login: Test_DRF/auth/login_admin
* Staff login: Test_DRF/auth/login_staff
* Seller login: Test_DRF/auth/login_seller
* Client login: Test_DRF/auth/login_client

Authentication is handled using JWT (SimpleJWT).

---

Advertisements

Postman:

* Create advertisement: Test_DRF/Advertisement/CreateAd (Basic sellers: 1 ad; Premium: unlimited)
* Edit advertisement: Test_DRF/Advertisement/editAd (Max 3 attempts due to moderation)
* Delete advertisement: Test_DRF/Advertisement/DeleteAd (Seller / Staff / Admin)
* View advertisement: Test_DRF/Advertisement/ad_view (Public access)

Premium Only:

* View advertisement statistics: Test_DRF/Advertisement/premium_only/ad_stats (Premium sellers only)

Important Notice:

* Daily - 15s, Weekly - 30s, Monthly - 45s

Sorting & Filtering:

* Sort by year: Sort_by_year (year_lt, year_gt, year_in)
* Sort by price: Sort_by_price (price_lt, price_gt, price_in)
* Sort by brand: Sort_by_brand (brand)

---

Chat System

Postman:

* Create chat room: Test_DRF/Chat/createChat (Client initiates chat from advertisement page)
* Load chat room: Test_DRF/Chat/loadChat (Load chat using chat ID)

Frontend (HTML + JS):

* Frontend is separated from Django templates
* Move HTML folder outside Django project (e.g., Desktop)
* Open chat.html in a browser (Change id of chat_id room into current created chat room id in main.js file in folder before logging into the account)
* Open two browsers:

  * One logged in as client
  * One logged in as seller
* Send messages between users
* Messages persist after page reload
* Uses JWT, Fetch API, and CORS
* Frontend stores the JWT token received from login and sends it in the 'Authorization' header for all requests.
* Messages sorted by time

---

Postman & Mock data

Test accounts:

Role	Email	                Password
Admin	testAdmin5@gmail.com	super123
Staff	testManager@gmail.com	super123
Seller	testSeller10@gmail.com	super123
Client	testBuyer5@gmail.com	super123

Project Status:

* JWT Authentication
* Role-based permissions
* Advertisement moderation
* Premium logic
* Chat system
* Separate frontend
* Postman tested
* Console tested

Final Notes:

* Backend controls all sensitive fields (sender, buyer, seller)
* Frontend never sends user IDs manually
* Chat messages are secure and role-restricted
* Frontend folder should be zipped together with the HTML/JS files for submission.
* Postman collection also included in submission for testing API endpoints.

Teacher note:

* Frontend is separated intentionally to demonstrate API-only backend design.
* Staff/Admin permissions are enforced via DRF permission classes.
* Only staff or admin can block/unblock users.