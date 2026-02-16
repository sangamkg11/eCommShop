

<h1>About The Project</h1>
<hr>
eCommShop is an eCommerce application built with Python Django Framework. Some of the features of this project includes custom user model, categories and products, Carts, Incrementing, Decrementing and removing car items, Unlimited Product image gallery, Orders, Payments, after-order functionalities such as reduce the quantify of sold products, send the order received email, clearing the cart, Order completion page as well as generating an invoice for the order. Also we have a Review and Rating system with the interactive rating stars that even allows you to rate a half-star rating. My account functionalities for the customer who can easily edit his profile, profile pictures, change his account password, and also manage his orders and much more. 

<img width="1276" height="888" alt="image" src="https://github.com/user-attachments/assets/a57d1590-d3ff-4f96-91b1-3423942fd1ad" />

## <h1>Setup Instructions</h1>


 1. Clone the repository git clone https://github.com/sangamkg11/eCommShop.git
 2. Navigrate to the working directory cd greatkart-pre-deploy

 3. Open the project from the code editor code . or atom .

 4. Create virtual environment python -m venv env

 5. Activate the virtual environment source env/Scripts/activate

 6. Install required packages to run the project pip install -r requirements.txt

 7. Rename .env-sample to .env

 8. Fill up the environment variables: Generate your own Secret key using this tool https://djecrety.ir/, copy and paste the secret key in the SECRET_KEY field.


Your configuration should look something like this:
## 
Clone the repo and install dependencies:
```bash
SECRET_KEY=47d)n05#ei0rg4#)*@fuhc%$5+0n(t%jgxg$)!1pkegsi*l4c%
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=youremailaddress@gmail.com
EMAIL_HOST_PASSWORD=yourStrongPassword
EMAIL_USE_TLS=True

```
Note: If you are using gmail account, make sure to use app password

9. Create database tables
```bash
python manage.py migrate
```
10. Create a super user
```bash
python manage.py createsuperuser
```
GitBash users may have to run this to create a super user - winpty python manage.py createsuperuser

11. Run server
```bash
python manage.py runserver
```
12. Login to admin panel - (http://127.0.0.1:8000/eCommShop-attempt/)

13. Add categories, products, add variations, register user, login, place orders and EXPLORE SO MANY FEATURES


<h1>Support</h1>
💙 If you like this project, give it a ⭐ and share it with friends!


Made with ❤️ and Python(Django)
