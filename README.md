https://github.com/moppimies/cybermooc
Using Django and OWASP 2021 list.

Requires Django
Start: python .\manage.py runserver
localhost:8000

user without superuser rights:
username:user
password: passwordd123

Superuser:
username:admin
password:passwordd123

admin panel: localhost:8000/admin

FLAW 1, A03:2021 – Injection:
Python-file "views.py" in the function "vote". https://github.com/moppimies/CyberMOOCProject/blob/55110b549785b0a0e9084708f77fd96ea8d5fc40/polls/views.py#L32

There is a function which queries the database without any user input sanitazitation. Sanitazitation means checking the user input for potentially hazardous requests. User could potentially make a malicous query by injecting SQL language to the request. If user could enter SQL to the question_id variable, user could modify the whole query and potentially gain access to the database.
Injection is listed as a third most common security risk in 2021 OWASP top 10 web application security risks. In worst case scenario attacker could modify data in the database or get sensitive data such as names, passwords, emails, social security numbers, street adresses etc.

The fix is provided in the code. It is commented out. The fix is rather simple because it uses django models which are tested and safe for the most part. Django automatically uses modules that sanitize the user input.


FLAW 2: CSRF-token missing:
Python file "settings.py" where the django csrf middleware is imported and html file detail.html.
https://github.com/moppimies/CyberMOOCProject/blob/35086ca06b6ffbfdc5f438cea7bb0caae455d121/seittisivut/settings.py#L48
https://github.com/moppimies/CyberMOOCProject/blob/35086ca06b6ffbfdc5f438cea7bb0caae455d121/polls/templates/polls/detail.html#L6

Although not mentioned in the OWASP 2021 top 10 web application security risks it is a potentially very hazardous.
CSRF was one of the main topics handled in the course. Modern web frameworks typically contains CSRF-token validation when the state of the website changes, usually the state changes happen when the POST-method is used.
In this example attacker could possibly vote for the blog chosen by the attacker if the CSRF-token is missing. And potentially fixing the results of the poll in favor of the attacker.

Like with previous flaw there is built-in methods and middlewares in django which provide fix for the problem. Django.middleware.csrf imported in settings.py provides csrf-tokens to the user. Django automatically warns if the POST-method is used without CSRF-tokens.
CSRF-tokens are introduced in templates.


FLAW 3: A09 - Security Logging and Monitoring Failures
Project flaw is in polls/views.py/vote function. https://github.com/moppimies/CyberMOOCProject/blob/35086ca06b6ffbfdc5f438cea7bb0caae455d121/polls/views.py#L55

The polls apps idea is to test that user is logged in before he can vote. The flaw is present if there is no "@login_required" decorator. This is a security flaw because non-authorizated users can vote. Apps idea is to give the authorizated users access to the voting.
Attacker could use a script or a botnet of multiple computers in order to influnce the results of the poll.

Fix is rather simple with Django because there is built in authentication system. Especially django.contrib.auth library contains many useful tools to authenticate the user.
Using these still require some version management from the site host, so that the outdated/flawed libraries won't go to production.


FLAW 4: Security misconfiguration A05-2021:

Flaw is present in seittisivut/settings.py if AUTH_PASSWORD_VALIDATORS is not declarated. https://github.com/moppimies/CyberMOOCProject/blob/35086ca06b6ffbfdc5f438cea7bb0caae455d121/seittisivut/settings.py#L89

User can make a new account to the database so that the password is not checked by any metrics and thus allowing the user to make accounts with very weak passwords.
E.g. admin can make a superuser with password "123456" which at first place in most used passwords in the world; https://en.wikipedia.org/wiki/Wikipedia:10,000_most_common_passwords.
A malicous user could very easily launch a bruteforce attack and gain access to the account and use it for malicious purposes. If attacker gains access to user with superuser rights, it is extremely harmful.

Djangos AUTH_PASSWORD_VALIDATORS provides the fix for this problem.
When AUTH_PASSWORD_VALIDATORS is used, user needs to a enter a password that is checked by these validators. For example "django.contrib.auth.password_validation.CommonPasswordValidator" checks if the password occurs in a list of common passwords and
"django.contrib.auth.password_validation.MinimumLengthValidator" requires the user to make account with atleast 8 characters.

FLAW 5: A02-2021 Cryptographic Failure 

Flaw is present in seittisivut/settings.py if secret_key is leaked to github or any other public page. 
In this particular case it is in public github page. https://github.com/moppimies/CyberMOOCProject/blob/35086ca06b6ffbfdc5f438cea7bb0caae455d121/seittisivut/settings.py#L24

Cryptographic failures are second most common security flaws according to OWASP 2021 list. Cryptographic failure can happen in many ways; not using encryption on sensitive data, using unsecure protocols to transfer data over the internet, weak hashing algorithms, secure keys are not stored safely, using default keys etc.
I have done this mistake and published private information on Github. Nowdays there are many bots lurking around scraping passwords and secret keys on the internet, so users making public git repos need to be extra careful.
There is lot of things that developers need to keep in mind when making a secure website.

In this case cryptographic failure could be fixed by making a .gitignore in which we could specify which files or directories we don't want in our public repositary. Another fix is to make project repositary private but in this case it is not possible.
I have made a mock up .gitignore file so I can demonstrate how it is possible to fix the problem. I need to do a mock-up fix because otherwise settings.py wouldn't go to the public git repo.
This file is named .gitignore_mock because otherwise you couldn't not see the issue on github. The fix is rather simple but easy to forget.
